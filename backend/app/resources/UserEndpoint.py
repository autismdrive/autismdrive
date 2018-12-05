import flask_restful
from flask import request
from marshmallow import ValidationError
from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError

from app import RestException, db
from app.model.user import User
from app.resources.schema import UserSchema


class UserEndpoint(flask_restful.Resource):

    schema = UserSchema()

    def get(self, id):
        model = db.session.query(User).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        db.session.query(User).filter_by(id=id).delete()
        db.session.commit()
        return None

    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(User).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)


class UserListEndpoint(flask_restful.Resource):

    usersSchema = UserSchema(many=True)
    userSchema = UserSchema()

    def get(self):
        users = db.session.query(User).all()
        return self.usersSchema.dump(users)

    def post(self):
        request_data = request.get_json()
        try:
            new_user, errors = self.userSchema.load(request_data)
            if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
            email_exists = db.session.query(exists().where(User.email == new_user.email)).scalar()
            if email_exists:
                raise RestException(RestException.EMAIL_EXISTS)
            db.session.add(new_user)
            db.session.commit()
            return self.userSchema.dump(new_user)
        except IntegrityError as ie:
            raise RestException(RestException.INVALID_OBJECT)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=new_user.errors)
