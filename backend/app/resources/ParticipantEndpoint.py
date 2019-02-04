import datetime

import flask_restful
from flask import request, g

from app import RestException, db, auth
from app.model.participant import Participant
from app.resources.schema import ParticipantSchema
from app.wrappers import requires_roles


class ParticipantEndpoint(flask_restful.Resource):

    schema = ParticipantSchema()

    @auth.login_required
    def get(self, id):
        model = db.session.query(Participant).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        if not model and (g.user.related_to_participant(model.id) and not g.user.role == 'Admin'):
            raise RestException(RestException.UNRELATED_PARTICIPANT)
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_roles('Admin')
    def delete(self, id):
        db.session.query(Participant).filter_by(id=id).delete()
        db.session.commit()
        return None

    @auth.login_required
    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Participant).filter_by(id=id).first()
        if not g.user.related_to_participant(instance.id) and not g.user.role == 'Admin':
            raise RestException(RestException.UNRELATED_PARTICIPANT)
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)



