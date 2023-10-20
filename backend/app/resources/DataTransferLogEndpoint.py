import flask_restful
from flask import request
from sqlalchemy import desc

from app.auth import auth
from app.models import DataTransferLog
from app.schemas import DataTransferLogPageSchema
from app.enums import Role
from app.wrappers import requires_roles


class DataTransferLogEndpoint(flask_restful.Resource):

    logs_schema = DataTransferLogPageSchema()

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        from flask import current_app

        db = getattr(current_app, "db")

        args = request.args
        page_number = eval(args["pageNumber"]) if ("pageNumber" in args) else 0
        per_page = eval(args["pageSize"]) if ("pageSize" in args) else 20
        query = db.select(DataTransferLog).order_by(desc(DataTransferLog.last_updated))
        page = db.paginate(query, page=page_number + 1, per_page=per_page, error_out=False)
        return self.logs_schema.dump(page)
