import flask_restful
from flask import request

from app import db, RestException
from app.model.participant import Participant
from app.model.user import User
from app.model.user_participant import UserParticipant
from app.resources.schema import UserParticipantSchema, UserParticipantsSchema, ParticipantUsersSchema


class UserByParticipantEndpoint(flask_restful.Resource):

    schema = ParticipantUsersSchema()

    def get(self, participant_id):
        user_participants = db.session.query(UserParticipant)\
            .join(UserParticipant.user)\
            .filter(UserParticipant.participant_id == participant_id)\
            .order_by(User.title)\
            .all()
        return self.schema.dump(user_participants, many=True)


class ParticipantByUserEndpoint(flask_restful.Resource):

    schema = UserParticipantsSchema()

    def get(self, user_id):
        user_participants = db.session.query(UserParticipant).\
            join(UserParticipant.participant).\
            filter(UserParticipant.user_id == user_id).\
            order_by(Participant.name).\
            all()
        return self.schema.dump(user_participants,many=True)

    def post(self, user_id):
        request_data = request.get_json()
        user_participants = self.schema.load(request_data, many=True).data
        db.session.query(UserParticipant).filter_by(user_id=user_id).delete()
        for up in user_participants:
            db.session.add(UserParticipant(user_id=user_id,
                           participant_id=up.participant_id))
        db.session.commit()
        return self.get(user_id)


class UserParticipantEndpoint(flask_restful.Resource):
    schema = UserParticipantSchema()

    def get(self, id):
        model = db.session.query(UserParticipant).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        db.session.query(UserParticipant).filter_by(id=id).delete()
        db.session.commit()
        return None


class UserParticipantListEndpoint(flask_restful.Resource):
    schema = UserParticipantSchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data).data
        db.session.query(UserParticipant).filter_by(user_id=load_result.user_id,
                                                     participant_id=load_result.participant_id).delete()
        db.session.add(load_result)
        db.session.commit()
        return self.schema.dump(load_result)
