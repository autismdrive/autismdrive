import flask_restful
from flask import request

from app import db, RestException, auth
from app.model.user import User
from app.model.role import Role
from app.model.study import Study
from app.model.study_user import StudyUser, StudyUserStatus
from app.schema.schema import StudyUserSchema, UserStudiesSchema, StudyUsersSchema
from app.wrappers import requires_roles


class StudyByUserEndpoint(flask_restful.Resource):

    schema = UserStudiesSchema()

    @auth.login_required
    def get(self, user_id):
        study_users = db.session.query(StudyUser)\
            .join(StudyUser.study)\
            .filter(StudyUser.user_id == user_id)\
            .order_by(Study.title)\
            .all()
        return self.schema.dump(study_users, many=True)


class StudyInquiryByUserEndpoint(flask_restful.Resource):

    schema = UserStudiesSchema()

    @auth.login_required
    def get(self, user_id):
        study_users = db.session.query(StudyUser)\
            .join(StudyUser.study)\
            .filter(StudyUser.user_id == user_id)\
            .filter(StudyUser.status == StudyUserStatus.inquiry_sent)\
            .order_by(Study.title)\
            .all()
        return self.schema.dump(study_users, many=True)


class StudyEnrolledByUserEndpoint(flask_restful.Resource):

    schema = UserStudiesSchema()

    @auth.login_required
    def get(self, user_id):
        study_users = db.session.query(StudyUser)\
            .join(StudyUser.study)\
            .filter(StudyUser.user_id == user_id)\
            .filter(StudyUser.status == StudyUserStatus.enrolled)\
            .order_by(Study.title)\
            .all()
        return self.schema.dump(study_users, many=True)


class UserByStudyEndpoint(flask_restful.Resource):

    schema = StudyUsersSchema()

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, study_id):
        study_users = db.session.query(StudyUser).\
            join(StudyUser.user).\
            filter(StudyUser.study_id == study_id).\
            order_by(User.email).\
            all()
        return self.schema.dump(study_users, many=True)

    @auth.login_required
    @requires_roles(Role.admin)
    def post(self, study_id):
        request_data = request.get_json()

        for item in request_data:
            item['study_id'] = study_id

        study_users = self.schema.load(request_data, many=True)
        db.session.query(StudyUser).filter_by(study_id=study_id).delete()
        for c in study_users:
            db.session.add(StudyUser(study_id=study_id,
                           user_id=c.user_id))
        db.session.commit()
        return self.get(study_id)


class StudyUserEndpoint(flask_restful.Resource):
    schema = StudyUserSchema()

    @auth.login_required
    def get(self, id):
        model = db.session.query(StudyUser).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    def delete(self, id):
        db.session.query(StudyUser).filter_by(id=id).delete()
        db.session.commit()
        return None


class StudyUserListEndpoint(flask_restful.Resource):
    schema = StudyUserSchema()

    @auth.login_required
    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data)
        db.session.query(StudyUser).filter_by(study_id=load_result.study_id,
                                                     user_id=load_result.user_id).delete()
        db.session.add(load_result)
        db.session.commit()
        return self.schema.dump(load_result)
