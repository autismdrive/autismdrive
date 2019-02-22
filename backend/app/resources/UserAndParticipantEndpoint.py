import flask_restful
from flask import request, g
from marshmallow import ValidationError
from sqlalchemy import exc

from app import db, RestException, auth
from app.model.participant import Participant, Relationship
from app.resources.schema import ParticipantSchema


class ParticipantBySessionEndpoint(flask_restful.Resource):

    schema = ParticipantSchema()

    @auth.login_required
    def get(self):
        participants = db.session.query(Participant).\
            filter(Participant.user_id == g.user.id).\
            order_by(Participant.last_name).\
            all()
        return self.schema.dump(participants, many=True)

    @auth.login_required
    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.participant_schema.load(request_data).data
            db.session.add(load_result)
            db.session.commit()
            return self.schema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)
        except exc.IntegrityError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)


