import flask_restful
from flask import g, jsonify

from app.auth import auth
from app.schemas import SchemaRegistry


class SessionEndpoint(flask_restful.Resource):
    """Provides a way to get the current user, and to delete the user."""

    schema = SchemaRegistry.UserSchema()

    @auth.login_required
    def get(self):
        if "user" in g:
            return jsonify(self.schema.dump(g.user))
        else:
            return None

    @staticmethod
    def delete():
        if "user" in g:
            g.user = None
        else:
            return None
