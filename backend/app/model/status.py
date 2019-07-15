from flask_marshmallow import Schema
from marshmallow import post_load

from app import app


class Status:
    """ Provides general information about the backend service, what mode it is running in, could also use it for
        health checks etc... """
    development = app.config.get("DEVELOPMENT")
    testing = app.config.get("TESTING")
    mirroring = app.config.get("MIRRORING")


class StatusSchema(Schema):
    class Meta:
        ordered = True
        fields = ["development", "testing", "mirroring"]

