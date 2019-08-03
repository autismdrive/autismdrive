
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
import click
import os
from flask_marshmallow import Marshmallow

from app.elastic_index import ElasticIndex
from app.email_service import EmailService
from app.rest_exception import RestException

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')
# Load the configuration from the instance folder
app.config.from_pyfile('config.py')
# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
if "TESTING" in os.environ and os.environ["TESTING"] == "true":
    app.config.from_object('config.testing')
    app.config.from_pyfile('testing.py')

if "MIRRORING" in os.environ and os.environ["MIRRORING"] == "true":
    app.config.from_object('config.mirror')


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

# Search System
elastic_index = ElasticIndex(app)

#
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
    data_loader.load_events()
    data_loader.load_locations()
    data_loader.load_resources()
    data_loader.load_studies()
    data_loader.load_users()
    data_loader.load_participants()


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
def initindex():
    """Delete all information from the elastic search Index."""
    click.echo('Loading data into Elastic Search')
    from app import data_loader
    data_loader = data_loader.DataLoader()
    data_loader.build_index()


@app.cli.command()
def clearindex():
    """Delete all information from the elasticsearch index"""
    click.echo('Removing Data from Elastic Search')
    from app import data_loader
    data_loader = data_loader.DataLoader()
    data_loader.clear_index()


@app.cli.command()
def reset():
    """Remove all data and recreate it from the example data files"""
    click.echo('Rebuilding the databases from the example data files')
    from app import data_loader
    data_loader = data_loader.DataLoader()
    data_loader.clear_index()
    data_loader.clear()
    _load_data(data_loader)
    data_loader.build_index()


@app.cli.command()
def resourcereset():
    """Remove all data about resources, studies, and trainings, and recreate it from the example data files"""
    click.echo('Re-populating resources, studies, and trainings from the example data files')
    from app import data_loader
    data_loader = data_loader.DataLoader()
    data_loader.clear_index()
    data_loader.clear_resources()
    data_loader.load_categories()
    data_loader.load_events()
    data_loader.load_locations()
    data_loader.load_resources()
    data_loader.load_studies()
    data_loader.build_index()


@app.cli.command()
def run_full_export():
    """Remove all data and recreate it from the example data files"""
    if app.config["MIRRORING"]:
        click.echo('Exporting all data.')
        from app.import_service import ImportService
        importer = ImportService(app, db)
        importer.run_full_backup()
    else:
        click.echo('This system is not configured to run exports. Ingoring.')



from app import views

# Cron scheduler
if app.config["MIRRORING"]:
    from app.import_service import ImportService
    importer = ImportService(app, db)
    importer.start()
else:
    from app.export_service import ExportService
    ExportService.start()