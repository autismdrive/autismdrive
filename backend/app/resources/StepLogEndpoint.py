import flask_restful

from app import db, auth
from app.model.step_log import StepLog
from app.resources.schema import StepLogSchema
from app.model.user import Role
from app.wrappers import requires_roles


class StepLogEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, participant_id):
        schema = StepLogSchema(many=True)
        logs = db.session.query(StepLog)\
            .filter(StepLog.participant_id == participant_id)\
            .all()
        return schema.dump(logs)