import flask_restful
from flask import request, g
from marshmallow import ValidationError

from app import db, RestException, auth
from app.model.participant import Participant
from app.model.user_participant import UserParticipant
from app.resources.schema import UserParticipantsSchema, ParticipantSchema
from app.wrappers import requires_roles


class ParticipantBySessionEndpoint(flask_restful.Resource):

    schema = UserParticipantsSchema()
    participant_schema = ParticipantSchema()

    @auth.login_required
    def get(self, relationship):
        user_participants = db.session.query(UserParticipant).\
            join(UserParticipant.participant).\
            filter(UserParticipant.user_id == g.user.id and UserParticipant.relationship == relationship).\
            order_by(Participant.last_name).\
            all()
        return self.schema.dump(user_participants, many=True)

    @auth.login_required
    def post(self, relationship):
        request_data = request.get_json()
        try:
            load_result = self.participant_schema.load(request_data).data
            relation = UserParticipant(user_id = g.user.id, participant=load_result, relationship=relationship)
            db.session.add(load_result)
            db.session.add(relation)
            db.session.commit()
            return self.schema.dump(relation)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)


class UserParticipantEndpoint(flask_restful.Resource):
    schema = UserParticipantsSchema()

    @requires_roles('Admin')
    def get(self, id):
        model = db.session.query(UserParticipant).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @requires_roles('Admin')
    def delete(self, id):
        db.session.query(UserParticipant).filter_by(id=id).delete()
        db.session.commit()
        return None



