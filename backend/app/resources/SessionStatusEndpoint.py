import jwt
from flask import g, request
from flask.views import MethodView

from app.auth import auth
from config.load import settings


class SessionStatusEndpoint(MethodView):
    """
    Returns the timecode (in seconds) when the current session expires,
    or 0 if there is no current session.
    """

    @auth.login_required
    def get(self):
        # We don't need to send in the auth token as an argument, it is in the
        # header.
        auth_token = request.headers["AUTHORIZATION"].split(" ")[1]
        if "user" in g and auth_token:
            try:
                payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms="HS256")
                return payload["exp"]
            except Exception:
                return 0
        else:
            return 0
