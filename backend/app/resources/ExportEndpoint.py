import flask_restful

from app import auth
from app.model.export_info import ExportInfoSchema
from app.model.user import Role
from app.wrappers import requires_roles
from app.export_service import DataExport


class ExportEndpoint(flask_restful.Resource):

    schema = ExportInfoSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, name):
        return DataExport().get_data(name)


class ExportListEndpoint(flask_restful.Resource):

    schema = ExportInfoSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        return self.schema.dump(DataExport.all_exportable_data_names())


