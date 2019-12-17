import flask_restful
from flask import request, g
from marshmallow import ValidationError
from sqlalchemy import exc, func

from app import db, RestException, auth
from app.model.participant import Participant, Relationship
from app.model.user import User, Role
from app.schema.schema import ParticipantSchema
from app.wrappers import requires_roles


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
        if 'relationship' in request_data:
            if not Relationship.has_name(request_data['relationship']):
                raise RestException(RestException.UNKNOWN_RELATIONSHIP,
                                    details="Valid Options:" + ','.join(Relationship.options()))
            else:
                relationship = request_data['relationship']
                request_data.pop('relationship', None)
        else:
            relationship = None
        if 'user_id' not in request_data:
            request_data['user_id'] = g.user.id
        try:
            load_result = self.schema.load(request_data).data
            load_result.user = db.session.query(User).filter(User.id == request_data['user_id']).first()
            load_result.relationship = relationship
            db.session.add(load_result)
            db.session.commit()
            return self.schema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)
        except exc.IntegrityError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)


class UserParticipantListEndpoint(flask_restful.Resource):
    def count_participants(self, relationship):
        query = db.session.query(Participant).filter(Participant.relationship == relationship)
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        return query.session.execute(count_q).scalar()

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        participant_list = {
            'num_self_participants': self.count_participants('self_participant'),
            'num_self_guardians': self.count_participants('self_guardian'),
            'num_dependents': self.count_participants('dependent'),
            'num_self_professionals': self.count_participants('self_professional'),
            'all_participants': ParticipantSchema(many=True).dump(db.session.query(Participant)
                                                                  .order_by(Participant.relationship).all(), many=True)
        }
        return participant_list
