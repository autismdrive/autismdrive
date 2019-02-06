from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
import click
import os
from flask_marshmallow import Marshmallow

from app.email_service import EmailService
from app.rest_exception import RestException

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')
# Load the configuration from the instance folder
app.config.from_pyfile('config.py')
# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
if "APP_CONFIG_FILE" in os.environ:
    app.config.from_envvar('APP_CONFIG_FILE')

# Database Configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Enable CORS
if(app.config["CORS_ENABLED"]) :
    cors = CORS(app, resources={r"*": {"origins": "*"}})

# Flask-Marshmallow provides HATEOAS links
ma = Marshmallow(app)

# Database Migrations
migrate = Migrate(app, db, compare_type=True)

# email service
email_service = EmailService(app)

# Token Authentication
auth = HTTPTokenAuth('Bearer')

# Password Encryption
bcrypt = Bcrypt(app)

# Constructing for a problem when building urls when the id is null.
# there is a fix in the works for this, see
# https://github.com/kids-first/kf-api-dathanaservice/pull/219
# handler = lambda error, endpoint, values: ''


def handler(error, endpoint, values=''):
    print("URL Build error:" + str(error))
    return ''
app.url_build_error_handlers.append(handler)


# Handle errors consistently
@app.errorhandler(RestException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def handle_404(error):
    return handle_invalid_usage(RestException(RestException.NOT_FOUND, 404))


def _load_data(data_loader):
    data_loader.load_categories()
    data_loader.load_resources()
    data_loader.load_studies()
    data_loader.load_trainings()
    data_loader.load_users()
    data_loader.load_participants()
    data_loader.link_users_participants()
    data_loader.load_clinical_diagnoses_questionnaire()
    data_loader.load_contact_questionnaire()
    data_loader.load_current_behaviors_questionnaire()
    data_loader.load_demographics_questionnaire()
    data_loader.load_developmental_questionnaire()
    data_loader.load_education_questionnaire()
    data_loader.load_employment_questionnaire()
    data_loader.load_evaluation_history_questionnaire()
    data_loader.load_home_questionnaire()
    data_loader.load_identification_questionnaire()
    data_loader.load_supports_questionnaire()


@app.cli.command()
def initdb():
    """Initialize the database."""
    from app import data_loader
    data_loader = data_loader.DataLoader()
    _load_data(data_loader)


@app.cli.command()
def cleardb():
    """Delete all information from the database."""
    click.echo('Clearing out the database')
    from app import data_loader
    data_loader = data_loader.DataLoader()
    data_loader.clear()


@app.cli.command()
def reset():
    """Remove all data and recreate it from the example data files"""
    click.echo('Rebuilding the databases from the example data files')
    from app import data_loader
    data_loader = data_loader.DataLoader()
    data_loader.clear()
    _load_data(data_loader)


from app import views
