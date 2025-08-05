from flask import jsonify
from flask.views import MethodView

from app.models import FrontendConfig
from app.schemas import SchemaRegistry


class ConfigEndpoint(MethodView):
    """Provides a way to get configuration information about the currently running backend."""

    schema = SchemaRegistry.FrontendConfigSchema()

    def get(self):
        config = FrontendConfig()
        return jsonify(self.schema.dump(config))
