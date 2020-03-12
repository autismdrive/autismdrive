import datetime
import unittest
import os

from app.model.email_log import EmailLog

os.environ["TESTING"] = "true"

from tests.base_test_questionnaire import BaseTestQuestionnaire
from app import db, app
from app.email_service import TEST_MESSAGES
from app.prompting_emails import PromptingEmails


class TestExportCase(BaseTestQuestionnaire, unittest.TestCase):

    def create_email_log_records(self, num_records, days_removed):
        for _ in range(num_records):
            log = EmailLog(last_updated=datetime.datetime.now() - datetime.timedelta(days=days_removed),
                           user_id=self.construct_user().id, type="confirm_email")
            db.session.add(log)
            db.session.commit()
            days_removed += 2

    def test_confirm_email_followup_sent_after_7_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(1, 6)

        # Prompting email should not be sent before 7 days.
        PromptingEmails().send_set_password_prompts()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(1, 8)

        PromptingEmails().send_set_password_prompts()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-1]['subject']))

    def test_confirm_email_followup_sent_after_14_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(2, 6)

        # Prompting email should not be sent between 7 and 14 days.
        PromptingEmails().send_set_password_prompts()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(2, 8)

        PromptingEmails().send_set_password_prompts()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-1]['subject']))

    def test_confirm_email_followup_sent_after_30_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(3, 12)

        # Prompting email should not be sent between 14 and 30 days.
        PromptingEmails().send_set_password_prompts()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(3, 16)

        PromptingEmails().send_set_password_prompts()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-1]['subject']))

    def test_confirm_email_followup_sent_after_60_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(4, 28)

        # Prompting email should not be sent between 30 and 60 days.
        PromptingEmails().send_set_password_prompts()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(4, 31)

        PromptingEmails().send_set_password_prompts()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-1]['subject']))

    def test_confirm_email_followup_sent_after_90_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(5, 28)

        # Prompting email should not be sent between 60 and 90 days.
        PromptingEmails().send_set_password_prompts()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(5, 31)

        PromptingEmails().send_set_password_prompts()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-1]['subject']))

    def test_confirm_email_does_not_send_more_than_5_times_total(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(6, 31)

        PromptingEmails().send_set_password_prompts()
        self.assertEqual(len(TEST_MESSAGES), message_count)