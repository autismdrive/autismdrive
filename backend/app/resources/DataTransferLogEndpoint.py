import flask_restful
from flask import request
from sqlalchemy import desc

from app.auth import auth
from app.database import session
from app.model.data_transfer_log import DataTransferLogPageSchema, DataTransferLog
from app.model.role import Role
from app.wrappers import requires_roles


class DataTransferLogEndpoint(flask_restful.Resource):

    logs_schema = DataTransferLogPageSchema()

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        args = request.args
        page_number = eval(args["pageNumber"]) if ("pageNumber" in args) else 0
        per_page = eval(args["pageSize"]) if ("pageSize" in args) else 20
        query = session.query(DataTransferLog).order_by(desc("last_updated"))
        page = query.paginate(page=page_number + 1, per_page=per_page, error_out=False)
        return self.logs_schema.dump(page)
