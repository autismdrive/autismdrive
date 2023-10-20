# Login
# *****************************
from functools import wraps
import datetime

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy import func

from app.auth import auth
from app.database import session
from app.email_service import email_service
from flask import g, request, Blueprint, jsonify

from app.rest_exception import RestException
from app.schemas import UserSchema
from config.load import settings

auth_blueprint = Blueprint("auth", __name__, url_prefix="/api")


def confirm_email(email_token):
    """When users create a new account with an email and a password, this
    allows the front end to confirm their email and log them into the system."""
    from app.models import User

    try:
        ts = URLSafeTimedSerializer(settings.SECRET_KEY)
        email = ts.loads(email_token, salt="email-confirm-key", max_age=86400)
    except:
        raise RestException(RestException.EMAIL_TOKEN_INVALID)

    user = session.query(User).filter_by(email=email).first_or_404()
    user.email_verified = True
    session.add(user)
    session.commit()

    auth_token = user.encode_auth_token()
    user.token = auth_token
    return user


@auth_blueprint.route("/login_password", methods=["GET", "POST"])
def login_password():
    from app.models import User

    request_data = request.get_json()

    if request_data is None:
        raise RestException(RestException.INVALID_INPUT)

    email = request_data["email"]
    user = session.query(User).filter(func.lower(User.email) == email.lower()).first()
    schema = UserSchema(many=False)

    if user is None:
        raise RestException(RestException.LOGIN_FAILURE)
    if user.email_verified:
        if user.is_correct_password(request_data["password"]):
            # redirect users back to the front end, include the new auth token.
            auth_token = user.encode_auth_token()
            g.user = user
            user.token = auth_token
            user.last_login = datetime.datetime.utcnow()
            session.add(user)
            session.commit()
            return schema.jsonify(user)
        else:
            raise RestException(RestException.LOGIN_FAILURE)
    else:
        if "email_token" in request_data:
            g.user = confirm_email(request_data["email_token"])
            return schema.jsonify(user)
        else:
            raise RestException(RestException.CONFIRM_EMAIL)


@auth_blueprint.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    from app.models import User
    from app.models import EmailLog

    request_data = request.get_json()
    email = request_data["email"]
    user = session.query(User).filter(func.lower(User.email) == func.lower(email)).first()

    if user:
        tracking_code = email_service.reset_email(user)

        log = EmailLog(user_id=user.id, type="reset_email", tracking_code=tracking_code)
        session.add(log)
        session.commit()

        if (settings.TESTING or settings.DEVELOPMENT) and user.token_url:
            return jsonify(user.token_url)
        else:
            return ""
    else:
        raise RestException(RestException.EMAIL_NOT_REGISTERED)


@auth_blueprint.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    from app.models import User

    request_data = request.get_json()
    password = request_data["password"]
    email_token = request_data["email_token"]
    try:
        ts = URLSafeTimedSerializer(settings.SECRET_KEY)
        email = ts.loads(email_token, salt="email-reset-key", max_age=86400)  # 24 hours
    except SignatureExpired:
        raise RestException(RestException.TOKEN_EXPIRED)
    except BadSignature:
        raise RestException(RestException.TOKEN_INVALID)

    user = session.query(User).filter(func.lower(User.email) == email.lower()).first_or_404()
    user.token_url = ""
    user.email_verified = True
    user.password = password
    user.last_login = datetime.datetime.utcnow()
    session.add(user)
    session.commit()
    auth_token = user.encode_auth_token()
    user.token = auth_token
    return UserSchema().jsonify(user)


@auth.verify_token
def verify_token(token):
    from app.models import User

    try:
        resp = User.decode_auth_token(token)
        if resp:
            g.user = session.query(User).filter_by(id=resp).first()
    except:
        g.user = None

    if "user" in g and g.user:
        g.user.token_url = ""
        return True
    else:
        return False


def login_optional(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method != "OPTIONS":  # pragma: no cover
            try:
                auth = verify_token(request.headers["AUTHORIZATION"].split(" ")[1])
            except:
                auth = False

        return f(*args, **kwargs)

    return decorated
