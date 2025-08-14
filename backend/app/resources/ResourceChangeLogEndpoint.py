from flask.views import MethodView
from sqlalchemy import Integer, cast

from app.auth import auth
from app.database import session
from app.enums import Permission, Role
from app.models import ResourceChangeLog
from app.schemas import SchemaRegistry
from app.wrappers import requires_permission, requires_role


class ResourceChangeLogListEndpoint(MethodView):
    resourceChangeLogSchema = SchemaRegistry.ResourceChangeLogSchema(many=True)

    @auth.login_required
    @requires_role(Role.admin)
    def get(self):
        resource_change_logs = session.query(ResourceChangeLog).all()
        return self.SchemaRegistry.resourceChangeLogSchema.dump(resource_change_logs)


class ResourceChangeLogByUserEndpoint(MethodView):
    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, user_id):
        schema = SchemaRegistry.ResourceChangeLogSchema(many=True)
        logs = session.query(ResourceChangeLog).filter(ResourceChangeLog.user_id == cast(user_id, Integer)).all()
        return schema.dump(logs)


class ResourceChangeLogByResourceEndpoint(MethodView):
    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def get(self, resource_id: int):
        schema = SchemaRegistry.ResourceChangeLogSchema(many=True)
        logs = session.query(ResourceChangeLog).filter_by(resource_id=resource_id).all()
        return schema.dump(logs)
