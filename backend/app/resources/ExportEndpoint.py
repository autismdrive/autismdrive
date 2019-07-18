import datetime

import flask_restful
from flask import request

from app import auth, db
from app.model.export_info import ExportInfoSchema
from app.model.export_log import ExportLog
from app.model.user import Role, User
from app.schema.export_schema import AdminExportSchema
from app.wrappers import requires_roles
from app.export_service import ExportService


def get_date_arg():
    date_arg = request.args.get('after')
    after_date = None
    if date_arg:
        after_date = datetime.datetime.strptime(date_arg, ExportService.DATE_FORMAT)
    return after_date

class ExportEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, name):
        if name == "admin":
            return self.get_admin()

        name = ExportService.camel_case_it(name)
        schema = ExportService.get_schema(name, many=True)
        return schema.dump(ExportService().get_data(name, get_date_arg()))

    def get_admin(self):
        query = db.session.query(User).filter(User.role == Role.admin)
        schema = AdminExportSchema(many=True)
        return schema.dump(query.all())


class ExportListEndpoint(flask_restful.Resource):

    schema = ExportInfoSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):

        info_list = ExportService.get_table_info(get_date_arg())

        # Remove items that are not exportable, or that are identifying
        info_list = [item for item in info_list if item.exportable]
        info_list = [item for item in info_list if item.question_type != ExportService.TYPE_IDENTIFYING]

        # Get a count of the records, and log it.
        total_records_for_export = 0
        for item in info_list:
            total_records_for_export += item.size
        log = ExportLog(available_records=total_records_for_export)
        db.session.add(log)

        return self.schema.dump(info_list)


