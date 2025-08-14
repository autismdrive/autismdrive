from copy import deepcopy
from http import HTTPStatus

from flask import g, request
from flask.views import MethodView
from marshmallow import ValidationError
from sqlalchemy import Select, func, select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.interfaces import LoaderOption
from sqlalchemy.sql.base import ExecutableOption

from app.auth import auth
from app.database import session
from app.enums import Permission, Role
from app.models import Participant, User
from app.rest_exception import RestException
from app.schemas import SchemaRegistry
from app.utils import utcnow
from app.wrappers import requires_permission, requires_role


def add_joins_to_statement(
    statement: Select | ExecutableOption,
) -> Select | LoaderOption:
    return statement.options(
        joinedload(Participant.user),
        joinedload(Participant.identification),
        joinedload(Participant.contact),
    )


def get_participant_by_id(participant_id: int, with_joins=False) -> Participant | None:
    """
    Returns a Participant matching the given ID from the database. Optionally include joins to parent and child Categories.

    CAUTION: Make sure to close the session after calling this function!
    """
    statement = select(Participant)

    if with_joins:
        statement = add_joins_to_statement(statement)

    statement = statement.filter_by(id=participant_id)
    return session.execute(statement).unique().scalar_one_or_none()


class ParticipantEndpoint(MethodView):
    schema = SchemaRegistry.ParticipantSchema()

    @auth.login_required
    def get(self, participant_id: int):
        from app.resources.UserEndpoint import get_user_by_id

        u_id = g.user.id
        db_participant = get_participant_by_id(participant_id, with_joins=True)

        if db_participant is None:
            raise RestException(RestException.NOT_FOUND)
        if not (g.user.related_to_participant(db_participant.id) or g.user.role == Role.admin):
            raise RestException(RestException.UNRELATED_PARTICIPANT)

        db_user = get_user_by_id(u_id, with_joins=True)
        is_related = db_user.related_to_participant(participant_id)
        is_admin = db_user.role == Role.admin

        if is_related or is_admin:
            return self.schema.dump(db_participant)

        raise RestException(RestException.UNRELATED_PARTICIPANT)

    @auth.login_required
    @requires_role(Role.admin)
    def delete(self, participant_id: int):
        session.query(Participant).filter_by(id=participant_id).delete()
        return "", 204

    @auth.login_required
    def put(self, participant_id: int):
        request_data = request.get_json()

        old_participant = get_participant_by_id(participant_id, with_joins=False)

        if old_participant is None:
            raise RestException(RestException.NOT_FOUND)
        if not (g.user.related_to_participant(old_participant.id) or g.user.role == Role.admin):
            raise RestException(RestException.UNRELATED_PARTICIPANT)
        if "user_id" in request_data and g.user.role != Role.admin:
            raise RestException(RestException.PERMISSION_DENIED, HTTPStatus.FORBIDDEN)

        try:
            updated_values = self.schema.load(data=request_data, partial=True, session=session)
        except Exception as e:
            raise RestException(RestException.INVALID_OBJECT, details=e)

        filtered_dict = {k: request_data[k] for k in request_data if k in self.schema.load_fields}
        updated_dict = {**filtered_dict, "last_updated": utcnow()}
        update_statement = update(Participant).where(Participant.id == participant_id).values(updated_dict)
        session.execute(update_statement)
        session.commit()
        session.close()

        db_updated = get_participant_by_id(participant_id, with_joins=True)
        return self.schema.dump(db_updated)

class ParticipantListEndpoint(MethodView):
    schema = SchemaRegistry.ParticipantSchema(many=True)

    @auth.login_required
    @requires_permission(Permission.participant_admin)
    def get(self):
        statement = add_joins_to_statement(select(Participant))
        participants = session.execute(statement).unique().scalars().all()
        session.close()
        return self.schema.dump(participants)


class ParticipantAdminListEndpoint(MethodView):
    def count_participants(self, relationship, filter_out_test=False):
        if filter_out_test:
            query = session.query(Participant).filter(
                Participant.relationship == relationship,
                Participant.user.has(User.role != Role.admin),
                Participant.user.has(User.role != Role.test),
            )
        else:
            query = session.query(Participant).filter(Participant.relationship == relationship)
        count_q = query.statement.with_only_columns(func.count()).order_by(None)
        return query.session.execute(count_q).scalar()

    @auth.login_required
    @requires_permission(Permission.participant_admin)
    def get(self):
        statement = add_joins_to_statement(select(Participant))
        all_participants = session.execute(statement.order_by(Participant.relationship)).unique().scalars().all()
        participant_list = {
            "num_self_participants": self.count_participants("self_participant"),
            "num_self_guardians": self.count_participants("self_guardian"),
            "num_dependents": self.count_participants("dependent"),
            "num_self_professionals": self.count_participants("self_professional"),
            "num_self_interested": self.count_participants("self_interested"),
            "filtered_self_participants": self.count_participants("self_participant", filter_out_test=True),
            "filtered_self_guardians": self.count_participants("self_guardian", filter_out_test=True),
            "filtered_dependents": self.count_participants("dependent", filter_out_test=True),
            "filtered_self_professionals": self.count_participants("self_professional", filter_out_test=True),
            "filtered_self_interested": self.count_participants("self_interested", filter_out_test=True),
            "all_participants": SchemaRegistry.ParticipantSchema(many=True).dump(all_participants, many=True),
        }
        return participant_list
