import flask_restful
from flask import request

from app import RestException, db, email_service, auth
from app.model.email_log import EmailLog
from app.model.study import Study
from app.model.user import User
from app.model.study_user import StudyUser, StudyUserStatus


class StudyInquiryEndpoint(flask_restful.Resource):

    @auth.login_required
    def post(self):
        request_data = request.get_json()
        user_id = request_data['user_id']
        study_id = request_data['study_id']

        user = db.session.query(User).filter_by(id=user_id).first()
        study = db.session.query(Study).filter_by(id=study_id).first()

        if user and study:
            tracking_code = email_service.study_inquiry_email(study=study, user=user)
            log = EmailLog(user_id=user.id, type="study_inquiry_email", tracking_code=tracking_code)
            su = StudyUser(study_id=study.id, user_id=user.id, status=StudyUserStatus.inquiry_sent)
            db.session.add(log)
            db.session.add(su)
            db.session.commit()
            return ''
        else:
            raise RestException(RestException.STUDY_INQUIRY_ERROR)
