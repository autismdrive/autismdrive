from flask.views import MethodView
from sqlalchemy import Integer, cast

from app.auth import auth
from app.database import session
from app.enums import Permission, Role
from app.models import StudyChangeLog
from app.schemas import SchemaRegistry
from app.wrappers import requires_permission, requires_role


class StudyChangeLogListEndpoint(MethodView):
    studyChangeLogSchema = SchemaRegistry.StudyChangeLogSchema(many=True)

    @auth.login_required
    @requires_role(Role.admin)
    def get(self):
        study_change_logs = session.query(StudyChangeLog).all()
        return self.SchemaRegistry.studyChangeLogSchema.dump(study_change_logs)


class StudyChangeLogByUserEndpoint(MethodView):
    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, user_id):
        schema = SchemaRegistry.StudyChangeLogSchema(many=True)
        logs = session.query(StudyChangeLog).filter(StudyChangeLog.user_id == cast(user_id, Integer)).all()
        return schema.dump(logs)


class StudyChangeLogByStudyEndpoint(MethodView):
    @auth.login_required
    @requires_permission(Permission.edit_study)
    def get(self, study_id: int):
        schema = SchemaRegistry.StudyChangeLogSchema(many=True)
        logs = session.query(StudyChangeLog).filter_by(study_id=study_id).all()
        return schema.dump(logs)
