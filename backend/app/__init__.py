from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import click
from flask_marshmallow import Marshmallow

from app.rest_exception import RestException

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')
# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Database Configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Marshmallow provides HATEOAS links
ma = Marshmallow(app)

# Database Migrations
migrate = Migrate(app, db)

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
    data_loader.load_resources()
    data_loader.load_studies()
    data_loader.load_trainings()
    data_loader.load_users()


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
