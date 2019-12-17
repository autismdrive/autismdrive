import datetime

import flask_restful
from flask import request, g
from sqlalchemy import func

from app import RestException, db, auth
from app.model.participant import Participant
from app.model.user import Role
from app.schema.schema import ParticipantSchema
from app.wrappers import requires_roles


class ParticipantEndpoint(flask_restful.Resource):

    schema = ParticipantSchema()

    @auth.login_required
    def get(self, id):
        model = db.session.query(Participant).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        if not model and (g.user.related_to_participant(model.id) and not g.user.role == Role.admin):
            raise RestException(RestException.UNRELATED_PARTICIPANT)
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_roles(Role.admin)
    def delete(self, id):
        db.session.query(Participant).filter_by(id=id).delete()
        return None

    @auth.login_required
    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Participant).filter_by(id=id).first()
        if not g.user.related_to_participant(instance.id) and not g.user.role == Role.admin:
            raise RestException(RestException.UNRELATED_PARTICIPANT)
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)


class ParticipantListEndpoint(flask_restful.Resource):

    schema = ParticipantSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        participants = db.session.query(Participant).all()
        return self.schema.dump(participants)


class ParticipantAdminListEndpoint(flask_restful.Resource):
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
