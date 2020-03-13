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

    def create_email_log_records(self, num_records, days_removed, log_type):
        for _ in range(num_records):
            log = EmailLog(last_updated=datetime.datetime.now() - datetime.timedelta(days=days_removed),
                           user_id=self.construct_user().id, type=log_type)
            db.session.add(log)
            db.session.commit()
            days_removed += 2

    def test_prompting_emails_sent_after_7_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(1, 6, 'confirm_email')
        self.create_email_log_records(1, 6, 'complete_registration_prompt')
        self.create_email_log_records(1, 6, 'dependent_profile_prompt')

        # Prompting email should not be sent before 7 days.
        PromptingEmails().send_confirm_prompting_emails()
        PromptingEmails().send_complete_registration_prompting_emails()
        PromptingEmails().send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(1, 8, 'confirm_email')
        self.create_email_log_records(1, 8, 'complete_registration_prompt')
        self.create_email_log_records(1, 8, 'dependent_profile_prompt')

        PromptingEmails().send_confirm_prompting_emails()
        PromptingEmails().send_complete_registration_prompting_emails()
        PromptingEmails().send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 3)
        self.assertEqual("Autism DRIVE: Complete Your Dependent's Profile", self.decode(TEST_MESSAGES[-1]['subject']))
        self.assertEqual("Autism DRIVE: Complete Your Registration", self.decode(TEST_MESSAGES[-2]['subject']))
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-3]['subject']))

    def test_prompting_emails_sent_after_14_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(2, 6, 'confirm_email')
        self.create_email_log_records(2, 6, 'complete_registration_prompt')
        self.create_email_log_records(2, 6, 'dependent_profile_prompt')

        # Prompting email should not be sent between 7 and 14 days.
        PromptingEmails().send_confirm_prompting_emails()
        PromptingEmails().send_complete_registration_prompting_emails()
        PromptingEmails().send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(2, 8, 'confirm_email')
        self.create_email_log_records(2, 8, 'complete_registration_prompt')
        self.create_email_log_records(2, 8, 'dependent_profile_prompt')

        PromptingEmails().send_confirm_prompting_emails()
        PromptingEmails().send_complete_registration_prompting_emails()
        PromptingEmails().send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 3)
        self.assertEqual("Autism DRIVE: Complete Your Dependent's Profile", self.decode(TEST_MESSAGES[-1]['subject']))
        self.assertEqual("Autism DRIVE: Complete Your Registration", self.decode(TEST_MESSAGES[-2]['subject']))
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-3]['subject']))

    def test_prompting_emails_sent_after_30_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(3, 12, 'confirm_email')
        self.create_email_log_records(3, 12, 'complete_registration_prompt')
        self.create_email_log_records(3, 12, 'dependent_profile_prompt')

        # Prompting email should not be sent between 14 and 30 days.

        PromptingEmails().send_confirm_prompting_emails()
        PromptingEmails().send_complete_registration_prompting_emails()
        PromptingEmails().send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(3, 16, 'confirm_email')
        self.create_email_log_records(3, 16, 'complete_registration_prompt')
        self.create_email_log_records(3, 16, 'dependent_profile_prompt')

        PromptingEmails().send_confirm_prompting_emails()
        PromptingEmails().send_complete_registration_prompting_emails()
        PromptingEmails().send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 3)
        self.assertEqual("Autism DRIVE: Complete Your Dependent's Profile", self.decode(TEST_MESSAGES[-1]['subject']))
        self.assertEqual("Autism DRIVE: Complete Your Registration", self.decode(TEST_MESSAGES[-2]['subject']))
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-3]['subject']))

    def test_prompting_emails_sent_after_60_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(4, 28, 'confirm_email')
        self.create_email_log_records(4, 28, 'complete_registration_prompt')
        self.create_email_log_records(4, 28, 'dependent_profile_prompt')

        # Prompting email should not be sent between 30 and 60 days.

        PromptingEmails().send_confirm_prompting_emails()
        PromptingEmails().send_complete_registration_prompting_emails()
        PromptingEmails().send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(4, 31, 'confirm_email')
        self.create_email_log_records(4, 31, 'complete_registration_prompt')
        self.create_email_log_records(4, 31, 'dependent_profile_prompt')

        PromptingEmails().send_confirm_prompting_emails()
        PromptingEmails().send_complete_registration_prompting_emails()
        PromptingEmails().send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 3)
        self.assertEqual("Autism DRIVE: Complete Your Dependent's Profile", self.decode(TEST_MESSAGES[-1]['subject']))
        self.assertEqual("Autism DRIVE: Complete Your Registration", self.decode(TEST_MESSAGES[-2]['subject']))
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-3]['subject']))

    def test_prompting_emails_sent_after_90_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(5, 28, 'confirm_email')
        self.create_email_log_records(5, 28, 'complete_registration_prompt')
        self.create_email_log_records(5, 28, 'dependent_profile_prompt')

        # Prompting email should not be sent between 60 and 90 days.

        PromptingEmails().send_confirm_prompting_emails()
        PromptingEmails().send_complete_registration_prompting_emails()
        PromptingEmails().send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(5, 31, 'confirm_email')
        self.create_email_log_records(5, 31, 'complete_registration_prompt')
        self.create_email_log_records(5, 31, 'dependent_profile_prompt')

        PromptingEmails().send_confirm_prompting_emails()
        PromptingEmails().send_complete_registration_prompting_emails()
        PromptingEmails().send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 3)
        self.assertEqual("Autism DRIVE: Complete Your Dependent's Profile", self.decode(TEST_MESSAGES[-1]['subject']))
        self.assertEqual("Autism DRIVE: Complete Your Registration", self.decode(TEST_MESSAGES[-2]['subject']))
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-3]['subject']))

    def test_prompting_emails_do_not_send_more_than_5_times_total(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(6, 31, 'confirm_email')
        self.create_email_log_records(6, 31, 'complete_registration_prompt')
        self.create_email_log_records(6, 31, 'dependent_profile_prompt')

        PromptingEmails().send_confirm_prompting_emails()
        PromptingEmails().send_complete_registration_prompting_emails()
        PromptingEmails().send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
