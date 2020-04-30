import flask_restful
from flask import request

from app import db, RestException, auth
from app.model.user import User
from app.model.role import Role
from app.model.user_favorite import UserFavorite
from app.schema.schema import UserFavoriteSchema
from app.wrappers import requires_roles


class FavoritesByUserEndpoint(flask_restful.Resource):

    schema = UserFavoriteSchema()

    @auth.login_required
    def get(self, user_id):
        user_favorites = db.session.query(UserFavorite)\
            .filter(UserFavorite.user_id == user_id)\
            .all()
        return self.schema.dump(user_favorites, many=True)


class FavoritesByUserAndTypeEndpoint(flask_restful.Resource):

    schema = UserFavoriteSchema()

    @auth.login_required
    def get(self, user_id, favorite_type):
        user_favorites = db.session.query(UserFavorite)\
            .filter(UserFavorite.user_id == user_id)\
            .filter(UserFavorite.type == favorite_type)\
            .all()
        return self.schema.dump(user_favorites, many=True)


class UserFavoriteEndpoint(flask_restful.Resource):
    schema = UserFavoriteSchema()

    @auth.login_required
    def get(self, id):
        model = db.session.query(UserFavorite).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    def delete(self, id):
        db.session.query(UserFavorite).filter_by(id=id).delete()
        db.session.commit()
        return None


class UserFavoriteListEndpoint(flask_restful.Resource):
    schema = UserFavoriteSchema(many=True)

    @auth.login_required
    def get(self):
        resources = db.session.query(UserFavorite).all()
        return self.schema.dump(resources)

    @auth.login_required
    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data, many=True).data
        db.session.add_all(load_result)
        db.session.commit()
        return self.schema.dump(load_result)
