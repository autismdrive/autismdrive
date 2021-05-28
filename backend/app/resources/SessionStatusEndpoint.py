import datetime
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
import flask_restful
from flask import g, jsonify, request
import jwt
from app import app, auth


class SessionStatusEndpoint(flask_restful.Resource):
    """
    Returns the timecode (in seconds) when the current session expires,
    or 0 if there is no current session.
    """

    @auth.login_required
    def get(self):
        # We don't need to send in the auth token as an argument, it is in the
        # header.
        auth_token = request.headers['AUTHORIZATION'].split(' ')[1];
        if "user" in g and auth_token:
            try:
                payload = jwt.decode(
                    auth_token,
                    app.config.get('SECRET_KEY'),
                    algorithms='HS256')
                return payload['exp']
            except Exception as e:
                return 0
        else:
            return 0
