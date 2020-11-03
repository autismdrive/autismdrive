import datetime

from dateutil.tz import UTC

from app.email_service import EmailService


class EmailPromptService:
    def __init__(self, app, db, email_log_model, study_model, user_model):
        self.app = app
        self.db = db
        self.email_log_model = email_log_model
        self.study_model = study_model
        self.user_model = user_model

    def send_confirm_prompting_emails(self):
        recipients = self.db.session.query(self.user_model).filter_by(password=None).all()
        self.__send_prompts(recipients, EmailService(self.app).async_confirm_email, 'confirm_email')

    def send_complete_registration_prompting_emails(self):
        confirmed_users = self.db.session.query(self.user_model).filter(self.user_model.password is not None).all()
        recipients = [u for u in confirmed_users if u.self_registration_complete() is False]
        self.__send_prompts(recipients, EmailService(self.app).complete_registration_prompt_email,
                            'complete_registration_prompt')

    def send_dependent_profile_prompting_emails(self):
        confirmed_users = self.db.session.query(self.user_model).filter(self.user_model.password is not None).all()
        recipients = []
        for u in confirmed_users:
            if (u.self_participant is not None) \
                    and (u.self_participant.relationship.name == 'self_guardian') \
                    and (u.self_registration_complete() is True):
                dependents = [p for p in u.participants if p.relationship.name == 'dependent']
                incomplete_dependents = [p for p in dependents if p.get_percent_complete() < 1]
                if (len(dependents) == 0) or (len(incomplete_dependents) > 0):
                    recipients.append(u)
        self.__send_prompts(recipients, EmailService(self.app).complete_dependent_profile_prompt_email,
                            'dependent_profile_prompt')

    def __send_prompts(self, recipients, send_method, log_type):
        for rec in recipients:
            email_logs = self.db.session.query(self.email_log_model)\
                .filter_by(user_id=rec.id)\
                .filter_by(type=log_type) \
                .order_by(self.email_log_model.last_updated).all()
            if len(email_logs) > 0:
                most_recent = email_logs[-1]
                days_since_most_recent = (datetime.datetime.now(tz=UTC) - most_recent.last_updated).total_seconds() / 86400
            if (len(email_logs) == 0) and (log_type != 'confirm_email'):
                if (rec.last_login is not None) and ((datetime.datetime.now(tz=UTC) - rec.last_login).total_seconds() > (2 * 86400)):
                    self.__send_prompting_email(rec, send_method, log_type, '0days')
            elif 0 < len(email_logs) <= 2:
                days = '7days' if len(email_logs) == 1 else '14days'
                if days_since_most_recent > 7:
                    self.__send_prompting_email(rec, send_method, log_type, days)
            elif len(email_logs) == 3:
                if days_since_most_recent > 16:
                    self.__send_prompting_email(rec, send_method, log_type, '30days')
            elif 3 < len(email_logs) < 6:
                if days_since_most_recent > 30:
                    days = str((len(email_logs) - 2) * 30) + 'days'
                    self.__send_prompting_email(rec, send_method, log_type, days)

    def __send_prompting_email(self, user, send_method, log_type, days):
        campaign = 'prompting'
        if log_type == 'confirm_email':
            campaign = 'reset_password'
        elif log_type == 'complete_registration_prompt':
            campaign = 'create_yourprofile'
        elif log_type == 'dependent_profile_prompt':
            campaign = 'create_dependentprofile'
        current_studies = self.db.session.query(self.study_model).filter_by(status='currently_enrolling').all()
        for study in current_studies:
            study.link = self.app.config['SITE_URL'] + '/#/study/' + str(study.id) + \
                         EmailService.generate_google_analytics_link_content(campaign + '_study' + str(study.id), days)
        tracking_code = send_method(user, current_studies, days)
        log = self.email_log_model(user_id=user.id, type=log_type, tracking_code=tracking_code)
        self.db.session.add(log)
        self.db.session.commit()
