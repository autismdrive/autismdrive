from flask.views import MethodView
from sqlalchemy import Integer, cast

from app.auth import auth
from app.database import session
from app.enums import Permission, Role
from app.models import EmailLog
from app.schemas import SchemaRegistry
from app.wrappers import requires_permission, requires_role


class EmailLogListEndpoint(MethodView):
    emailLogsSchema = SchemaRegistry.EmailLogSchema(many=True)

    @auth.login_required
    @requires_role(Role.admin)
    def get(self):
        email_logs = session.query(EmailLog).all()
        return self.emailLogsSchema.dump(email_logs)


class EmailLogEndpoint(MethodView):
    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, user_id):
        schema = SchemaRegistry.EmailLogSchema(many=True)
        logs = session.query(EmailLog).filter(EmailLog.user_id == cast(user_id, Integer)).all()
        return schema.dump(logs)
