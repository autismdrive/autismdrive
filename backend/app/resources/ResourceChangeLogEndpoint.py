import flask_restful
from sqlalchemy import cast, Integer

from app.auth import auth
from app.database import session
from app.models import ResourceChangeLog
from app.enums import Permission, Role
from app.schemas import SchemaRegistry
from app.wrappers import requires_roles, requires_permission


class ResourceChangeLogListEndpoint(flask_restful.Resource):

    resourceChangeLogSchema = SchemaRegistry.ResourceChangeLogSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        resource_change_logs = session.query(ResourceChangeLog).all()
        return self.SchemaRegistry.resourceChangeLogSchema.dump(resource_change_logs)


class ResourceChangeLogByUserEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, user_id):
        schema = SchemaRegistry.ResourceChangeLogSchema(many=True)
        logs = session.query(ResourceChangeLog).filter(ResourceChangeLog.user_id == cast(user_id, Integer)).all()
        return schema.dump(logs)


class ResourceChangeLogByResourceEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def get(self, resource_id):
        schema = SchemaRegistry.ResourceChangeLogSchema(many=True)
        logs = (
            session.query(ResourceChangeLog).filter(ResourceChangeLog.resource_id == cast(resource_id, Integer)).all()
        )
        return schema.dump(logs)
