import flask_restful
from flask import jsonify

from app.model.frontend_config import FrontendConfigSchema, FrontendConfig


class ConfigEndpoint(flask_restful.Resource):
    """Provides a way to get configuration information about the currently running backend."""
    schema = FrontendConfigSchema()

    def get(self):
        config = FrontendConfig()
        return jsonify(self.schema.dump(config))
