import flask
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPTokenAuth
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session

from app.elastic_index import ElasticIndex
from app.email_service import EmailService


class APIApp(flask.Flask):
    db: SQLAlchemy
    session: scoped_session
    ma: Marshmallow
    migrate: Migrate
    auth: HTTPTokenAuth
    bcrypt: Bcrypt
    email_service: EmailService
    password_requirements: dict
    elastic_index: ElasticIndex
