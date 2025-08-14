from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import session
from app.email_service import EmailService
from app.models import User
from app.utils import utcnow
from config.load import settings

ONE_DAY = 86400


class EmailPromptService:
    email_service = EmailService()

    def __init__(self, email_log_model, study_model, user_model):
        self.email_log_model = email_log_model
        self.study_model = study_model
        self.user_model = user_model

    def send_confirm_prompting_emails(self):
        recipients = session.query(self.user_model).filter_by(password=None).all()
        self._send_prompts(recipients, self.email_service.async_confirm_email, "confirm_email")

    def send_complete_registration_prompting_emails(self):
        confirmed_users = (
            session.execute(select(self.user_model).filter(self.user_model.password is not None))
            .unique()
            .scalars()
            .all()
        )
        recipients = [u for u in confirmed_users if u.self_registration_complete() is False]
        session.close()
        self._send_prompts(
            recipients, self.email_service.complete_registration_prompt_email, "complete_registration_prompt"
        )

    def send_dependent_profile_prompting_emails(self):
        confirmed_users = (
            session.execute(select(User).options(joinedload(User.participants)).where(User._password.is_not(None)))
            .unique()
            .scalars()
            .all()
        )
        recipients = []
        for u in confirmed_users:
            if (
                (u.self_participant() is not None)
                and (u.self_participant().relationship.name == "self_guardian")
                and (u.self_registration_complete() is True)
            ):
                dependents = [p for p in u.participants if p.relationship.name == "dependent"]
                incomplete_dependents = [p for p in dependents if p.get_percent_complete() < 1]
                if (len(dependents) == 0) or (len(incomplete_dependents) > 0):
                    recipients.append(u)
        self._send_prompts(
            recipients, self.email_service.complete_dependent_profile_prompt_email, "dependent_profile_prompt"
        )

    def _send_prompts(self, recipients: list[User], send_method: Callable, log_type: str):
        """
        Schedules prompting emails to recipients who have not yet completed the specified action.

        The frequency of the emails is determined based on the number of previous emails sent and the time since
        the last email was sent:

        - If no emails have been sent and the user logged in more than 2 days ago, send an email.
        - If 1 or 2 emails have already been sent, schedule a reminder email at 7 or 14 days, respectively.
        - If 3 emails have already been sent and more than 16 days have passed since the last email, remind them at 30 days.
        - If 4 or 5 emails have already been sent and more than 30 days have passed since the last email, remind them at 60 or 90 days, respectively.
        """

        for rec in recipients:
            email_logs = (
                session.query(self.email_log_model)
                .filter_by(user_id=rec.id)
                .filter_by(type=log_type)
                .order_by(self.email_log_model.last_updated)
                .all()
            )
            days_since_most_recent = -1

            # Determine when we last sent them an email.
            if len(email_logs) > 0:
                most_recent = email_logs[-1]
                days_since_most_recent = (utcnow() - most_recent.last_updated).total_seconds() / ONE_DAY

            # If we've never emailed them AND they haven't completed their registration/profile yet,
            # send them a reminder email 2 days after their last login
            if (len(email_logs) == 0) and (log_type != "confirm_email"):
                if (rec.last_login is not None) and ((utcnow() - rec.last_login).total_seconds() > (2 * ONE_DAY)):
                    self._send_prompting_email(rec, send_method, log_type, "0days")

            # If we've already sent them 1 or 2 emails, schedule a reminder for
            # 1 week or 2 weeks (respectively) after the last prompting email.
            elif 0 < len(email_logs) <= 2:
                days = "7days" if len(email_logs) == 1 else "14days"
                if days_since_most_recent > 7:
                    self._send_prompting_email(rec, send_method, log_type, days)

            # If we've already sent them 3 emails AND it's been over 16 days since we last sent a reminder,
            # schedule another reminder for 30 days after the last prompting email.
            elif len(email_logs) == 3:
                if days_since_most_recent > 16:
                    self._send_prompting_email(rec, send_method, log_type, "30days")

            # If we've already sent them 4 or 5 emails AND it's been over 30 days since we last sent a reminder,
            # schedule another reminder for 60 or 90 days (respectively) after the last prompting email.
            elif 3 < len(email_logs) < 6:
                if days_since_most_recent > 30:
                    days = str((len(email_logs) - 2) * 30) + "days"
                    self._send_prompting_email(rec, send_method, log_type, days)

    def _send_prompting_email(self, user, send_method, log_type, days):
        match log_type:
            case "confirm_email":
                campaign = "reset_password"
            case "complete_registration_prompt":
                campaign = "create_yourprofile"
            case "dependent_profile_prompt":
                campaign = "create_dependentprofile"
            case _:
                campaign = "prompting"

        current_studies = session.query(self.study_model).filter_by(status="currently_enrolling").all()
        for study in current_studies:
            study.link = (
                settings.SITE_URL
                + "/#/study/"
                + str(study.id)
                + EmailService.generate_google_analytics_link_content(campaign + "_study" + str(study.id), days)
            )
        tracking_code = send_method(user, current_studies, days)
        log = self.email_log_model(user_id=user.id, type=log_type, tracking_code=tracking_code)
        session.add(log)
        session.commit()
