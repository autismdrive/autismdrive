import flask_restful
from flask import request, g
from marshmallow import ValidationError
from sqlalchemy import exc, cast, Integer

from app.auth import auth
from app.database import session
from app.models import Participant, User
from app.enums import Relationship
from app.rest_exception import RestException
from app.schemas import ParticipantSchema


class ParticipantBySessionEndpoint(flask_restful.Resource):

    schema = ParticipantSchema()

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

        user = session.query(User).filter(User.id == request_data["user_id"]).first()
        if user.self_participant() is not None:
            if Relationship.is_self(relationship):
                raise RestException(RestException.NOT_YOUR_ACCOUNT)

        try:
            load_result = self.schema.load(request_data)
            load_result.user = session.query(User).filter(User.id == request_data["user_id"]).first()
            load_result.relationship = relationship
            session.add(load_result)
            session.commit()
            return self.schema.dump(load_result)
        except (ValidationError, exc.IntegrityError) as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)
