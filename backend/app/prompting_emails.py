import datetime

from dateutil.tz import UTC

from app import db, app
from app.model.email_log import EmailLog
from app.model.study import Study
from app.model.user import User
from app.email_service import EmailService


class PromptingEmails:

    def send_set_password_prompts(self):
        recipients = db.session.query(User).filter_by(password=None).all()
        for rec in recipients:
            confirm_logs = db.session.query(EmailLog)\
                .filter_by(user_id=rec.id)\
                .filter_by(type='confirm_email') \
                .order_by(EmailLog.last_updated).all()
            if len(confirm_logs) <= 2:
                most_recent = confirm_logs[-1]
                if (datetime.datetime.now(tz=UTC) - most_recent.last_updated).total_seconds() > 604800:
                    self.send_confirm_email(rec)
            elif len(confirm_logs) is 3:
                most_recent = confirm_logs[-1]
                if (datetime.datetime.now(tz=UTC) - most_recent.last_updated).total_seconds() > 1314900:
                    self.send_confirm_email(rec)
            elif 3 < len(confirm_logs) < 6:
                most_recent = confirm_logs[-1]
                if (datetime.datetime.now(tz=UTC) - most_recent.last_updated).total_seconds() > 2629800:
                    self.send_confirm_email(rec)

    @staticmethod
    def send_confirm_email(user):
        current_studies = db.session.query(Study).filter_by(status='currently_enrolling').all()
        for study in current_studies:
            study.link = app.config['SITE_URL'] + '/#/study/' + str(study.id)
        tracking_code = EmailService(app).confirm_email(user, current_studies)
        log = EmailLog(user_id=user.id, type="confirm_email", tracking_code=tracking_code)
        db.session.add(log)
        db.session.commit()

    @staticmethod
    def send_complete_registration_email(user):
        current_studies = db.session.query(Study).filter_by(status='currently_enrolling').all()
        for study in current_studies:
            study.link = app.config['SITE_URL'] + '/#/study/' + str(study.id)
        tracking_code = EmailService(app).complete_registration_prompt_email(user, current_studies)
        log = EmailLog(user_id=user.id, type="complete_registration_prompt", tracking_code=tracking_code)
        db.session.add(log)
        db.session.commit()

    @staticmethod
    def send_dependent_profile_email(user):
        current_studies = db.session.query(Study).filter_by(status='currently_enrolling').all()
        for study in current_studies:
            study.link = app.config['SITE_URL'] + '/#/study/' + str(study.id)
        tracking_code = EmailService(app).complete_dependent_profile_prompt_email(user, current_studies)
        log = EmailLog(user_id=user.id, type="dependent_profile_prompt", tracking_code=tracking_code)
        db.session.add(log)
        db.session.commit()
