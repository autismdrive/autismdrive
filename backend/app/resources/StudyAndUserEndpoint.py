import flask_restful
from flask import request
from sqlalchemy import cast, Integer, select
from sqlalchemy.orm import joinedload

from app.auth import auth
from app.database import session
from app.enums import Role, StudyUserStatus
from app.models import Study, StudyUser, User
from app.rest_exception import RestException
from app.schemas import StudyUserSchema, UserStudiesSchema, StudyUsersSchema
from app.wrappers import requires_roles


class StudyInquiryByUserEndpoint(flask_restful.Resource):

    schema = UserStudiesSchema()

    @auth.login_required
    def get(self, user_id):
        study_users = (
            session.query(StudyUser)
            .join(StudyUser.study)
            .filter(StudyUser.user_id == cast(user_id, Integer))
            .filter(StudyUser.status == StudyUserStatus.inquiry_sent)
            .order_by(Study.title)
            .all()
        )
        return self.schema.dump(study_users, many=True)


class StudyEnrolledByUserEndpoint(flask_restful.Resource):

    schema = UserStudiesSchema()

    @auth.login_required
    def get(self, user_id):
        study_users = (
            session.query(StudyUser)
            .join(StudyUser.study)
            .filter(StudyUser.user_id == cast(user_id, Integer))
            .filter(StudyUser.status == StudyUserStatus.enrolled)
            .order_by(Study.title)
            .all()
        )
        return self.schema.dump(study_users, many=True)


class UserByStudyEndpoint(flask_restful.Resource):

    schema = StudyUsersSchema()

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, study_id):
        s_id = cast(study_id, Integer)
        study_users = (
            session.execute(
                select(StudyUser)
                .options(joinedload(StudyUser.user).options(joinedload(User.participants)))
                .filter(StudyUser.study_id == s_id)
            )
            .unique()
            .scalars()
            .all()
        )
        session.close()

        # Sort the study_users by user email
        study_users.sort(key=lambda x: x.user.email)

        return self.schema.dump(study_users, many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def post(self, study_id):
        request_data = request.get_json()
        s_id = int(study_id)

        for item in request_data:
            item["study_id"] = s_id

        study_users = self.schema.load(request_data, many=True)
        session.query(StudyUser).filter_by(study_id=cast(s_id, Integer)).delete()
        for c in study_users:
            session.add(StudyUser(study_id=s_id, user_id=c.user_id))
        session.commit()
        return self.get(s_id)


class StudyUserEndpoint(flask_restful.Resource):
    schema = StudyUserSchema()

    @auth.login_required
    def get(self, id):
        model = session.query(StudyUser).filter_by(id=cast(id, Integer)).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    def delete(self, id):
        session.query(StudyUser).filter_by(id=cast(id, Integer)).delete()
        session.commit()
        return None


class StudyUserListEndpoint(flask_restful.Resource):
    schema = StudyUserSchema()

    @auth.login_required
    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data)
        session.query(StudyUser).filter_by(study_id=load_result.study_id, user_id=load_result.user_id).delete()
        session.add(load_result)
        session.commit()
        return self.schema.dump(load_result)
