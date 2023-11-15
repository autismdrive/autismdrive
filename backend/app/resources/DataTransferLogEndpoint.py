import flask_restful
import math
from flask import request
from sqlalchemy import select, desc

from app.auth import auth
from app.database import session
from app.enums import Role
from app.models import DataTransferLog
from app.schemas import DataTransferLogPageSchema
from app.wrappers import requires_roles


class DataTransferLogEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):

        logs_schema = DataTransferLogPageSchema()

        args = request.args
        page_number = int(args["pageNumber"]) if ("pageNumber" in args) else 0
        per_page = int(args["pageSize"]) if ("pageSize" in args) else 20

        q = session.query(DataTransferLog)
        num_items = q.count()
        num_pages = math.ceil(num_items / per_page)
        items = q.order_by(desc(DataTransferLog.last_updated)).limit(per_page).offset(page_number + 1).all()
        return logs_schema.dump(
            {
                "items": items,
                "pages": num_pages,
                "total": num_items,
            }
        )
