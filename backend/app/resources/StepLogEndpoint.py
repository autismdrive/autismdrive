
import flask_restful

from app import db, auth
from app.model.step_log import StepLog
from app.resources.schema import StepLogSchema
from app.model.user import Role
from app.wrappers import requires_roles


class StepLogListEndpoint(flask_restful.Resource):

    stepLogsSchema = StepLogSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        step_logs = db.session.query(StepLog).all()
        return self.stepLogsSchema.dump(step_logs)


class StepLogEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, participant_id):
        schema = StepLogSchema(many=True)
        logs = db.session.query(StepLog)\
            .filter(StepLog.participant_id == participant_id)\
            .all()
        return schema.dump(logs)
