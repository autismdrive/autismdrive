import logging.config
from urllib.parse import unquote

import click
from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify, url_for, Blueprint
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful.reqparse import RequestParser

from app.api_app import APIApp
from app.data_loader import data_loader
from app.elastic_index import elastic_index
from app.email_prompt_service import EmailPromptService
from app.email_service import EmailService
from app.resources.Auth import auth_blueprint
from app.resources.Tracking import tracking_blueprint
from app.rest_exception import RestException
from app.views import StarDriveApi, endpoints
from config.logging import logging_config


def create_app(settings=None):
    from config.load import settings as loaded_settings

    settings = loaded_settings if settings is None else settings

    logging.config.dictConfig(logging_config)

    _app = APIApp(__name__, instance_relative_config=True)

    _app.config.from_object(settings)

    # Database Configuration
    from app.database import db

    _app.db = db
    _app.db.init_app(_app)
    _app.session = _app.db.session

    # Enable CORS
    if settings.CORS_ENABLED:
        # Convert list of allowed origins to list of regexes
        origins_re = [r"^https?:\/\/%s(.*)" % o.replace(".", "\.") for o in settings.CORS_ALLOW_ORIGINS]
        cors = CORS(_app, origins=origins_re)

    # Flask-Marshmallow provides HATEOAS links
    from app.schema.ma import ma

    _app.ma = ma
    _app.ma.init_app(_app)
    _app.ma.SQLAlchemySchema.OPTIONS_CLASS.session = _app.db.session
    _app.ma.SQLAlchemyAutoSchema.OPTIONS_CLASS.session = _app.db.session

    # Database Migrations
    _app.migrate = Migrate(_app, _app.db, compare_type=True)

    # email service
    _app.email_service = EmailService()

    # Token Authentication
    from app.auth import auth, bcrypt, password_requirements

    _app.auth = auth

    # Password Encryption
    bcrypt.init_app(_app)
    _app.bcrypt = bcrypt

    # Password Requirements
    _app.password_requirements = password_requirements

    # Search System
    _app.elastic_index = elastic_index

    @_app.errorhandler(Exception)
    def handle_exception(e):
        from traceback_with_variables import iter_exc_lines

        _app.logger.error("\n".join(iter_exc_lines(e)))
        return "Server Error", 500

    # Handle errors consistently
    @_app.errorhandler(RestException)
    def handle_invalid_usage(error):
        error_dict = {}
        if hasattr(error, "to_dict"):
            error_dict = error.to_dict()
        elif hasattr(error, "__dict__"):
            error_dict = error.__dict__

        if "details" in error_dict:
            details = error_dict["details"]
            if hasattr(details, "to_dict"):
                error_dict["details"] = details.to_dict()
            elif hasattr(details, "__dict__"):
                error_dict["details"] = details.__dict__

        response = jsonify(error_dict)
        response.status_code = error.status_code
        return response

    @_app.errorhandler(404)
    def handle_404(error):
        return handle_invalid_usage(RestException(RestException.NOT_FOUND, 404))

    def _load_data():
        data_loader.load_users()
        data_loader.load_participants()
        data_loader.load_categories()
        data_loader.load_events()
        data_loader.load_locations()
        data_loader.load_resources()
        data_loader.load_studies()
        data_loader.load_zip_codes()
        data_loader.load_chain_steps()

    @_app.cli.command()
    def initdb():
        """Initialize the database."""

        _load_data()

    @_app.cli.command()
    def cleardb():
        """Delete all information from the database."""
        click.echo("Clearing out the database")

        data_loader.clear()

    @_app.cli.command()
    def initindex():
        """Delete all information from the elastic search Index."""
        click.echo("Loading data into Elastic Search")
        _app.elastic_index.clear()
        data_loader.build_index()

    @_app.cli.command()
    def clearindex():
        """Delete all information from the elasticsearch index"""
        click.echo("Removing Data from Elastic Search")
        data_loader.clear_index()

    @_app.cli.command()
    def reset():
        """Remove all data and recreate it from the example data files"""
        click.echo("Rebuilding the databases from the example data files")
        data_loader.clear_index()
        data_loader.clear()
        _load_data()
        data_loader.build_index()

    @_app.cli.command()
    def resourcereset():
        """Used for Staging updates where we don't want to do a full reset and wipe away all user data.
        Does not clear and rebuild index because that is a separate step of the prod update.
        Remove all data about resources, studies, and trainings, and recreate it from the example data files"""
        click.echo("Re-populating resources, studies, and trainings from the example data files")

        data_loader.clear_resources()
        data_loader.load_categories()
        data_loader.load_events()
        data_loader.load_locations()
        data_loader.load_resources()
        data_loader.load_studies()
        data_loader.load_zip_codes()
        data_loader.load_chain_steps()

    @_app.cli.command()
    def loadstudies():
        """Used for loading new studies into the database"""
        click.echo("Loading additional studies, not clearing out existing ones")

        data_loader.load_studies()

    @_app.cli.command()
    def loadusers():
        """Used for loading new users into the database"""
        click.echo("Loading users, not clearing out existing ones")

        data_loader.load_users()

    @_app.cli.command()
    def loadparticipants():
        """Used for loading new participants into the database"""
        click.echo("Loading participants, not clearing out existing ones")

        data_loader.load_participants()

    @_app.cli.command()
    def run_full_export():
        """Remove all data and recreate it from the example data files"""
        if settings.MIRRORING:
            from app.import_service import ImportService

            click.echo("Exporting all data.")
            import_service = ImportService()
            import_service.run_full_backup()
        else:
            click.echo("This system is not configured to run exports. Ingoring.")

    def schedule_tasks():
        from app.model.user import User
        from app.model.study import Study
        from app.model.email_log import EmailLog
        from app.export_service import ExportService
        from app.import_service import ImportService

        scheduler = BackgroundScheduler(daemon=True)
        scheduler.start()
        if settings.MIRRORING:
            import_service = ImportService()
            scheduler.add_job(import_service.run_backup, "interval", minutes=import_service.import_interval_minutes)
            scheduler.add_job(import_service.run_full_backup, "interval", days=1)
        else:
            email_prompt_service = EmailPromptService(EmailLog, Study, User)
            scheduler.add_job(
                ExportService.send_alert_if_exports_not_running,
                "interval",
                minutes=settings.EXPORT_CHECK_INTERNAL_MINUTES,
            )
            scheduler.add_job(
                email_prompt_service.send_confirm_prompting_emails,
                "interval",
                days=1,
            )
            scheduler.add_job(
                email_prompt_service.send_complete_registration_prompting_emails,
                "interval",
                days=1,
            )
            scheduler.add_job(
                email_prompt_service.send_dependent_profile_prompting_emails,
                "interval",
                days=1,
            )

    api_blueprint = Blueprint("api", __name__, url_prefix="/api")
    api = StarDriveApi(api_blueprint)
    _app.register_blueprint(api_blueprint)
    _app.register_blueprint(auth_blueprint)
    _app.register_blueprint(tracking_blueprint)

    parser = RequestParser()
    parser.add_argument("resource")

    @_app.route("/", methods=["GET"])
    def root():
        output = {}
        for rule in _app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = "<{0}>".format(arg)

            methods = ",".join(rule.methods)
            url = url_for(rule.endpoint, **options)
            output[rule.endpoint] = unquote(url)

        return jsonify(output)

    # Add all endpoints to the API
    for endpoint in endpoints:
        api.add_resource(endpoint[0], endpoint[1])

    # Cron scheduler
    if not _app.got_first_request:
        schedule_tasks()

    return _app
