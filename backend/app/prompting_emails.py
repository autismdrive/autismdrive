import datetime

from dateutil.tz import UTC

from app import db, app
from app.model.email_log import EmailLog
from app.model.study import Study
from app.model.user import User
from app.email_service import EmailService


class PromptingEmails:

    def send_prompts(self, recipients, send_method, log_type):
        for rec in recipients:
            email_logs = db.session.query(EmailLog)\
                .filter_by(user_id=rec.id)\
                .filter_by(type=log_type) \
                .order_by(EmailLog.last_updated).all()
            if (len(email_logs) is 0) and (log_type is not 'confirm_email'):
                if (datetime.datetime.now(tz=UTC) - rec.last_login).total_seconds() > 172800:
                    self.send_prompting_email(rec, send_method, log_type)
            elif 0 < len(email_logs) <= 2:
                most_recent = email_logs[-1]
                if (datetime.datetime.now(tz=UTC) - most_recent.last_updated).total_seconds() > 604800:
                    self.send_prompting_email(rec, send_method, log_type)
            elif len(email_logs) is 3:
                most_recent = email_logs[-1]
                if (datetime.datetime.now(tz=UTC) - most_recent.last_updated).total_seconds() > 1314900:
                    self.send_prompting_email(rec, send_method, log_type)
            elif 3 < len(email_logs) < 6:
                most_recent = email_logs[-1]
                if (datetime.datetime.now(tz=UTC) - most_recent.last_updated).total_seconds() > 2629800:
                    self.send_prompting_email(rec, send_method, log_type)

    @staticmethod
    def send_prompting_email(user, send_method, log_type):
        current_studies = db.session.query(Study).filter_by(status='currently_enrolling').all()
        for study in current_studies:
            study.link = app.config['SITE_URL'] + '/#/study/' + str(study.id)
        tracking_code = send_method(user, current_studies)
        log = EmailLog(user_id=user.id, type=log_type, tracking_code=tracking_code)
        db.session.add(log)
        db.session.commit()

    def send_confirm_prompting_emails(self):
        recipients = db.session.query(User).filter_by(password=None).all()
        self.send_prompts(recipients, EmailService(app).confirm_email, 'confirm_email')

    def send_complete_registration_prompting_emails(self):
        confirmed_users = db.session.query(User).filter(User.password is not None).all()
        recipients = [u for u in confirmed_users if u.self_registration_complete() is False]
        self.send_prompts(recipients, EmailService(app).complete_registration_prompt_email,
                          'complete_registration_prompt')

    def send_dependent_profile_prompting_emails(self):
        confirmed_users = db.session.query(User).filter(User.password is not None).all()
        recipients = []
        for u in confirmed_users:
            if (u.get_self_participant().relationship.name == 'self_guardian') \
                    and (u.self_registration_complete() is True):
                dependents = [p for p in u.participants if p.relationship.name == 'dependent']
                incomplete_dependents = [p for p in dependents if p.get_percent_complete() < 1]
                if (len(dependents) == 0) or (len(incomplete_dependents) > 0):
                    recipients.append(u)
        self.send_prompts(recipients, EmailService(app).complete_dependent_profile_prompt_email,
                          'dependent_profile_prompt')
