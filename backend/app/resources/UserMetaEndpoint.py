import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError
from sqlalchemy import exc, cast, Integer

from app.auth import auth
from app.database import session
from app.models import UserMeta
from app.rest_exception import RestException
from app.schemas import UserMetaSchema


class UserMetaEndpoint(flask_restful.Resource):
    schema = UserMetaSchema()

    @auth.login_required
    def get(self, id):
        model = session.query(UserMeta).filter_by(id=cast(id, Integer)).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    def delete(self, id):
        session.query(UserMeta).filter_by(id=cast(id, Integer)).delete()
        return None

    @auth.login_required
    def post(self, id):
        request_data = request.get_json()

        try:
            existing = session.query(UserMeta).filter(UserMeta.id == cast(id, Integer)).first()
            new_meta = self.schema.load(request_data, instance=existing)
            new_meta.last_updated = datetime.datetime.utcnow()
            session.add(new_meta)
            session.commit()
            return self.schema.dump(new_meta)
        except (ValidationError, exc.IntegrityError) as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)
