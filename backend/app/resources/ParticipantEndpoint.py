import datetime

import flask_restful
from flask import request, g
from sqlalchemy import func, select, Select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.interfaces import LoaderOption
from sqlalchemy.sql.base import ExecutableOption

from app.auth import auth
from app.database import session
from app.enums import Permission, Role
from app.models import Participant, User
from app.rest_exception import RestException
from app.schemas import SchemaRegistry
from app.wrappers import requires_roles, requires_permission


def add_joins_to_statement(statement: Select | ExecutableOption) -> Select | LoaderOption:
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


class ParticipantEndpoint(flask_restful.Resource):

    schema = SchemaRegistry.ParticipantSchema()

    @auth.login_required
    def get(self, participant_id: int):
        db_participant = get_participant_by_id(participant_id, with_joins=True)
        session.close()
        if db_participant is None:
            raise RestException(RestException.NOT_FOUND)
        if not (db_participant and (g.user.related_to_participant(db_participant.id) or g.user.role == Role.admin)):
            raise RestException(RestException.UNRELATED_PARTICIPANT)
        return self.schema.dump(db_participant)

    @auth.login_required
    @requires_roles(Role.admin)
    def delete(self, participant_id: int):
        session.query(Participant).filter_by(id=participant_id).delete()
        return None

    @auth.login_required
    def put(self, participant_id: int):
        request_data = request.get_json()
        db_participant = get_participant_by_id(participant_id, with_joins=False)
        if db_participant is None:
            raise RestException(RestException.NOT_FOUND)
        if not (g.user.related_to_participant(db_participant.id) or g.user.role == Role.admin):
            raise RestException(RestException.UNRELATED_PARTICIPANT)

        try:
            updated = self.schema.load(request_data, instance=db_participant)
        except Exception as errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)

        updated.last_updated = datetime.datetime.utcnow()
        session.add(updated)
        session.commit()
        session.close()

        updated_db_participant = get_participant_by_id(participant_id, with_joins=True)

        session.close()
        return self.schema.dump(updated_db_participant) if updated_db_participant else None


class ParticipantListEndpoint(flask_restful.Resource):

    schema = SchemaRegistry.ParticipantSchema(many=True)

    @auth.login_required
    @requires_permission(Permission.participant_admin)
    def get(self):
        statement = add_joins_to_statement(select(Participant))
        participants = session.execute(statement).unique().scalars().all()
        session.close()
        return self.schema.dump(participants)


class ParticipantAdminListEndpoint(flask_restful.Resource):
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
