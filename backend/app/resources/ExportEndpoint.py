import datetime

import flask_restful
from flask import json, request

from app import auth, db
from app.model.export_info import ExportInfoSchema
from app.model.user import Role, User
from app.resources.ExportSchema import AdminExportSchema
from app.wrappers import requires_roles
from app.export_service import ExportService


class ExportEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, name):
        if name == "admin":
            return self.get_admin()
        date_arg = request.args.get('after')
        name = ExportService.camel_case_it(name)
        schema = ExportService.get_schema(name, many=True)
        after_date = None
        if date_arg:
            after_date = datetime.datetime.strptime(date_arg, ExportService.DATE_FORMAT)
        return schema.dump(ExportService().get_data(name, after_date))

    def get_admin(self):
        query = db.session.query(User).filter(User.role == Role.admin)
        schema = AdminExportSchema(many=True)
        return schema.dump(query.all())


class ExportListEndpoint(flask_restful.Resource):

    schema = ExportInfoSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        return self.schema.dump(ExportService.get_export_info())


