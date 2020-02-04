import flask_restful
from app import db, auth
from app.model.resource_change_log import ResourceChangeLog
from app.schema.schema import ResourceChangeLogSchema
from app.model.role import Role, Permission
from app.wrappers import requires_roles, requires_permission


class ResourceChangeLogListEndpoint(flask_restful.Resource):

    resourceChangeLogSchema = ResourceChangeLogSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        resource_change_logs = db.session.query(ResourceChangeLog).all()
        return self.resourceChangeLogSchema.dump(resource_change_logs)


class ResourceChangeLogByUserEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, user_id):
        schema = ResourceChangeLogSchema(many=True)
        logs = db.session.query(ResourceChangeLog)\
            .filter(ResourceChangeLog.user_id == user_id)\
            .all()
        return schema.dump(logs)


class ResourceChangeLogByResourceEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def get(self, resource_id):
        schema = ResourceChangeLogSchema(many=True)
        logs = db.session.query(ResourceChangeLog)\
            .filter(ResourceChangeLog.resource_id == resource_id)\
            .all()
        return schema.dump(logs)
