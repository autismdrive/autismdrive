import flask_restful
from sqlalchemy import cast, Integer

from app.auth import auth
from app.database import session
from app.enums import Permission, Role
from app.models import StudyChangeLog
from app.schemas import SchemaRegistry
from app.wrappers import requires_roles, requires_permission


class StudyChangeLogListEndpoint(flask_restful.Resource):

    studyChangeLogSchema = SchemaRegistry.StudyChangeLogSchema(many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self):
        study_change_logs = session.query(StudyChangeLog).all()
        return self.SchemaRegistry.studyChangeLogSchema.dump(study_change_logs)


class StudyChangeLogByUserEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, user_id):
        schema = SchemaRegistry.StudyChangeLogSchema(many=True)
        logs = session.query(StudyChangeLog).filter(StudyChangeLog.user_id == cast(user_id, Integer)).all()
        return schema.dump(logs)


class StudyChangeLogByStudyEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.edit_study)
    def get(self, study_id: int):
        schema = SchemaRegistry.StudyChangeLogSchema(many=True)
        logs = session.query(StudyChangeLog).filter_by(study_id=study_id).all()
        return schema.dump(logs)
