import json
import logging.config
import sys
from inspect import getframeinfo, getargvalues, currentframe, getouterframes
from urllib.parse import unquote

import click
import flask_restful
import traceback_with_variables
from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify, url_for, Blueprint
from flask_cors import CORS
from flask_restful.reqparse import RequestParser

from app.api_app import APIApp
from app.data_loader import data_loader
from app.elastic_index import elastic_index
from app.email_prompt_service import EmailPromptService
from app.resources.Auth import auth_blueprint
from app.resources.Tracking import tracking_blueprint
from app.rest_exception import RestException
from app.views import endpoints
from config.logging import logging_config


def create_app(settings=None):
    from config.load import settings as loaded_settings

    _settings = loaded_settings if settings is None else settings

    click.secho(f"\n*** create_app > _settings.ENV_NAME = {_settings.ENV_NAME} ***\n")

    logging.config.dictConfig(logging_config)

    _app = APIApp(__name__, instance_relative_config=True)

    _app.config.from_object(_settings)
    _app.settings = _settings

    # Enable CORS
    if _settings.CORS_ENABLED:
        # Convert list of allowed origins to list of regexes
        origins_re = [r"^https?:\/\/%s(.*)" % o.replace(".", "\.") for o in _settings.CORS_ALLOW_ORIGINS]
        CORS(_app, origins=origins_re)

    # Database
    from app.database import session

    _app.session = session

    # Email service
    from app.email_service import EmailService

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

        try:
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
        except Exception as _:
            error_dict = {"details": traceback_with_variables.format_exc(error)}

        error_location = None
        error_context = None

        # if settings.ENV_NAME in ["local", "dev", "testing"]:
        try:
            frame = currentframe()
            outer_frames = getouterframes(currentframe())

            for frame_info in outer_frames:
                if "Endpoint" in frame_info.filename:
                    arg_vals = getargvalues(frame_info.frame)
                    error_location = f"{frame_info.filename}:{frame_info.lineno}"
                    error_context = json.loads(
                        json.dumps(arg_vals.locals, ensure_ascii=True, indent=4, sort_keys=True, default=str)
                    )
        finally:
            # Prevent memory leak (https://docs.python.org/3/library/inspect.html#:~:text=handle_stackframe_without_leak)
            del outer_frames
            del frame

        response_dict = error_dict | {
            "error_location": error_location,
            "error_context": error_context,
        }

        response = jsonify(response_dict)
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
        from app.database import clear_db

        click.echo("Clearing out the database")
        clear_db()

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
        from app.database import clear_db

        click.echo("Rebuilding the databases from the example data files")
        data_loader.clear_index()
        clear_db()
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

    @_app.cli.command()
    def schedule_tasks():
        from app.models import User
        from app.models import Study
        from app.models import EmailLog
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
    api = flask_restful.Api(api_blueprint)
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

    @_app.teardown_appcontext
    def shutdown_session(exception=None):
        """Enable Flask to automatically remove database sessions at the
        end of the request or when the application shuts down.
        """
        from app.database import session

        session.remove()

    return _app
