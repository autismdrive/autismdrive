
import flask_restful
from app import db, auth
from app.model.email_log import EmailLogSchema, EmailLog
from app.model.user import Role
from app.wrappers import requires_roles


class EmailLogListEndpoint(flask_restful.Resource):

    emailLogsSchema = EmailLogSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        email_logs = db.session.query(EmailLog).all()
        return self.emailLogsSchema.dump(email_logs)
