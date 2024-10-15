import datetime
import smtplib
import uuid
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, url_for
from itsdangerous import URLSafeTimedSerializer

from config.load import settings


class EmailService:
    api_url: str = settings.API_URL
    site_url: str = settings.SITE_URL
    admin_email: str = settings.ADMIN_EMAIL
    principal_investigator_email: str = settings.PRINCIPAL_INVESTIGATOR_EMAIL
    TEST_MESSAGES = []

    def tracking_code(self):
        return str(uuid.uuid4())[:16]

    def email_server(self):
        server = smtplib.SMTP(host=settings.MAIL_SERVER, port=settings.MAIL_PORT, timeout=settings.MAIL_TIMEOUT)
        server.ehlo()
        if settings.MAIL_USE_TLS:
            server.starttls()
        if settings.MAIL_USERNAME:
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        return server

    def send_email(self, subject, recipients, text_body, html_body, sender=None, ical=None):
        msg_root = MIMEMultipart("related")
        msg_root.set_charset("utf8")

        if sender is None:
            sender = settings.MAIL_DEFAULT_SENDER

        msg_root["Subject"] = Header(subject.encode("utf-8"), "utf-8").encode()
        msg_root["From"] = sender
        msg_root["To"] = ", ".join(recipients)
        msg_root.preamble = "This is a multi-part message in MIME format."

        msg_alternative = MIMEMultipart("alternative")
        msg_root.attach(msg_alternative)

        part1 = MIMEText(text_body, "plain", _charset="UTF-8")
        part2 = MIMEText(html_body, "html", _charset="UTF-8")

        msg_alternative.attach(part1)
        msg_alternative.attach(part2)

        if ical:
            ical_attachment = MIMEText(ical.decode("utf-8"), "calendar")
            ical_attachment.add_header("Filename", "event.ics")
            ical_attachment.add_header("Content-Disposition", "attachment; filename=event.ics")
            msg_root.attach(ical_attachment)

        if settings.TESTING:
            print("TEST:  Recording Emails, not sending - %s - to:%s" % (subject, recipients))
            self.TEST_MESSAGES.append(msg_root)
            return

        server = self.email_server()
        server.sendmail(sender, recipients, msg_root.as_bytes())
        server.quit()

    def confirm_email(self, user, current_studies, tracking_code=None, logo_url=None, days="0days"):
        if tracking_code is None and logo_url is None:
            tracking_code = self.tracking_code()
            logo_url = url_for("track.logo", user_id=user.id, code=tracking_code, _external=True)
        user.token_url = ""
        ts = URLSafeTimedSerializer(settings.SECRET_KEY)
        token = ts.dumps(user.email, salt="email-reset-key")
        role = "" + user.role.name + "/"

        ga_link = self.generate_google_analytics_link_content("reset_password", days)
        studies_ga_link = self.generate_google_analytics_link_content("reset_password_studies", days)
        subject = "Autism DRIVE: Confirm Email"
        confirm_url = settings.SITE_URL + settings.FRONTEND_EMAIL_RESET + role + token + ga_link
        text_body = render_template(
            "confirm_email.txt",
            user=user,
            confirm_url=confirm_url,
            forgot_pass_url=settings.SITE_URL + settings.FRONTEND_FORGOT_PASSWORD + ga_link,
            tracking_code=tracking_code,
            current_studies=current_studies,
            studies_url=self.site_url + "/#/studies/currently_enrolling" + studies_ga_link,
        )

        html_body = render_template(
            "confirm_email.html",
            user=user,
            confirm_url=confirm_url,
            forgot_pass_url=settings.SITE_URL + settings.FRONTEND_FORGOT_PASSWORD + ga_link,
            logo_url=logo_url,
            tracking_code=tracking_code,
            current_studies=current_studies,
            studies_url=self.site_url + "/#/studies/currently_enrolling" + studies_ga_link,
        )

        self.send_email(subject, recipients=[user.email], text_body=text_body, html_body=html_body)

        if settings.TESTING or settings.DEVELOPMENT:
            user.token_url = confirm_url

        return tracking_code

    def async_confirm_email(self, user, current_studies, days):
        from flask import current_app

        with current_app.app_context(), current_app.test_request_context():
            tracking_code = self.tracking_code()
            logo_url = self.api_url + "/api/track/" + str(user.id) + "/" + tracking_code + "/UVA_STAR-logo.png"

            return self.confirm_email(user, current_studies, tracking_code, logo_url, days)

    def reset_email(self, user):
        user.token_url = ""
        ts = URLSafeTimedSerializer(settings.SECRET_KEY)
        token = ts.dumps(user.email, salt="email-reset-key")
        role = "" + user.role.name + "/"
        tracking_code = self.tracking_code()

        subject = "Autism DRIVE: Password Reset Email"
        reset_url = settings.SITE_URL + settings.FRONTEND_EMAIL_RESET + role + token
        logo_url = url_for("track.logo", user_id=user.id, code=tracking_code, _external=True)
        text_body = render_template(
            "reset_email.txt",
            user=user,
            reset_url=reset_url,
            forgot_pass_url=settings.SITE_URL + settings.FRONTEND_FORGOT_PASSWORD,
            tracking_code=tracking_code,
        )

        html_body = render_template(
            "reset_email.html",
            user=user,
            reset_url=reset_url,
            forgot_pass_url=settings.SITE_URL + settings.FRONTEND_FORGOT_PASSWORD,
            logo_url=logo_url,
            tracking_code=tracking_code,
        )

        self.send_email(subject, recipients=[user.email], text_body=text_body, html_body=html_body)

        if settings.TESTING or settings.DEVELOPMENT:
            user.token_url = reset_url

        return tracking_code

    def study_inquiry_email(self, study, user):
        tracking_code = self.tracking_code()

        subject = "Autism DRIVE: Study Inquiry Email"
        logo_url = url_for("track.logo", user_id=user.id, code=tracking_code, _external=True)
        text_body = render_template(
            "study_inquiry_email.txt",
            user=user,
            study=study,
            user_detail_url=self.site_url + "/#/admin/user/" + str(user.id),
            tracking_code=tracking_code,
        )

        html_body = render_template(
            "study_inquiry_email.html",
            user=user,
            study=study,
            user_detail_url=self.site_url + "/#/admin/user/" + str(user.id),
            logo_url=logo_url,
            tracking_code=tracking_code,
        )

        self.send_email(
            subject,
            recipients=[study.coordinator_email, "autismdrive@virginia.edu"],
            text_body=text_body,
            html_body=html_body,
        )

        return tracking_code

    def admin_alert_email(self, subject, message, alert_principal_investigator=False):
        from flask import current_app

        with current_app.app_context():
            context = {}
            text_body = render_template("admin_email.txt", msg=message, site_url=self.site_url, **context)
            html_body = render_template("admin_email.html", msg=message, site_url=self.site_url, **context)
            recipients = [self.admin_email]
            if alert_principal_investigator:
                recipients.append(self.principal_investigator_email)

            self.send_email(subject, recipients=recipients, text_body=text_body, html_body=html_body)

    def complete_registration_prompt_email(self, user, current_studies, days):
        from flask import current_app

        with current_app.app_context(), current_app.test_request_context():
            tracking_code = self.tracking_code()

            ga_link = self.generate_google_analytics_link_content("create_yourprofile", days)
            studies_ga_link = self.generate_google_analytics_link_content("create_yourprofile_studies", days)
            subject = "Autism DRIVE: Complete Your Registration"
            logo_url = self.api_url + "/api/track/" + str(user.id) + "/" + tracking_code + "/UVA_STAR-logo.png"
            text_body = render_template(
                "complete_registration_email.txt",
                profile_url=settings.SITE_URL + "/#/profile" + ga_link,
                forgot_pass_url=settings.SITE_URL + settings.FRONTEND_FORGOT_PASSWORD + ga_link,
                current_studies=current_studies,
                studies_url=self.site_url + "/#/studies/currently_enrolling" + studies_ga_link,
            )

            html_body = render_template(
                "complete_registration_email.html",
                profile_url=settings.SITE_URL + "/#/profile" + ga_link,
                forgot_pass_url=settings.SITE_URL + settings.FRONTEND_FORGOT_PASSWORD + ga_link,
                logo_url=logo_url,
                tracking_code=tracking_code,
                current_studies=current_studies,
                studies_url=self.site_url + "/#/studies/currently_enrolling" + studies_ga_link,
            )

            self.send_email(subject, recipients=[user.email], text_body=text_body, html_body=html_body)

            return tracking_code

    def complete_dependent_profile_prompt_email(self, user, current_studies, days):
        from flask import current_app

        with current_app.app_context(), current_app.test_request_context():
            tracking_code = self.tracking_code()

            ga_link = self.generate_google_analytics_link_content("create_dependentprofile", days)
            studies_ga_link = self.generate_google_analytics_link_content("create_dependentprofile_studies", days)
            subject = "Autism DRIVE: Complete Your Dependent's Profile"
            logo_url = self.api_url + "/api/track/" + str(user.id) + "/" + tracking_code + "/UVA_STAR-logo.png"
            text_body = render_template(
                "complete_dependent_profile_email.txt",
                profile_url=settings.SITE_URL + "/#/profile" + ga_link,
                forgot_pass_url=settings.SITE_URL + settings.FRONTEND_FORGOT_PASSWORD + ga_link,
                current_studies=current_studies,
                studies_url=self.site_url + "/#/studies/currently_enrolling" + studies_ga_link,
            )

            html_body = render_template(
                "complete_dependent_profile_email.html",
                profile_url=settings.SITE_URL + "/#/profile" + ga_link,
                forgot_pass_url=settings.SITE_URL + settings.FRONTEND_FORGOT_PASSWORD + ga_link,
                logo_url=logo_url,
                tracking_code=tracking_code,
                current_studies=current_studies,
                studies_url=self.site_url + "/#/studies/currently_enrolling" + studies_ga_link,
            )

            self.send_email(subject, recipients=[user.email], text_body=text_body, html_body=html_body)

            return tracking_code

    @staticmethod
    def generate_google_analytics_link_content(campaign, days):
        return (
            "?utm_source=email&utm_medium=referral&utm_campaign="
            + campaign
            + "&utm_content="
            + days
            + "&utm_term="
            + str(datetime.date.today())
        )


email_service = EmailService()
