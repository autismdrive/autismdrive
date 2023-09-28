import flask_restful
from flask import request

from app.auth import auth
from app.database import session
from app.email_service import email_service
from app.model.email_log import EmailLog
from app.model.study import Study, StudyUserStatus, StudyUser
from app.model.user import User
from app.rest_exception import RestException


class StudyInquiryEndpoint(flask_restful.Resource):
    @auth.login_required
    def post(self):
        request_data = request.get_json()
        user_id = request_data["user_id"]
        study_id = request_data["study_id"]

        user = session.query(User).filter_by(id=user_id).first()
        study = session.query(Study).filter_by(id=study_id).first()

        if user and study:
            tracking_code = email_service.study_inquiry_email(study=study, user=user)
            log = EmailLog(user_id=user.id, type="study_inquiry_email", tracking_code=tracking_code)
            su = StudyUser(study_id=study.id, user_id=user.id, status=StudyUserStatus.inquiry_sent)
            session.add(log)
            session.add(su)
            session.commit()
            return ""
        else:
            raise RestException(RestException.STUDY_INQUIRY_ERROR)
