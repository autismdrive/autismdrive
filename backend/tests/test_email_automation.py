import smtplib
from typing import Literal
from unittest.mock import MagicMock, patch

from app.utils import utcnow

from tests.base_test_questionnaire import BaseTestQuestionnaire  # isort:skip
import datetime
import uuid

from fixtures.fixture_utils import fake
from sqlalchemy import select
from sqlalchemy.orm import joinedload, make_transient

from app.email_prompt_service import EmailPromptService
from app.enums import Relationship
from app.models import EmailLog, Study, User
from app.resources.UserEndpoint import get_user_by_id


class TestEmailPromptService(BaseTestQuestionnaire):
    email_prompt_service = EmailPromptService(EmailLog, Study, User)

    def create_email_log_records(
        self,
        num_records: int,
        days_removed: int,
        log_type: Literal["confirm_email", "complete_registration_prompt", "dependent_profile_prompt"],
        user=None,
    ):
        """
        Adds the given number of past email log records, 2 days apart, with the given initial offset,
        to the database for testing purposes.

        :param num_records: Number of past email log records to create.
        :param days_removed: Number of days before the first record.
        :param log_type: Type of email log ("confirm_email" or "dependent_profile_prompt").
        :param user: User object to associate with the email logs. If None, uses the default user.

        Example:
        The following would create 3 email log records, each 2 days apart, with an initial offset
        of 10 days (i.e., 10, 12, & 14 days ago):
        ``create_email_log_records(3, 10, "confirm_email", user)``
        """

        if user is None:
            user = self.default_user

        u_id = int(f"{user.id}")

        for _ in range(num_records):
            log = EmailLog(
                last_updated=utcnow() - datetime.timedelta(days=days_removed),
                user_id=u_id,
                type=log_type,
                tracking_code=str(uuid.uuid4())[:16],
            )
            self.session.add(log)
            self.session.commit()
            days_removed += 2

    def create_complete_guardian(self):
        u1 = self.construct_user(email=fake.email(), last_login=fake.past_datetime())
        p1 = self.construct_participant(user_id=u1.id, relationship=Relationship.self_guardian)
        q1 = {"user_id": u1.id, "participant_id": p1.id}
        jq1 = self.jsonify(q1)
        headers = self.logged_in_headers(u1.id)
        r1 = self.client.post(
            "api/flow/guardian_intake/identification_questionnaire",
            data=jq1,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(r1, "create_complete_guardian > r1")

        r2 = self.client.post(
            "api/flow/guardian_intake/contact_questionnaire",
            data=jq1,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(r2, "create_complete_guardian > r2")

        r3 = self.client.post(
            "api/flow/guardian_intake/demographics_questionnaire",
            data=jq1,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(r3, "create_complete_guardian > r3")

        db_user = (
            self.session.execute(select(User).options(joinedload(User.participants)).filter_by(id=u1.id))
            .unique()
            .scalar_one()
        )
        self.assertTrue(db_user.self_registration_complete())
        make_transient(db_user)
        self.session.close()
        return db_user

    @patch("smtplib.SMTP", autospec=True)
    def test_prompting_emails_sent_after_7_days(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail

        # Create a new user who just logged in today.
        user = self.construct_user(email=fake.email())

        mock_sendmail.assert_not_called()

        # If we sent the user an email 6 days ago, prompting email should NOT be sent.
        self.create_email_log_records(num_records=1, days_removed=6, log_type="confirm_email", user=user)
        self.email_prompt_service.send_confirm_prompting_emails()
        mock_sendmail.assert_not_called()

        self.session.query(EmailLog).delete()
        self.session.commit()

        # If we sent the user an email 8 days ago, a prompting email should be sent.
        self.create_email_log_records(num_records=1, days_removed=8, log_type="confirm_email", user=user)
        self.email_prompt_service.send_confirm_prompting_emails()
        self.assert_email_sent(mock_sendmail, user.email, "Autism DRIVE: Confirm Email")

    @patch("smtplib.SMTP", autospec=True)
    def test_prompting_emails_sent_after_14_days(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        user = self.construct_user(email=fake.email())

        # If we already sent the user 2 emails 6 & 8 days ago, prompting email should NOT be sent.
        self.create_email_log_records(2, 6, "confirm_email", user=user)
        self.email_prompt_service.send_confirm_prompting_emails()
        mock_sendmail.assert_not_called()

        self.session.query(EmailLog).delete()
        self.session.commit()

        # If we already sent the user 2 emails 8 & 10 days ago, prompting email should be sent.
        self.create_email_log_records(2, 8, "confirm_email", user=user)
        self.email_prompt_service.send_confirm_prompting_emails()
        self.assert_email_sent(
            mock_sendmail=mock_sendmail,
            expected_recipient=user.email,
            expected_subject="Autism DRIVE: Confirm Email",
        )

    @patch("smtplib.SMTP", autospec=True)
    def test_prompting_emails_sent_after_30_days(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        user = self.construct_user(email=fake.email())

        # With 3 records at 10, 12, and 14 days ago, prompting email should NOT be sent.
        self.create_email_log_records(3, 10, "confirm_email", user=user)
        self.email_prompt_service.send_confirm_prompting_emails()
        mock_sendmail.assert_not_called()
        self.session.query(EmailLog).delete()
        self.session.commit()

        # With 3 records at 17, 19, and 21 days ago, prompting email should be sent.
        self.create_email_log_records(3, 17, "confirm_email", user=user)
        self.email_prompt_service.send_confirm_prompting_emails()
        self.assert_email_sent(
            mock_sendmail=mock_sendmail,
            expected_recipient=user.email,
            expected_subject="Autism DRIVE: Confirm Email",
        )

    @patch("smtplib.SMTP", autospec=True)
    def test_prompting_emails_sent_after_60_days(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        user = self.construct_user(email=fake.email())

        self.create_email_log_records(4, 28, "confirm_email", user=user)

        # Prompting email should not be sent between 30 and 60 days.

        self.email_prompt_service.send_confirm_prompting_emails()
        mock_sendmail.assert_not_called()
        self.session.query(EmailLog).delete()
        self.session.commit()

        self.create_email_log_records(4, 31, "confirm_email", user=user)

        self.email_prompt_service.send_confirm_prompting_emails()
        self.assert_email_sent(mock_sendmail, user.email, "Autism DRIVE: Confirm Email")

    @patch("smtplib.SMTP", autospec=True)
    def test_prompting_emails_sent_after_90_days(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        user = self.construct_user(email=fake.email())

        self.create_email_log_records(5, 28, "confirm_email", user)

        # Prompting email should not be sent between 60 and 90 days.

        self.email_prompt_service.send_confirm_prompting_emails()
        mock_sendmail.assert_not_called()
        self.session.query(EmailLog).delete()
        self.session.commit()

        self.create_email_log_records(5, 31, "confirm_email", user=user)

        self.email_prompt_service.send_confirm_prompting_emails()
        self.assert_email_sent(mock_sendmail, user.email, "Autism DRIVE: Confirm Email")

    @patch("smtplib.SMTP", autospec=True)
    def test_prompting_emails_do_not_send_more_than_5_times_total(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        user = self.construct_user(email=fake.email())

        self.create_email_log_records(6, 31, "confirm_email")

        self.email_prompt_service.send_confirm_prompting_emails()
        mock_sendmail.assert_not_called()

    @patch("smtplib.SMTP", autospec=True)
    def test_self_registration_prompting_email(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        u1 = self.construct_user(email=fake.email())
        u1_id = u1.id
        headers_u1 = self.logged_in_headers(user_id=u1_id)
        p1 = self.construct_participant(user_id=u1_id, relationship=Relationship.self_guardian)
        p1_id = p1.id
        q1 = {"user_id": u1_id, "participant_id": p1_id}
        self.client.post(
            "api/flow/guardian_intake/identification_questionnaire",
            data=self.jsonify(q1),
            content_type="application/json",
            follow_redirects=True,
            headers=headers_u1,
        )

        self.client.post(
            "api/flow/guardian_intake/contact_questionnaire",
            data=self.jsonify(q1),
            content_type="application/json",
            follow_redirects=True,
            headers=headers_u1,
        )

        self.client.post(
            "api/flow/guardian_intake/demographics_questionnaire",
            data=self.jsonify(q1),
            content_type="application/json",
            follow_redirects=True,
            headers=headers_u1,
        )

        db_u1 = get_user_by_id(u1_id)
        self.assertTrue(db_u1.self_registration_complete())
        self.session.close()

        u2 = self.construct_user(email="test2@sartography.com", last_login="12/4/19 10:00")
        u2_id = u2.id
        headers_u2 = self.logged_in_headers(user_id=u2_id)
        p2 = self.construct_participant(user_id=u2.id, relationship=Relationship.self_guardian)
        p2_id = p2.id
        q2 = {"user_id": u2_id, "participant_id": p2_id}
        q2_json = self.jsonify(q2)
        self.client.post(
            "api/flow/guardian_intake/identification_questionnaire",
            data=q2_json,
            content_type="application/json",
            follow_redirects=True,
            headers=headers_u2,
        )

        self.client.post(
            "api/flow/guardian_intake/contact_questionnaire",
            data=q2_json,
            content_type="application/json",
            follow_redirects=True,
            headers=headers_u2,
        )

        db_u2 = get_user_by_id(u2_id)
        self.assertFalse(db_u2.self_registration_complete())
        self.session.close()

        # Set the users' last login dates to 2 days ago.
        self._back_date_last_login(u1_id, 2)
        self._back_date_last_login(u2_id, 2)

        mock_sendmail.reset_mock()
        self.email_prompt_service.send_complete_registration_prompting_emails()
        self.assert_email_sent(mock_sendmail, f"{db_u2.email}", "Autism DRIVE: Complete Your Registration")

    @patch("smtplib.SMTP", autospec=True)
    def test_dependent_profile_sends_prompt_with_no_dependent(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        u1 = self.create_complete_guardian()

        # Set the user's last login date to 2 days ago.
        self._back_date_last_login(u1.id, 2)

        mock_sendmail.reset_mock()
        self.email_prompt_service.send_dependent_profile_prompting_emails()
        self.assert_email_sent(mock_sendmail, f"{u1.email}", "Autism DRIVE: Complete Your Dependent's Profile")

    @patch("smtplib.SMTP", autospec=True)
    def test_dependent_profile_sends_scheduled_prompt_with_no_dependent(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        u1 = self.create_complete_guardian()

        self.create_email_log_records(5, 28, "dependent_profile_prompt", user=u1)

        # Prompting email should not be sent between 60 and 90 days.

        self.email_prompt_service.send_dependent_profile_prompting_emails()
        mock_sendmail.assert_not_called()
        self.session.query(EmailLog).delete()
        self.session.commit()

        self.create_email_log_records(5, 31, "dependent_profile_prompt", user=u1)

        mock_sendmail.reset_mock()
        self.email_prompt_service.send_dependent_profile_prompting_emails()
        self.assert_email_sent(mock_sendmail, f"{u1.email}", "Autism DRIVE: Complete Your Dependent's Profile")

    @patch("smtplib.SMTP", autospec=True)
    def test_dependent_profile_sends_prompt_with_incomplete_dependent(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        u1 = self.create_complete_guardian()
        u1_id = u1.id
        d1 = self.construct_participant(user_id=u1_id, relationship=Relationship.dependent)
        d1_id = d1.id
        q1 = {"user_id": u1_id, "participant_id": d1_id}
        rv = self.client.post(
            "api/flow/dependent_intake/developmental_questionnaire",
            data=self.jsonify(q1),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(u1_id),
        )
        self.assert_success(rv)

        user = self.construct_user(email=fake.email())

        # Set the user's last login date to 2 days ago.
        self._back_date_last_login(u1_id, 2)

        mock_sendmail.reset_mock()
        self.email_prompt_service.send_dependent_profile_prompting_emails()
        self.assert_email_sent(mock_sendmail, f"{u1.email}", "Autism DRIVE: Complete Your Dependent's Profile")

    @patch("smtplib.SMTP", autospec=True)
    def test_dependent_profile_does_not_send_prompt_with_complete_dependent(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        u1 = self.create_complete_guardian()
        u1_id = u1.id
        d1 = self.construct_participant(user_id=u1.id, relationship=Relationship.dependent)
        d1_id = d1.id
        q1 = {"user_id": u1_id, "participant_id": d1_id}
        q1_json = self.jsonify(q1)
        headers = self.logged_in_headers(u1.id)
        rv = self.client.post(
            "api/flow/dependent_intake/identification_questionnaire",
            data=q1_json,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)
        rv = self.client.post(
            "api/flow/dependent_intake/demographics_questionnaire",
            data=q1_json,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)
        rv = self.client.post(
            "api/flow/dependent_intake/home_dependent_questionnaire",
            data=q1_json,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)
        rv = self.client.post(
            "api/flow/dependent_intake/evaluation_history_dependent_questionnaire",
            data=q1_json,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)
        rv = self.client.post(
            "api/flow/dependent_intake/clinical_diagnoses_questionnaire",
            data=q1_json,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)
        rv = self.client.post(
            "api/flow/dependent_intake/developmental_questionnaire",
            data=q1_json,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)
        rv = self.client.post(
            "api/flow/dependent_intake/current_behaviors_dependent_questionnaire",
            data=q1_json,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)
        rv = self.client.post(
            "api/flow/dependent_intake/education_dependent_questionnaire",
            data=q1_json,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)
        rv = self.client.post(
            "api/flow/dependent_intake/supports_questionnaire",
            data=q1_json,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)

        mock_sendmail.reset_mock()
        self.email_prompt_service.send_dependent_profile_prompting_emails()
        mock_sendmail.assert_not_called()

    @patch("smtplib.SMTP", autospec=True)
    def test_self_participants_that_are_not_their_own_legal_guardians_do_not_get_reminders(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        u2 = self.construct_user(email=fake.email(), last_login=fake.past_datetime())
        u2._password = bytes(fake.password(), "utf-8")
        user_meta = self.construct_user_meta(user_id=u2.id)
        user_meta.self_participant = True
        user_meta.self_has_guardian = True
        self.session.merge(user_meta)
        self.session.commit()
        self.session.close()

        # Assure no new messages to go out to this individual who is not their own legal guardian.
        self.email_prompt_service.send_complete_registration_prompting_emails()
        mock_sendmail.assert_not_called()

    def _back_date_last_login(self, user_id, days):
        db_user = get_user_by_id(user_id)
        db_user.last_login = utcnow() - datetime.timedelta(days=days)
        self.session.commit()
        self.session.close()
