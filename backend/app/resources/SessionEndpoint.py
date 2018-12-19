import flask_restful
from flask import g, jsonify

from app import auth
from app.resources.schema import UserSchema


class SessionEndpoint(flask_restful.Resource):
    """Provides a way to get the current user, and to delete the user."""
    schema = UserSchema()

    @auth.login_required
    def get(self):
        return jsonify(self.schema.dump(g.user).data)

    @staticmethod
    @auth.login_required
    def delete():
        if "user" in g:
            g.user = None
        return None



