import flask_restful
from flask import request, g
from marshmallow import ValidationError
from sqlalchemy import exc, cast, Integer, select
from sqlalchemy.orm import joinedload

from app.auth import auth
from app.database import session
from app.models import Participant, User
from app.enums import Relationship
from app.rest_exception import RestException
from app.schemas import SchemaRegistry


class ParticipantBySessionEndpoint(flask_restful.Resource):

    schema = SchemaRegistry.ParticipantSchema()

    @auth.login_required
    def get(self):
        participants = (
            session.query(Participant)
            .filter(Participant.user_id == cast(g.user.id, Integer))
            .order_by(Participant.id)
            .all()
        )
        return self.schema.dump(participants, many=True)

    @auth.login_required
    def post(self):
        request_data = request.get_json()
        if "relationship" in request_data:
            if not Relationship.has_name(request_data["relationship"]):
                raise RestException(
                    RestException.UNKNOWN_RELATIONSHIP, details="Valid Options:" + ",".join(Relationship.options())
                )
            else:
                relationship = request_data["relationship"]
                request_data.pop("relationship", None)

        else:
            relationship = None

        if "user_id" not in request_data:
            request_data["user_id"] = g.user.id

        user_id = cast(request_data["user_id"], Integer)
        user = session.query(User).filter(User.id == user_id).first()
        if user.self_participant() is not None:
            if Relationship.is_self(relationship):
                raise RestException(RestException.NOT_YOUR_ACCOUNT)

        try:
            load_result = self.schema.load(request_data)
            db_user = session.query(User).filter(User.id == user_id).first()

            if db_user is None:
                raise RestException(
                    RestException.NOT_FOUND, details=f"User with id {request_data['user_id']} not found."
                )

            load_result.user_id = db_user.id
            load_result.relationship = relationship
            session.add(load_result)
            session.commit()
            participant_id = load_result.id
            session.close()

            db_participant = (
                session.execute(
                    select(Participant)
                    .options(
                        joinedload(Participant.user),
                        joinedload(Participant.identification),
                        joinedload(Participant.contact),
                    )
                    .filter(Participant.id == participant_id)
                )
                .unique()
                .scalar_one()
            )

            return self.schema.dump(db_participant)
        except (ValidationError, exc.IntegrityError) as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)
