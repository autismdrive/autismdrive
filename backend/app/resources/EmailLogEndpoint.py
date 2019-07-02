import flask_restful

from app import db, auth
from app.model.email_log import EmailLog
from app.resources.schema import EmailLogSchema
from app.model.user import Role
from app.wrappers import requires_roles


class EmailLogEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, user_id):
        schema = EmailLogSchema(many=True)
        logs = db.session.query(EmailLog)\
            .filter(EmailLog.user_id == user_id)\
            .all()
        return schema.dump(logs)
