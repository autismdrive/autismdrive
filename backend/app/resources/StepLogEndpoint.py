import flask_restful

from app.auth import auth
from app.database import session
from app.enums import Permission, Role
from app.models import StepLog
from app.schemas import StepLogSchema
from app.wrappers import requires_roles, requires_permission


class StepLogListEndpoint(flask_restful.Resource):

    stepLogsSchema = StepLogSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        step_logs = session.query(StepLog).all()
        return self.stepLogsSchema.dump(step_logs)


class StepLogEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, participant_id):
        schema = StepLogSchema(many=True)
        logs = session.query(StepLog).filter(StepLog.participant_id == participant_id).all()
        return schema.dump(logs)
