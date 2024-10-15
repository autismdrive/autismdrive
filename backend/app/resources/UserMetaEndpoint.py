import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError
from sqlalchemy import exc

from app.auth import auth
from app.database import session
from app.models import UserMeta
from app.rest_exception import RestException
from app.schemas import SchemaRegistry


class UserMetaEndpoint(flask_restful.Resource):
    schema = SchemaRegistry.UserMetaSchema()

    @auth.login_required
    def get(self, user_id: int):
        model = session.query(UserMeta).filter_by(id=user_id).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    def delete(self, user_id: int):
        session.query(UserMeta).filter_by(id=user_id).delete()
        return None

    @auth.login_required
    def post(self, user_id: int):
        request_data = request.get_json()

        try:
            existing = session.query(UserMeta).filter(UserMeta.id == user_id).first()
            new_meta = self.schema.load(request_data, instance=existing)
            new_meta.last_updated = datetime.datetime.utcnow()
            session.add(new_meta)
            session.commit()
            return self.schema.dump(new_meta)
        except (ValidationError, exc.IntegrityError) as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)
