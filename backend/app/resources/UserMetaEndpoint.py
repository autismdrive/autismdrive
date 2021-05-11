import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError
from sqlalchemy import exc

from app.schema.schema import UserMetaSchema
from app import RestException, db, elastic_index, auth, app
from app.model.user_meta import UserMeta


class UserMetaEndpoint(flask_restful.Resource):
    schema = UserMetaSchema()

    @auth.login_required
    def get(self, id):
        model = db.session.query(UserMeta).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    def delete(self, id):
        db.session.query(UserMeta).filter_by(id=id).delete()
        return None

    @auth.login_required
    def post(self, id):
        request_data = request.get_json()
        instance = db.session.query(UserMeta).filter(UserMeta.id == id).first()

        try:
            updated = self.schema.load(request_data, instance=instance)
        except Exception as errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)

        updated.last_updated = datetime.datetime.utcnow()
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)

