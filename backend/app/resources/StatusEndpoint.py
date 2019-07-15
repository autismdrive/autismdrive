import flask_restful
from flask import jsonify

from app.model.status import StatusSchema, Status


class StatusEndpoint(flask_restful.Resource):
    """Provides a way to get configuration information about the currently running backend."""
    schema = StatusSchema()

    def get(self):
        status = Status()
        return jsonify(self.schema.dump(status).data)
