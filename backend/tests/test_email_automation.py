import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.email_prompt_service import EmailPromptService
from app.email_service import EmailService
from app.models import EmailLog, Study, User
from app.enums import Relationship
from app.resources.UserEndpoint import get_user_by_id
from fixtures.fixure_utils import fake
from tests.base_test_questionnaire import BaseTestQuestionnaire


class TestEmailPromptService(BaseTestQuestionnaire):
    email_prompt_service = EmailPromptService(EmailLog, Study, User)

    def create_email_log_records(self, num_records, days_removed, log_type, user=None):
        if user is None:
            user = self.construct_user()
        for _ in range(num_records):
            log = EmailLog(
                last_updated=datetime.datetime.now() - datetime.timedelta(days=days_removed),
                user_id=user.id,
                type=log_type,
                tracking_code=str(uuid.uuid4())[:16],
            )
            self.session.add(log)
            self.session.commit()
            days_removed += 2

    def create_complete_guardian(self):
        u1 = self.construct_user(email="test1@sartography.com", last_login="12/4/19 10:00")
        p1 = self.construct_participant(user_id=u1.id, relationship=Relationship.self_guardian)
        q1 = {"user_id": u1.id, "participant_id": p1.id}
        self.client.post(
            "api/flow/guardian_intake/identification_questionnaire",
            data=self.jsonify(q1),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(u1.id),
        )

        self.client.post(
            "api/flow/guardian_intake/contact_questionnaire",
            data=self.jsonify(q1),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(u1.id),
        )

        self.client.post(
            "api/flow/guardian_intake/demographics_questionnaire",
            data=self.jsonify(q1),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(u1.id),
        )

        db_user = (
            self.session.execute(select(User).options(joinedload(User.participants)).filter_by(id=u1.id))
            .unique()
            .scalar_one()
        )
        self.assertTrue(db_user.self_registration_complete())
        self.session.close()
        return db_user

    def test_prompting_emails_sent_after_7_days(self):
        message_count = len(EmailService.TEST_MESSAGES)

        self.create_email_log_records(1, 6, "confirm_email")

        # Prompting email should not be sent before 7 days.
        self.email_prompt_service.send_confirm_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count)
        self.session.query(EmailLog).delete()
        self.session.commit()

        self.create_email_log_records(1, 8, "confirm_email")

        self.email_prompt_service.send_confirm_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(EmailService.TEST_MESSAGES[-1]["subject"]))

    def test_prompting_emails_sent_after_14_days(self):
        message_count = len(EmailService.TEST_MESSAGES)

        self.create_email_log_records(2, 6, "confirm_email")

        # Prompting email should not be sent between 7 and 14 days.
        self.email_prompt_service.send_confirm_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count)
        self.session.query(EmailLog).delete()
        self.session.commit()

        self.create_email_log_records(2, 8, "confirm_email")

        self.email_prompt_service.send_confirm_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(EmailService.TEST_MESSAGES[-1]["subject"]))

    def test_prompting_emails_sent_after_30_days(self):
        message_count = len(EmailService.TEST_MESSAGES)

        self.create_email_log_records(3, 12, "confirm_email")

        # Prompting email should not be sent between 14 and 30 days.

        self.email_prompt_service.send_confirm_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count)
        self.session.query(EmailLog).delete()
        self.session.commit()

        self.create_email_log_records(3, 17, "confirm_email")

        self.email_prompt_service.send_confirm_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(EmailService.TEST_MESSAGES[-1]["subject"]))

    def test_prompting_emails_sent_after_60_days(self):
        message_count = len(EmailService.TEST_MESSAGES)

        self.create_email_log_records(4, 28, "confirm_email")

        # Prompting email should not be sent between 30 and 60 days.

        self.email_prompt_service.send_confirm_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count)
        self.session.query(EmailLog).delete()
        self.session.commit()

        self.create_email_log_records(4, 31, "confirm_email")

        self.email_prompt_service.send_confirm_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(EmailService.TEST_MESSAGES[-1]["subject"]))

    def test_prompting_emails_sent_after_90_days(self):
        message_count = len(EmailService.TEST_MESSAGES)

        self.create_email_log_records(5, 28, "confirm_email")

        # Prompting email should not be sent between 60 and 90 days.

        self.email_prompt_service.send_confirm_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count)
        self.session.query(EmailLog).delete()
        self.session.commit()

        self.create_email_log_records(5, 31, "confirm_email")

        self.email_prompt_service.send_confirm_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(EmailService.TEST_MESSAGES[-1]["subject"]))

    def test_prompting_emails_do_not_send_more_than_5_times_total(self):
        message_count = len(EmailService.TEST_MESSAGES)

        self.create_email_log_records(6, 31, "confirm_email")

        self.email_prompt_service.send_confirm_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count)

    def test_self_registration_prompting_email(self):
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

        message_count = len(EmailService.TEST_MESSAGES)

        # Set the users' last login dates to 2 days ago.
        self._back_date_last_login(u1_id, 2)
        self._back_date_last_login(u2_id, 2)

        self.email_prompt_service.send_complete_registration_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count + 1)
        self.assertEqual(
            "Autism DRIVE: Complete Your Registration", self.decode(EmailService.TEST_MESSAGES[-1]["subject"])
        )
        self.assertEqual("test2@sartography.com", EmailService.TEST_MESSAGES[-1]["To"])

    def test_dependent_profile_sends_prompt_with_no_dependent(self):
        u1 = self.create_complete_guardian()

        message_count = len(EmailService.TEST_MESSAGES)

        # Set the user's last login date to 2 days ago.
        self._back_date_last_login(u1.id, 2)

        self.email_prompt_service.send_dependent_profile_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count + 1)
        self.assertEqual(
            "Autism DRIVE: Complete Your Dependent's Profile", self.decode(EmailService.TEST_MESSAGES[-1]["subject"])
        )
        self.assertEqual(u1.email, EmailService.TEST_MESSAGES[-1]["To"])

    def test_dependent_profile_sends_scheduled_prompt_with_no_dependent(self):
        u1 = self.create_complete_guardian()
        message_count = len(EmailService.TEST_MESSAGES)

        self.create_email_log_records(5, 28, "dependent_profile_prompt", user=u1)

        # Prompting email should not be sent between 60 and 90 days.

        self.email_prompt_service.send_dependent_profile_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count)
        self.session.query(EmailLog).delete()
        self.session.commit()

        self.create_email_log_records(5, 31, "dependent_profile_prompt", user=u1)

        self.email_prompt_service.send_dependent_profile_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count + 1)
        self.assertEqual(
            "Autism DRIVE: Complete Your Dependent's Profile", self.decode(EmailService.TEST_MESSAGES[-1]["subject"])
        )
        self.assertEqual(u1.email, EmailService.TEST_MESSAGES[-1]["To"])

    def test_dependent_profile_sends_prompt_with_incomplete_dependent(self):
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

        message_count = len(EmailService.TEST_MESSAGES)

        # Set the user's last login date to 2 days ago.
        self._back_date_last_login(u1_id, 2)

        self.email_prompt_service.send_dependent_profile_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count + 1)
        self.assertEqual(
            "Autism DRIVE: Complete Your Dependent's Profile", self.decode(EmailService.TEST_MESSAGES[-1]["subject"])
        )
        self.assertEqual(u1.email, EmailService.TEST_MESSAGES[-1]["To"])

    def test_dependent_profile_does_not_send_prompt_with_complete_dependent(self):
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

        message_count_before = len(EmailService.TEST_MESSAGES)

        self.email_prompt_service.send_dependent_profile_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count_before)

    def test_self_participants_that_are_not_their_own_legal_guardians_do_not_get_reminders(self):
        u2 = self.construct_user(email="test2@sartography.com", last_login="12/4/19 10:00")
        u2._password = b"123412"
        user_meta = self.construct_user_meta(user_id=u2.id)

        user_meta.self_participant = True
        user_meta.self_has_guardian = True
        self.session.add(user_meta)
        self.session.commit()
        self.session.close()

        # Assure no new messages to go out to this individual who is not their own legal guardian.
        message_count = len(EmailService.TEST_MESSAGES)
        self.email_prompt_service.send_complete_registration_prompting_emails()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count)

    def _back_date_last_login(self, user_id, days):
        db_user = get_user_by_id(user_id)
        db_user.last_login = datetime.datetime.now() - datetime.timedelta(days=days)
        self.session.commit()
        self.session.close()
