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
                with open(settings.JWT.public_key_path, "rb") as key_file:
                    public_key = key_file.read()
                    payload = jwt.decode(
                        jwt=auth_token,
                        key=public_key,
                        algorithms=[settings.JWT.algorithm],
                    )
                    return payload["exp"]
            except Exception:
                return 0
        else:
            return 0
