import flask_restful
from flask import jsonify

from app.models import FrontendConfig
from app.schemas import SchemaRegistry


class ConfigEndpoint(flask_restful.Resource):
    """Provides a way to get configuration information about the currently running backend."""

    schema = SchemaRegistry.FrontendConfigSchema()

    def get(self):
        config = FrontendConfig()
        return jsonify(self.schema.dump(config))
