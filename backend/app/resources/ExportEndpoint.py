import datetime

import flask_restful
from flask import request
from sqlalchemy import desc

from app.auth import auth
from app.database import session
from app.enums import Role
from app.export_service import ExportService
from app.models import DataTransferLog, DataTransferLogDetail, User
from app.schemas import ExportSchemas, ExportInfoSchema
from app.utils import pascal_case_it
from app.wrappers import requires_roles


def get_date_arg():
    """
    Returns a UTC datetime object from the "after" URL parameter in the request args,
    or None if not present. The date string is assumed to be in the UTC timezone.
    """
    date_arg = request.args.get("after")
    return (
        datetime.datetime.strptime(date_arg, ExportService.DATE_FORMAT).replace(tzinfo=datetime.timezone.utc)
        if date_arg
        else None
    )


class ExportEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, name):
        if name == "admin":
            return self.get_admin()

        name = pascal_case_it(name)
        schema = ExportService.get_schema(name, many=True)
        return schema.dump(ExportService().get_data(name, last_updated=get_date_arg()))

    def get_admin(self):
        query = session.query(User).filter(User.role == Role.admin)
        schema = ExportSchemas.AdminExportSchema(many=True)
        return schema.dump(query.all())


class ExportListEndpoint(flask_restful.Resource):

    schema = ExportInfoSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        date_started = datetime.datetime.utcnow()
        info_list = ExportService.get_table_info(get_date_arg())

        # Remove items that are not exportable, or that are identifying
        info_list = [item for item in info_list if item.exportable]
        info_list = [item for item in info_list if item.question_type != ExportService.TYPE_IDENTIFYING]

        # Get a count of the records, and log it.
        log = DataTransferLog(type="exporting")
        total_records_for_export = 0
        for item in info_list:
            total_records_for_export += item.size
            if item.size > 0:
                log_detail = DataTransferLogDetail(
                    date_started=date_started, class_name=item.class_name, successful=True, success_count=item.size
                )
                log.details.append(log_detail)
        log.total_records = total_records_for_export

        # If we find we aren't exporting anything, don't create a new log, just update the last one.
        if total_records_for_export == 0:
            log = (
                session.query(DataTransferLog)
                .filter(DataTransferLog.type == "exporting")
                .order_by(desc(DataTransferLog.last_updated))
                .limit(1)
                .first()
            )
            if log is None:
                log = DataTransferLog(type="exporting", total_records=0)
            log.last_updated = datetime.datetime.utcnow()
        session.add(log)
        session.commit()

        return self.schema.dump(info_list)
