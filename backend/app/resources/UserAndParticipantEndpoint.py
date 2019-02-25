import flask_restful
from flask import request, g
from marshmallow import ValidationError
from sqlalchemy import exc

from app import db, RestException, auth
from app.model.participant import Participant
from app.model.user import User
from app.resources.schema import ParticipantSchema


class ParticipantBySessionEndpoint(flask_restful.Resource):

    schema = ParticipantSchema()

    @auth.login_required
    def get(self):
        participants = db.session.query(Participant).\
            filter(Participant.user_id == g.user.id).\
            order_by(Participant.id).\
            all()
        return self.schema.dump(participants, many=True)

    @auth.login_required
    def post(self):
        request_data = request.get_json()
        if 'user_id' not in request_data:
            request_data['user_id'] = g.user.id
        try:
            load_result = self.schema.load(request_data).data
            if load_result.user is None:
                load_result.user = db.session.query(User).filter(User.id == request_data['user_id']).first()
            db.session.add(load_result)
            db.session.commit()
            return self.schema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)
        except exc.IntegrityError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)


