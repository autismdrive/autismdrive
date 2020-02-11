from app.model.email_log import EmailLogSchema
import flask_restful
from app import db, auth
from app.model.email_log import EmailLog
from app.schema.schema import EmailLogSchema
from app.model.role import Role, Permission
from app.wrappers import requires_roles, requires_permission


class EmailLogListEndpoint(flask_restful.Resource):

    emailLogsSchema = EmailLogSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        email_logs = db.session.query(EmailLog).all()
        return self.emailLogsSchema.dump(email_logs)


class EmailLogEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, user_id):
        schema = EmailLogSchema(many=True)
        logs = db.session.query(EmailLog)\
            .filter(EmailLog.user_id == user_id)\
            .all()
        return schema.dump(logs)
