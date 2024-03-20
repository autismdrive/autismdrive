import flask_restful
from flask import g, jsonify

from app.auth import auth
from app.schemas import SchemaRegistry


class SessionEndpoint(flask_restful.Resource):
    """Provides a way to get the current user, and to delete the user."""

    schema = SchemaRegistry.UserSchema()

    @auth.login_required
    def get(self):
        if "user" in g and g.user.id is not None:
            from app.resources.UserEndpoint import get_user_by_id

            db_user = get_user_by_id(g.user.id)
            return jsonify(self.schema.dump(db_user))
        else:
            return None

    @staticmethod
    def delete():
        if "user" in g:
            g.user = None
        else:
            return None
