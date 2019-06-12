
import flask_restful
from app import db, auth
from app.model.email_log import EmailLogSchema, EmailLog
from app.model.step_log import StepLogSchema, StepLog
from app.model.user import Role
from app.wrappers import requires_roles


class StepLogListEndpoint(flask_restful.Resource):

    stepLogsSchema = StepLogSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        step_logs = db.session.query(StepLog).all()
        return self.stepLogsSchema.dump(step_logs)
