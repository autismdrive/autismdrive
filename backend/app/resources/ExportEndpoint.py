import datetime

import flask_restful
from flask import json, request

from app import auth
from app.model.export_info import ExportInfoSchema
from app.model.user import Role
from app.wrappers import requires_roles
from app.export_service import ExportService


class ExportEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, name):
        date_arg = request.args.get('after')
        after_date = datetime.datetime.strptime(date_arg, ExportService.DATE_FORMAT)

        name = ExportService.camel_case_it(name)
        schema = ExportService.get_schema(name, many=True)
        return schema.dump(ExportService().get_data(name, after_date))


class ExportListEndpoint(flask_restful.Resource):

    schema = ExportInfoSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        return self.schema.dump(ExportService.get_export_info())


