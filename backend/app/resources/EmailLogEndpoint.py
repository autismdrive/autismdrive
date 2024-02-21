import flask_restful
from sqlalchemy import cast, Integer

from app.auth import auth
from app.database import session
from app.models import EmailLog
from app.enums import Permission, Role
from app.schemas import SchemaRegistry
from app.wrappers import requires_roles, requires_permission


class EmailLogListEndpoint(flask_restful.Resource):

    emailLogsSchema = SchemaRegistry.EmailLogSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        email_logs = session.query(EmailLog).all()
        return self.emailLogsSchema.dump(email_logs)


class EmailLogEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, user_id):
        schema = SchemaRegistry.EmailLogSchema(many=True)
        logs = session.query(EmailLog).filter(EmailLog.user_id == cast(user_id, Integer)).all()
        return schema.dump(logs)
