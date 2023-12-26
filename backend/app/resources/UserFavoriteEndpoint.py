import flask_restful
from flask import request
from sqlalchemy import cast, Integer

from app.auth import auth
from app.database import session
from app.models import UserFavorite
from app.rest_exception import RestException
from app.schemas import UserFavoriteSchema


class FavoritesByUserEndpoint(flask_restful.Resource):

    schema = UserFavoriteSchema()

    @auth.login_required
    def get(self, user_id):
        user_favorites = session.query(UserFavorite).filter(UserFavorite.user_id == cast(user_id, Integer)).all()
        return self.schema.dump(user_favorites, many=True)


class FavoritesByUserAndTypeEndpoint(flask_restful.Resource):

    schema = UserFavoriteSchema()

    @auth.login_required
    def get(self, user_id, favorite_type):
        user_favorites = (
            session.query(UserFavorite)
            .filter(UserFavorite.user_id == cast(user_id, Integer))
            .filter(UserFavorite.type == favorite_type)
            .all()
        )
        return self.schema.dump(user_favorites, many=True)


class UserFavoriteEndpoint(flask_restful.Resource):
    schema = UserFavoriteSchema()

    @auth.login_required
    def get(self, id):
        model = session.query(UserFavorite).filter_by(id=cast(id, Integer)).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    def delete(self, id):
        session.query(UserFavorite).filter_by(id=cast(id, Integer)).delete()
        session.commit()
        return None


class UserFavoriteListEndpoint(flask_restful.Resource):
    schema = UserFavoriteSchema(many=True)

    @auth.login_required
    def get(self):
        resources = session.query(UserFavorite).all()
        return self.schema.dump(resources)

    @auth.login_required
    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data, many=True)
        if load_result[0].type != "resource":
            session.query(UserFavorite).filter_by(user_id=load_result[0].user_id, resource_id=None).delete()
        session.add_all(load_result)
        session.commit()
        return self.schema.dump(load_result)
