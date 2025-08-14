import math

from flask import request
from flask.views import MethodView
from sqlalchemy import desc

from app.auth import auth
from app.database import session
from app.enums import Role
from app.models import DataTransferLog
from app.schemas import SchemaRegistry
from app.wrappers import requires_role


class DataTransferLogEndpoint(MethodView):
    @auth.login_required
    @requires_role(Role.admin)
    def get(self):
        logs_schema = SchemaRegistry.DataTransferLogPageSchema()

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
