import flask_restful
from flask import request
from sqlalchemy import cast, Integer

from app.auth import auth
from app.database import session
from app.email_service import email_service
from app.models import EmailLog, Study, StudyUser, User
from app.enums import StudyUserStatus
from app.models import StudyUser
from app.rest_exception import RestException


class StudyInquiryEndpoint(flask_restful.Resource):
    @auth.login_required
    def post(self):
        request_data = request.get_json()
        user_id = request_data["user_id"]
        study_id = request_data["study_id"]

        user = session.query(User).filter_by(id=cast(user_id, Integer)).first()
        study = session.query(Study).filter_by(id=cast(study_id, Integer)).first()

        if user and study:
            tracking_code = email_service.study_inquiry_email(study=study, user=user)
            log = EmailLog(user_id=user.id, type="study_inquiry_email", tracking_code=tracking_code)
            su = StudyUser(study_id=study.id, user_id=user.id, status=StudyUserStatus.inquiry_sent)
            session.add(log)
            session.add(su)
            session.commit()
            session.close()
            return ""
        else:
            raise RestException(RestException.STUDY_INQUIRY_ERROR)
