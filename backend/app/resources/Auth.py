# Login
# *****************************
from functools import wraps
import datetime

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy import func
from app import app, RestException, db, auth, email_service
from app.model.email_log import EmailLog
from app.model.user import User
from flask import g, request, Blueprint, jsonify

from app.schema.schema import UserSchema

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api')


def confirm_email(email_token):
    """When users create a new account with an email and a password, this
    allows the front end to confirm their email and log them into the system."""
    try:
        ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        email = ts.loads(email_token, salt="email-confirm-key", max_age=86400)
    except:
        raise RestException(RestException.EMAIL_TOKEN_INVALID)

    user = User.query.filter_by(email=email).first_or_404()
    user.email_verified = True
    db.session.add(user)
    db.session.commit()

    auth_token = user.encode_auth_token().decode()
    user.token = auth_token
    return user


@auth_blueprint.route('/login_password', methods=["GET", "POST"])
def login_password():
    request_data = request.get_json()
    email = request_data['email']
    user = User.query.filter(func.lower(User.email) == email.lower()).first()
    schema = UserSchema(many=False)

    if user is None:
        raise RestException(RestException.LOGIN_FAILURE)
    if user.email_verified:
        if user.is_correct_password(request_data["password"]):
            # redirect users back to the front end, include the new auth token.
            auth_token = user.encode_auth_token().decode()
            g.user = user
            user.token = auth_token
            user.last_login = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            return schema.jsonify(user)
        else:
            raise RestException(RestException.LOGIN_FAILURE)
    else:
        if 'email_token' in request_data:
            g.user = confirm_email(request_data['email_token'])
            return schema.jsonify(user)
        else:
            raise RestException(RestException.CONFIRM_EMAIL)


@auth_blueprint.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    request_data = request.get_json()
    email = request_data['email']
    user = User.query.filter(func.lower(User.email) == email.lower()).first()

    if user:
        tracking_code = email_service.reset_email(user)

        log = EmailLog(user_id=user.id, type="reset_email", tracking_code=tracking_code)
        db.session.add(log)
        db.session.commit()

        if (app.config.get('TESTING') or app.config.get('DEVELOPMENT')) and user.token_url:
            return jsonify(user.token_url)
        else:
            return ''
    else:
        raise RestException(RestException.EMAIL_NOT_REGISTERED)


@auth_blueprint.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    request_data = request.get_json()
    password = request_data['password']
    email_token = request_data['email_token']
    try:
        ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        email = ts.loads(email_token, salt="email-reset-key", max_age=86400) #24 hours
    except SignatureExpired:
        raise RestException(RestException.TOKEN_EXPIRED)
    except BadSignature:
        raise RestException(RestException.TOKEN_INVALID)

    user = User.query.filter(func.lower(User.email) == email.lower()).first_or_404()
    user.token_url = ''
    user.email_verified = True
    user.password = password
    user.last_login = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token().decode()
    user.token = auth_token
    return UserSchema().jsonify(user)


@auth.verify_token
def verify_token(token):
    try:
        resp = User.decode_auth_token(token)
        if resp:
            g.user = User.query.filter_by(id=resp).first()
    except:
        g.user = None

    if 'user' in g and g.user:
        g.user.token_url = ''
        return True
    else:
        return False


def login_optional(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method != 'OPTIONS':  # pragma: no cover
            try:
                auth = verify_token(request.headers['AUTHORIZATION'].split(' ')[1])
            except:
                auth = False

        return f(*args, **kwargs)

    return decorated
