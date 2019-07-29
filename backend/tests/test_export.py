import datetime
import unittest
import os

from app.import_service import ImportService
from app.model.data_transfer_log import DataTransferLog
from app.model.export_info import ExportInfoSchema

os.environ["TESTING"] = "true"

from flask import json
from tests.base_test_questionnaire import BaseTestQuestionnaire

from app import db, app
from app.email_service import TEST_MESSAGES
from app.export_service import ExportService
from app.model.participant import Relationship, Participant
from app.model.questionnaires.identification_questionnaire import IdentificationQuestionnaire

from app.model.user import Role, User
from app.schema.schema import UserSchema, ParticipantSchema
from tests.base_test import clean_db


class TestExportCase(BaseTestQuestionnaire, unittest.TestCase):

    def test_get_list_of_exportables_requires_admin(self):
        rv = self.app.get('/api/export')
        self.assertEquals(401, rv.status_code)

        headers = self.logged_in_headers(self.construct_user(email="joe@smoe.com", role=Role.user))
        rv = self.app.get('/api/export', headers=headers)
        self.assertEquals(403, rv.status_code)

    def test_get_list_of_exportables_contains_common_tables(self):
        rv = self.app.get('/api/export',
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertTrue(len(response) > 1)
        self.assertEqual(1, len(list(filter(lambda field: field['class_name'] == 'Category', response))))
        self.assertEqual(1, len(list(filter(lambda field: field['class_name'] == 'Participant', response))))
        self.assertEqual(1, len(list(filter(lambda field: field['class_name'] == 'User', response))))
        self.assertEqual(1, len(
            list(filter(lambda field: field['class_name'] == 'EvaluationHistorySelfQuestionnaire', response))))
        self.assertEqual(1, len(list(filter(lambda field: field['class_name'] == 'Category', response))))

    def test_get_list_of_exportables_has_basic_attributes(self):
        rv = self.app.get('/api/export', headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        user_data = list(filter(lambda field: field['class_name'] == 'User', response))
        self.assertTrue(len(user_data) > 0)
        self.assertEquals("/api/export/user", user_data[0]['url'])
        self.assertEquals("User", user_data[0]['class_name'])
        self.assertEquals("stardrive_user", user_data[0]['table_name'])

    def test_get_list_of_exportables_has_url_for_all_endpoints(self):
        rv = self.app.get('/api/export', headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        for entry in response:
            self.assertTrue('url' in entry, msg="No url provided for " + entry["class_name"])
            self.assertNotEqual("", entry['url'], msg="No url provided for " + entry["class_name"])

    def test_al_urls_respond_with_success(self):
        rv = self.app.get('/api/export',
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        exports = json.loads(rv.get_data(as_text=True))
        for export in exports:
            rv = self.app.get(export['url'],
                              follow_redirects=True,
                              content_type="application/json",
                              headers=self.logged_in_headers())
            self.assert_success(rv, msg="Failed to retrieve a list for " + export['class_name'])
            print("Successful export of " + export['class_name'])

    def test_user_has_no_identifying_information(self):
        rv = self.app.get('/api/export/User', headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertFalse("email" in response)
        print(response)

    def test_user_with_participant_properly_exported(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        db.session.commit()
        rv = self.app.get('/api/export/user', headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/export/participant', headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(u.id, response[0]["user_id"])

    def get_export(self):
        """Grabs everything exportable via the API, and returns it fully serialized ss json"""
        all_data = {}

        rv = self.app.get('/api/export', headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        exports = ExportInfoSchema(many=True).load(response).data
        for export in exports:
            rv = self.app.get(export.url, follow_redirects=True, content_type="application/json",
                              headers=self.logged_in_headers())
            all_data[export.class_name] = json.loads(rv.get_data(as_text=True))
        return all_data

    def load_database(self, all_data):
        rv = self.app.get('/api/export', headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        exports = ExportInfoSchema(many=True).load(response).data
        importer = ImportService(app, db)
        log = importer.log_for_export(exports, datetime.datetime.now())
        for export in exports:
            export.json_data = all_data[export.class_name]
            importer.load_data(export,log)

    def test_insert_user_with_participant(self):
        u = self.construct_user()
        u._password = b"xxxxx"
        u.email_verified = True

        role = u.role
        email_verified = u.email_verified
        orig_u_date = u.last_updated

        orig_user_dict = UserSchema().dump(u).data  # Use standard schema
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        orig_p_dict = ParticipantSchema().dump(p).data  # Use standard schema
        orig_p_date = p.last_updated
        db.session.commit()

        data = self.get_export()
        clean_db(db)
        db.session.commit()
        self.load_database(data)

        db_user = db.session.query(User).filter_by(id=orig_user_dict["id"]).first()
        self.assertIsNotNone(db_user, msg="User is recreated.")
        self.assertNotEqual(orig_user_dict["email"], db_user.email, msg="Email should be obfuscated")
        self.assertEqual(db_user.last_updated, orig_u_date, msg="Dates are kept in tact")
        self.assertEqual(db_user.role, role)
        self.assertEqual(db_user.email_verified, email_verified)
        self.assertEqual(None, db_user._password, msg="Passwords should not be exported.")

        db_par = db.session.query(Participant).filter_by(id=orig_p_dict["id"]).first()
        self.assertIsNotNone(db_par, msg="Participant is recreated.")
        self.assertEqual(db_par.user, db_user, msg="Relationship in tact")
        self.assertEqual(db_par.last_updated, orig_p_date, msg="Dates are kept in tact")

    def test_re_insert_user_with_modifications(self):
        # Construct the base user.
        u = self.construct_user()
        id = u.id
        db.session.commit()

        data = self.get_export()
        clean_db(db)
        db.session.commit()
        self.load_database(data)

        db_user = db.session.query(User).filter_by(id=id).first()
        self.assertFalse(db_user.email_verified, msg="Email should start off unverified")

        # Modify the exported data slightly, and reload
        data['User'][0]['email_verified'] = True
        self.load_database(data)
        db_user = db.session.query(User).filter_by(id=id).first()
        self.assertTrue(db_user.email_verified, msg="Email should now be verified.")

    def test_identifying_questinnaire_does_not_export(self):

        # Construct the base user.
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        iq = self.construct_identification_questionnaire(user=u, participant=p)
        id = u.id
        db.session.commit()

        data = self.get_export()
        clean_db(db)
        db.session.commit()
        self.load_database(data)

        self.assertEqual(ExportService.TYPE_IDENTIFYING,
                         IdentificationQuestionnaire().__question_type__)
        self.assertEqual(0, len(db.session.query(IdentificationQuestionnaire).all()),
                         msg="Identifying Questionnaires should not import.")

    def test_all_sensitive_exports_have_links_to_self(self):
        self.construct_everything()
        exports = ExportService.get_table_info()
        for export in exports:
            if export.question_type != ExportService.TYPE_SENSITIVE:
                continue
            rv = self.app.get(export.url, follow_redirects=True, content_type="application/json",
                              headers=self.logged_in_headers())
            data = json.loads(rv.get_data(as_text=True))
            for d in data:
                self.assertTrue('_links' in d, msg="%s should have links in json." % export.class_name)
                self.assertTrue('self' in d['_links'])
                self.assert_success(self.app.get(d['_links']['self'], headers=self.logged_in_headers()))

    def test_sensitive_records_returned_can_be_deleted(self):
        self.construct_all_questionnaires()
        exports = ExportService.get_table_info()
        for export in exports:
            rv = self.app.get(export.url, follow_redirects=True, content_type="application/json",
                              headers=self.logged_in_headers())
            data = json.loads(rv.get_data(as_text=True))
            for d in data:
                if export.question_type == ExportService.TYPE_SENSITIVE:
                    del_rv = self.app.delete(d['_links']['self'], headers=self.logged_in_headers())
                    self.assert_success(del_rv)

    def test_retrieve_records_later_than(self):
        self.construct_everything()
        #        date = datetime.datetime.now() - datetime.timedelta(minutes=5)

        date = datetime.datetime.utcnow()
        exports = ExportService.get_table_info()
        params = "?after=" + date.strftime(ExportService.DATE_FORMAT)
        for export in exports:
            rv = self.app.get(export.url + params, follow_redirects=True, content_type="application/json",
                              headers=self.logged_in_headers())
            data = json.loads(rv.get_data(as_text=True))
            self.assertEquals(0, len(data), msg=export.url + " does not respect 'after' param in get request.")

    def test_export_list_count_is_date_based(self):
        self.construct_everything()
        date = datetime.datetime.utcnow()
        params = "?after=" + date.strftime(ExportService.DATE_FORMAT)

        rv = self.app.get('/api/export', headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        for export in response:
            self.assertTrue(export['size'] > 0, msg=export['class_name'] + " should have a count > 0")

        rv = self.app.get('/api/export' + params, headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        for export in response:
            self.assertTrue(export['size'] == 0, msg=export['class_name'] + " should have a count of 0")

    def test_it_all_crazy_madness_wohoo(self):
        # Sanity check, can we load everything, export it, delete, and reload it all without error.
        self.construct_everything()
        data = self.get_export()
        clean_db(db)
        db.session.commit()
        self.load_database(data)

    def test_export_admin_details(self):
        user = self.construct_user(email="testadmin@test.com", role=Role.admin)
        user.password = "this_is_my_password!"
        db.session.add(user)
        db.session.commit()

        rv = self.app.get('/api/export/admin',
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertTrue(len(response) > 1)
        self.assertEqual(1, len(list(filter(lambda field: field['email'] == 'testadmin@test.com', response))))
        self.assertEqual(1, len(list(filter(lambda field: field['_password'] is not None, response))))

    def test_exporter_logs_export_calls(self):
        rv = self.app.get('/api/export',
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        export_logs = db.session.query(DataTransferLog).filter(DataTransferLog.type == "export").all()
        self.assertEqual(1, len(export_logs))
        self.assertIsNotNone(export_logs[0].last_updated)
        self.assertTrue(export_logs[0].total_records > 0, msg="The act of setting up this test harness should mean "
                                                                  "at least one user record is avialable for export")
        self.assertEquals(1, len(export_logs[0].details))
        detail = export_logs[0].details[0]
        self.assertEquals("User", detail.class_name)
        self.assertEquals(True, detail.successful)
        self.assertEquals(1, detail.success_count)

    def test_exporter_sends_no_email_alert_if_less_than_30_minutes_pass_without_export(self):

        message_count = len(TEST_MESSAGES)

        log = DataTransferLog(last_updated=datetime.datetime.now() - datetime.timedelta(minutes=28), total_records=2,
                              type="export")
        db.session.add(log)
        db.session.commit()
        ExportService.send_alert_if_exports_not_running()
        self.assertEqual(len(TEST_MESSAGES), message_count)

    def test_exporter_sends_email_alert_if_30_minutes_pass_without_export(self):

        message_count = len(TEST_MESSAGES)

        log = DataTransferLog(last_updated=datetime.datetime.now() - datetime.timedelta(minutes=45), total_records=2,
                              type="export")
        db.session.add(log)
        db.session.commit()

        ExportService.send_alert_if_exports_not_running()
        self.assertGreater(len(TEST_MESSAGES), message_count)
        self.assertEqual("Star Drive: Error - 45 minutes since last successful export",
                         self.decode(TEST_MESSAGES[-1]['subject']))
        ExportService.send_alert_if_exports_not_running()
        ExportService.send_alert_if_exports_not_running()
        ExportService.send_alert_if_exports_not_running()
        self.assertEqual(message_count + 1, len(TEST_MESSAGES), msg="No more messages should be sent.")
        self.assertEqual("admin@tester.com", TEST_MESSAGES[-1]['To'])

    def test_exporter_sends_second_email_after_2_hours(self):

        message_count = len(TEST_MESSAGES)

        log = DataTransferLog(last_updated=datetime.datetime.now() - datetime.timedelta(minutes=30), total_records=2,
                              type="export")
        db.session.add(log)
        db.session.commit()
        ExportService.send_alert_if_exports_not_running()
        self.assertGreater(len(TEST_MESSAGES), message_count)
        self.assertEqual("Star Drive: Error - 30 minutes since last successful export",
                         self.decode(TEST_MESSAGES[-1]['subject']))

        log.last_updated = datetime.datetime.now() - datetime.timedelta(minutes=120)
        db.session.add(log)
        db.session.commit()
        ExportService.send_alert_if_exports_not_running()
        self.assertGreater(len(TEST_MESSAGES), message_count + 1, "another email should have gone out")
        self.assertEqual("Star Drive: Error - 2 hours since last successful export",
                         self.decode(TEST_MESSAGES[-1]['subject']))

    def test_exporter_sends_12_emails_over_first_24_hours(self):
        message_count = len(TEST_MESSAGES)
        log = DataTransferLog(last_updated=datetime.datetime.now() - datetime.timedelta(hours=22),
                              total_records=2, type="export")
        db.session.add(log)
        db.session.commit()
        for i in range(20):
            ExportService.send_alert_if_exports_not_running()
        self.assertEqual(message_count + 12, len(TEST_MESSAGES), msg="12 emails should have gone out.")

    def test_exporter_sends_20_emails_over_first_48_hours(self):
        message_count = len(TEST_MESSAGES)
        log = DataTransferLog(last_updated=datetime.datetime.now() - datetime.timedelta(days=2), total_records=2,
                              type="export")
        db.session.add(log)
        db.session.commit()
        for i in range(20):
            ExportService.send_alert_if_exports_not_running()
        self.assertEqual(message_count + 20, len(TEST_MESSAGES), msg="20 emails should have gone out.")

    def test_exporter_notifies_PI_after_24_hours(self):
        message_count = len(TEST_MESSAGES)
        log = DataTransferLog(last_updated=datetime.datetime.now() - datetime.timedelta(hours=24), total_records=2,
                              type="export")
        db.session.add(log)
        db.session.commit()
        ExportService.send_alert_if_exports_not_running()
        self.assertTrue("pi@tester.com" in TEST_MESSAGES[-1]['To'])
