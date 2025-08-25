import flask
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPTokenAuth
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import scoped_session

from app.elastic_index import ElasticIndex
from app.email_service import EmailService
from config.base import Settings


class APIApp(flask.Flask):
    session: scoped_session
    ma: Marshmallow
    auth: HTTPTokenAuth
    bcrypt: Bcrypt
    email_service: EmailService
    password_requirements: dict
    elastic_index: ElasticIndex
    schedule_tasks: callable
    settings: Settings
