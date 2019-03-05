import datetime

import flask_restful
from flask import request, g
from marshmallow import ValidationError
from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError

from app import RestException, db, email_service, auth
from app.model.email_log import EmailLog
from app.model.user import User, Role
from app.resources.schema import UserSchema
from app.wrappers import requires_roles


class UserEndpoint(flask_restful.Resource):

    schema = UserSchema()

    @auth.login_required
    def get(self, id):
        if g.user.id != eval(id) and g.user.role != Role.admin:
            raise RestException(RestException.PERMISSION_DENIED)
        model = db.session.query(User).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_roles(Role.admin)
    def delete(self, id):
        db.session.query(User).filter_by(id=id).delete()
        db.session.commit()
        return None

    @auth.login_required
    def put(self, id):
        if g.user.id != eval(id) and g.user.role != Role.admin:
            raise RestException(RestException.PERMISSION_DENIED)
        request_data = request.get_json()
        if 'role' in request_data and request_data['role'] == 'admin' and g.user.role == Role.admin:
            request_data['role'] = 'admin'
        else:
            request_data['role'] = 'user'
        instance = db.session.query(User).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)


class UserListEndpoint(flask_restful.Resource):

    usersSchema = UserSchema(many=True)
    userSchema = UserSchema()

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        users = db.session.query(User).all()
        return self.usersSchema.dump(users)

    def post(self):
        request_data = request.get_json()
        try:
            request_data['role'] = 'user'
            new_user, errors = self.userSchema.load(request_data)
            if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
            email_exists = db.session.query(exists().where(User.email == new_user.email)).scalar()
            if email_exists:
                raise RestException(RestException.EMAIL_EXISTS)
            db.session.add(new_user)
            db.session.commit()
            self.send_confirm_email(new_user)
            return self.userSchema.dump(new_user)
        except IntegrityError as ie:
            raise RestException(RestException.INVALID_OBJECT)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=new_user.errors)

    def send_confirm_email(self, user):
        tracking_code = email_service.confirm_email(user)
        log = EmailLog(user_id=user.id, type="confirm_email", tracking_code=tracking_code)
        db.session.add(log)
        db.session.commit()
