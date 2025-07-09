import functools

import click
import elastic_transport
from psycopg import OperationalError as PsycopgOperationalError
from sqlalchemy.exc import OperationalError
import traceback
import logging

from urllib3.exceptions import NewConnectionError


def handle_db_connection_errors(func):
    """
    Decorator to handle database "Connection refused" errors.

    This prevents the application from crashing if it loses
    connection to the database, such as when the database
    server is temporarily down or unresponsive.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (OperationalError, PsycopgOperationalError, ConnectionRefusedError) as op_error:
            error_text = f"{op_error}"
            if str.find(error_text, "Connection refused"):
                # Print the file name and line number where the original error occurred.
                tb = traceback.extract_stack()[-2]
                hr = "-" * 80

                error_message = (
                    f"{hr}\n"
                    f"Database connection error occurred in {tb.filename} at line {tb.lineno}\n\n"
                    f"{op_error}\n"
                    f"{hr}\n"
                )

                # Don't raise the error, just log it.
                click.secho(error_message, color=True, fg="red")
                logging.getLogger("database").error(error_message)

    return wrapper


def handle_es_connection_errors(func):
    """
    Decorator to handle Elasticsearch "Connection refused" errors.

    This prevents the application from crashing if it loses
    connection to Elasticsearch, such as when the Elasticsearch
    server is temporarily down or unresponsive.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (elastic_transport.ConnectionError, ConnectionRefusedError, NewConnectionError) as es_error:
            error_text = f"{es_error}"

            if str.find(error_text, "Connection refused"):
                # Print the file name and line number where the original error occurred.
                tb = traceback.extract_stack()[-2]
                hr = "-" * 80

                error_message = (
                    f"{hr}\n"
                    f"Elasticsearch connection error occurred in {tb.filename} at line {tb.lineno}\n\n"
                    f"{es_error}\n"
                    f"{hr}\n"
                )

                # Don't raise the error, just log it.
                click.secho(error_message, color=True, fg="red")
                logging.getLogger("database").error(error_message)

        except Exception as generic_error:
            click.secho(f"Generic error: {generic_error}", color=True, fg="yellow")

    return wrapper
