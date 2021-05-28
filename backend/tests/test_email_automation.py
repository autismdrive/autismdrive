import datetime
import unittest
import os
from flask import json

os.environ["TESTING"] = "true"

from tests.base_test_questionnaire import BaseTestQuestionnaire
from app import app, db
from app.model.email_log import EmailLog
from app.model.participant import Relationship
from app.model.study import Study
from app.model.user import User
from app.email_service import TEST_MESSAGES
from app.email_prompt_service import EmailPromptService


class TestExportCase(BaseTestQuestionnaire, unittest.TestCase):

    def create_email_log_records(self, num_records, days_removed, log_type, user=None):
        if user is None:
            user = self.construct_user()
        for _ in range(num_records):
            log = EmailLog(last_updated=datetime.datetime.now() - datetime.timedelta(days=days_removed),
                           user_id=user.id, type=log_type)
            db.session.add(log)
            db.session.commit()
            days_removed += 2

    def create_complete_guardian(self):
        u1 = self.construct_user(email='test1@sartography.com', last_login='12/4/19 10:00')
        p1 = self.construct_participant(user=u1, relationship=Relationship.self_guardian)
        q1 = {
            'user_id': u1.id,
            'participant_id': p1.id
        }
        self.app.post('api/flow/guardian_intake/identification_questionnaire', data=self.jsonify(q1),
                      content_type="application/json",
                      follow_redirects=True, headers=self.logged_in_headers(u1))

        self.app.post('api/flow/guardian_intake/contact_questionnaire', data=self.jsonify(q1),
                      content_type="application/json",
                      follow_redirects=True, headers=self.logged_in_headers(u1))

        self.app.post('api/flow/guardian_intake/demographics_questionnaire', data=self.jsonify(q1),
                      content_type="application/json",
                      follow_redirects=True, headers=self.logged_in_headers(u1))

        self.assertTrue(u1.self_registration_complete())
        return u1

    def test_prompting_emails_sent_after_7_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(1, 6, 'confirm_email')

        # Prompting email should not be sent before 7 days.
        EmailPromptService(app, db, EmailLog, Study, User).send_confirm_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(1, 8, 'confirm_email')

        EmailPromptService(app, db, EmailLog, Study, User).send_confirm_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-1]['subject']))

    def test_prompting_emails_sent_after_14_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(2, 6, 'confirm_email')

        # Prompting email should not be sent between 7 and 14 days.
        EmailPromptService(app, db, EmailLog, Study, User).send_confirm_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(2, 8, 'confirm_email')

        EmailPromptService(app, db, EmailLog, Study, User).send_confirm_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-1]['subject']))

    def test_prompting_emails_sent_after_30_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(3, 12, 'confirm_email')

        # Prompting email should not be sent between 14 and 30 days.

        EmailPromptService(app, db, EmailLog, Study, User).send_confirm_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(3, 17, 'confirm_email')

        EmailPromptService(app, db, EmailLog, Study, User).send_confirm_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-1]['subject']))

    def test_prompting_emails_sent_after_60_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(4, 28, 'confirm_email')

        # Prompting email should not be sent between 30 and 60 days.

        EmailPromptService(app, db, EmailLog, Study, User).send_confirm_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(4, 31, 'confirm_email')

        EmailPromptService(app, db, EmailLog, Study, User).send_confirm_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-1]['subject']))

    def test_prompting_emails_sent_after_90_days(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(5, 28, 'confirm_email')

        # Prompting email should not be sent between 60 and 90 days.

        EmailPromptService(app, db, EmailLog, Study, User).send_confirm_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(5, 31, 'confirm_email')

        EmailPromptService(app, db, EmailLog, Study, User).send_confirm_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(TEST_MESSAGES[-1]['subject']))

    def test_prompting_emails_do_not_send_more_than_5_times_total(self):
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(6, 31, 'confirm_email')

        EmailPromptService(app, db, EmailLog, Study, User).send_confirm_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)

    def test_self_registration_prompting_email(self):
        u1 = self.construct_user(email='test1@sartography.com')
        p1 = self.construct_participant(user=u1, relationship=Relationship.self_guardian)
        q1 = {
            'user_id': u1.id,
            'participant_id': p1.id
        }
        self.app.post('api/flow/guardian_intake/identification_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))

        self.app.post('api/flow/guardian_intake/contact_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))

        self.app.post('api/flow/guardian_intake/demographics_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))

        self.assertTrue(u1.self_registration_complete())

        u2 = self.construct_user(email='test2@sartography.com', last_login="12/4/19 10:00")
        p2 = self.construct_participant(user=u2, relationship=Relationship.self_guardian)
        q2 = {
            'user_id': u2.id,
            'participant_id': p2.id
        }
        self.app.post('api/flow/guardian_intake/identification_questionnaire', data=self.jsonify(q2),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u2))

        self.app.post('api/flow/guardian_intake/contact_questionnaire', data=self.jsonify(q2),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u2))

        self.assertFalse(u2.self_registration_complete())

        message_count = len(TEST_MESSAGES)

        EmailPromptService(app, db, EmailLog, Study, User).send_complete_registration_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Complete Your Registration", self.decode(TEST_MESSAGES[-1]['subject']))
        self.assertEqual("test2@sartography.com", TEST_MESSAGES[-1]['To'])

    def test_dependent_profile_sends_prompt_with_no_dependent(self):
        u1 = self.create_complete_guardian()

        message_count = len(TEST_MESSAGES)

        EmailPromptService(app, db, EmailLog, Study, User).send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Complete Your Dependent's Profile", self.decode(TEST_MESSAGES[-1]['subject']))
        self.assertEqual(u1.email, TEST_MESSAGES[-1]['To'])

    def test_dependent_profile_sends_scheduled_prompt_with_no_dependent(self):
        u1 = self.create_complete_guardian()
        message_count = len(TEST_MESSAGES)

        self.create_email_log_records(5, 28, 'dependent_profile_prompt', user=u1)

        # Prompting email should not be sent between 60 and 90 days.

        EmailPromptService(app, db, EmailLog, Study, User).send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
        db.session.query(EmailLog).delete()
        db.session.commit()

        self.create_email_log_records(5, 31, 'dependent_profile_prompt', user=u1)

        EmailPromptService(app, db, EmailLog, Study, User).send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Complete Your Dependent's Profile", self.decode(TEST_MESSAGES[-1]['subject']))
        self.assertEqual(u1.email, TEST_MESSAGES[-1]['To'])

    def test_dependent_profile_sends_prompt_with_incomplete_dependent(self):
        u1 = self.create_complete_guardian()
        d1 = self.construct_participant(user=u1, relationship=Relationship.dependent)
        q1 = {
            'user_id': u1.id,
            'participant_id': d1.id
        }
        rv = self.app.post('api/flow/dependent_intake/developmental_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))
        self.assert_success(rv)

        message_count = len(TEST_MESSAGES)

        EmailPromptService(app, db, EmailLog, Study, User).send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count + 1)
        self.assertEqual("Autism DRIVE: Complete Your Dependent's Profile", self.decode(TEST_MESSAGES[-1]['subject']))
        self.assertEqual(u1.email, TEST_MESSAGES[-1]['To'])

    def test_dependent_profile_does_not_send_prompt_with_complete_dependent(self):
        u1 = self.create_complete_guardian()
        d1 = self.construct_participant(user=u1, relationship=Relationship.dependent)
        q1 = {
            'user_id': u1.id,
            'participant_id': d1.id
        }
        rv = self.app.post('api/flow/dependent_intake/identification_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))
        self.assert_success(rv)
        rv = self.app.post('api/flow/dependent_intake/demographics_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))
        self.assert_success(rv)
        rv = self.app.post('api/flow/dependent_intake/home_dependent_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))
        self.assert_success(rv)
        rv = self.app.post('api/flow/dependent_intake/evaluation_history_dependent_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))
        self.assert_success(rv)
        rv = self.app.post('api/flow/dependent_intake/clinical_diagnoses_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))
        self.assert_success(rv)
        rv = self.app.post('api/flow/dependent_intake/developmental_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))
        self.assert_success(rv)
        rv = self.app.post('api/flow/dependent_intake/current_behaviors_dependent_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))
        self.assert_success(rv)
        rv = self.app.post('api/flow/dependent_intake/education_dependent_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))
        self.assert_success(rv)
        rv = self.app.post('api/flow/dependent_intake/supports_questionnaire', data=self.jsonify(q1),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u1))
        self.assert_success(rv)

        message_count = len(TEST_MESSAGES)

        EmailPromptService(app, db, EmailLog, Study, User).send_dependent_profile_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)

    def test_self_participants_that_are_not_their_own_legal_guardians_do_not_get_reminders(self):
        u2 = self.construct_user(email='test2@sartography.com', last_login="12/4/19 10:00")
        u2._password = b'123412'
        user_meta = self.construct_usermeta(user=u2)
        user_meta.self_participant = True
        user_meta.self_has_guardian = True

        # Assure no new messages to go out to this individual who is not their own legal guardian.
        message_count = len(TEST_MESSAGES)
        EmailPromptService(app, db, EmailLog, Study, User).send_complete_registration_prompting_emails()
        self.assertEqual(len(TEST_MESSAGES), message_count)
