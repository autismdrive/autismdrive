# Login
# *****************************
import datetime
from functools import wraps

from flask import g, request, Blueprint, jsonify
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy import func, select, update
from sqlalchemy.orm import joinedload

from app.auth import auth
from app.database import session
from app.email_service import email_service
from app.rest_exception import RestException
from app.schemas import SchemaRegistry
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

    user = (
        session.execute(select(User).options(joinedload(User.participants)).filter_by(email=email))
        .unique()
        .scalar_one_or_none()
    )

    if user is None:
        raise RestException(RestException.EMAIL_NOT_REGISTERED)

    user_id = user.id
    user.email_verified = True
    session.add(user)
    session.commit()
    session.close()

    user_to_update = (
        session.execute(select(User).options(joinedload(User.participants)).filter_by(id=user_id))
        .unique()
        .scalar_one_or_none()
    )

    user_to_update.token = User.encode_auth_token(user_id=user_id)
    user_to_update.last_login = datetime.datetime.utcnow()
    session.add(user_to_update)
    session.commit()
    session.close()

    db_user = (
        session.execute(select(User).options(joinedload(User.participants)).filter_by(email=email))
        .unique()
        .scalar_one_or_none()
    )
    session.close()
    return db_user


@auth_blueprint.route("/login_password", methods=["GET", "POST"])
def login_password():
    from app.models import User

    request_data = request.get_json()

    if request_data is None:
        raise RestException(RestException.INVALID_INPUT)

    email = request_data["email"].lower()
    db_user = (
        session.execute(select(User).options(joinedload(User.participants)).filter_by(email=email))
        .unique()
        .scalar_one_or_none()
    )
    schema = SchemaRegistry.UserSchema(many=False)

    if db_user is None:
        raise RestException(RestException.LOGIN_FAILURE)
    if db_user.email_verified:
        user_id = db_user.id

        if User.is_correct_password(user_id=user_id, plaintext=request_data["password"]):
            # redirect users back to the front end, include the new auth token.
            user_to_update = (
                session.execute(select(User).options(joinedload(User.participants)).filter_by(email=email))
                .unique()
                .scalar_one_or_none()
            )
            user_to_update.token = User.encode_auth_token(user_id=user_id)
            user_to_update.last_login = datetime.datetime.utcnow()
            session.add(user_to_update)
            session.commit()
            session.close()

            updated_user = (
                session.execute(select(User).options(joinedload(User.participants)).filter_by(email=email))
                .unique()
                .scalar_one_or_none()
            )
            session.close()

            g.user = updated_user
            return jsonify(schema.dump(updated_user))
        else:
            raise RestException(RestException.LOGIN_FAILURE)
    else:
        if "email_token" in request_data:
            updated_user = confirm_email(request_data["email_token"])
            g.user = updated_user
            return jsonify(schema.dump(updated_user))
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
        email = ts.loads(email_token, salt="email-reset-key", max_age=86400).lower()  # 24 hours
    except SignatureExpired:
        raise RestException(RestException.TOKEN_EXPIRED)
    except BadSignature:
        raise RestException(RestException.TOKEN_INVALID)

    user = session.execute(select(User).filter_by(email=email)).unique().scalar_one_or_none()

    if user is None:
        raise RestException(RestException.EMAIL_NOT_REGISTERED)

    user_id = user.id
    session.close()

    user_to_update = session.execute(select(User).filter_by(id=user_id)).unique().scalar_one()
    user_to_update.token_url = ""
    user_to_update.email_verified = True
    user_to_update.password = password
    user_to_update.token = User.encode_auth_token(user_id=user_id)
    user_to_update.last_login = datetime.datetime.utcnow()
    session.add(user_to_update)
    session.commit()
    session.close()

    db_user = (
        session.execute(select(User).options(joinedload(User.participants)).filter_by(id=user_id)).unique().scalar_one()
    )
    return jsonify(SchemaRegistry.UserSchema().dump(user))


@auth.verify_token
def verify_token(token):
    from app.models import User

    user_id = None
    try:
        user_id = User.decode_auth_token(token)
    except:
        g.user = None

    if user_id is not None:
        db_user = (
            session.execute(select(User).options(joinedload(User.participants)).filter_by(id=user_id))
            .unique()
            .scalar_one()
        )
        db_user.token_url = ""
        session.add(db_user)
        session.commit()
        session.close()
        g.user = db_user

    return "user" in g and g.user


def login_optional(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method != "OPTIONS":  # pragma: no cover
            verify_token(request.headers["AUTHORIZATION"].split(" ")[1])

        return f(*args, **kwargs)

    return decorated
