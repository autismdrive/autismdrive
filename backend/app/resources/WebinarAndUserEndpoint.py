import flask_restful
from flask import request

from app import db, RestException
from app.model.user import User
from app.model.webinar import Webinar
from app.model.webinar_user import WebinarUser
from app.schema.schema import WebinarUserSchema


class WebinarByUserEndpoint(flask_restful.Resource):

    schema = WebinarUserSchema()

    def get(self, user_id):
        webinar_users = db.session.query(WebinarUser)\
            .join(WebinarUser.webinar)\
            .filter(WebinarUser.user_id == user_id)\
            .order_by(Webinar.title)\
            .all()
        return self.schema.dump(webinar_users, many=True)


class UserByWebinarEndpoint(flask_restful.Resource):

    schema = WebinarUserSchema()

    def get(self, webinar_id):
        webinar_users = db.session.query(WebinarUser).\
            join(WebinarUser.user).\
            filter(WebinarUser.webinar_id == webinar_id).\
            order_by(User.name).\
            all()
        return self.schema.dump(webinar_users,many=True)


class WebinarUserEndpoint(flask_restful.Resource):
    schema = WebinarUserSchema()

    def get(self, id):
        model = db.session.query(WebinarUser).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        db.session.query(WebinarUser).filter_by(id=id).delete()
        db.session.commit()
        return None


class WebinarUserListEndpoint(flask_restful.Resource):
    schema = WebinarUserSchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data).data
        db.session.query(WebinarUser).filter_by(webinar_id=load_result.webinar_id,
                                                     user_id=load_result.user_id).delete()
        db.session.add(load_result)
        db.session.commit()
        return self.schema.dump(load_result)
