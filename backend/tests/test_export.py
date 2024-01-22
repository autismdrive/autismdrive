import os
import time

os.environ["TESTING"] = "true"
os.environ["ENV_NAME"] = "testing"

import datetime
import tzlocal
from flask import json
from sqlalchemy import cast, Integer, select

from tests.base_test_questionnaire import BaseTestQuestionnaire
from app.email_service import EmailService
from app.enums import Relationship, Role
from app.export_service import ExportService
from app.import_service import ImportService
from app.models import DataTransferLog, Participant, User, IdentificationQuestionnaire
from app.schemas import ExportInfoSchema, UserSchema, ParticipantSchema


class TestExportCase(BaseTestQuestionnaire):
    def get_local_now(self):
        return datetime.datetime.now(tz=tzlocal.get_localzone())

    def test_get_list_of_exportables_requires_admin(self):
        rv = self.client.get("/api/export")
        self.assertEqual(401, rv.status_code)

        headers = self.logged_in_headers(self.construct_user(email="joe@smoe.com", role=Role.user))
        rv = self.client.get("/api/export", headers=headers)
        self.assertEqual(403, rv.status_code)

    def test_get_list_of_exportables_contains_common_tables(self):
        rv = self.client.get(
            "/api/export", follow_redirects=True, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertTrue(len(response) > 1)
        self.assertEqual(1, len(list(filter(lambda field: field["class_name"] == "Category", response))))
        self.assertEqual(1, len(list(filter(lambda field: field["class_name"] == "Participant", response))))
        self.assertEqual(1, len(list(filter(lambda field: field["class_name"] == "User", response))))
        self.assertEqual(
            1, len(list(filter(lambda field: field["class_name"] == "EvaluationHistorySelfQuestionnaire", response)))
        )
        self.assertEqual(1, len(list(filter(lambda field: field["class_name"] == "Category", response))))

    def test_get_list_of_exportables_has_basic_attributes(self):
        rv = self.client.get("/api/export", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        user_data = list(filter(lambda field: field["class_name"] == "User", response))
        self.assertTrue(len(user_data) > 0)
        self.assertEqual("/api/export/user", user_data[0]["url"])
        self.assertEqual("User", user_data[0]["class_name"])
        self.assertEqual("stardrive_user", user_data[0]["table_name"])

    def test_get_list_of_exportables_has_url_for_all_endpoints(self):
        rv = self.client.get("/api/export", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        for entry in response:
            self.assertTrue("url" in entry, msg="No url provided for " + entry["class_name"])
            self.assertNotEqual("", entry["url"], msg="No url provided for " + entry["class_name"])

    def test_all_urls_respond_with_success(self):
        rv = self.client.get(
            "/api/export", follow_redirects=True, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        exports = rv.json
        for export in exports:
            rv = self.client.get(
                export["url"], follow_redirects=True, content_type="application/json", headers=self.logged_in_headers()
            )
            self.assert_success(rv, msg="Failed to retrieve a list for " + export["class_name"])
            print("Successful export of " + export["class_name"])

    def test_user_has_no_identifying_information(self):
        rv = self.client.get("/api/export/User", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertFalse("email" in response)
        print(response)

    def test_user_with_participant_properly_exported(self):
        u = self.construct_user()
        p = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant)
        self.session.commit()
        rv = self.client.get("/api/export/user", headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.client.get("/api/export/participant", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(u.id, response[0]["user_id"])

    def get_export(self):
        """Grabs everything exportable via the API, and returns it fully serialized ss json"""
        all_data = {}

        rv = self.client.get("/api/export", headers=self.logged_in_headers())
        response = rv.json
        exports = ExportInfoSchema(many=True).load(response)
        for export in exports:
            rv = self.client.get(
                export.url, follow_redirects=True, content_type="application/json", headers=self.logged_in_headers()
            )
            all_data[export.class_name] = rv.json
        return all_data

    def load_database(self, all_data):
        rv = self.client.get("/api/export", headers=self.logged_in_headers())
        response = rv.json
        exports = ExportInfoSchema(many=True).load(response)
        importer = ImportService()
        log = importer.log_for_export(exports, self.get_local_now())
        results = {}
        for export in exports:
            export.json_data = all_data[export.class_name]
            results[export.class_name] = importer.load_data(export, log)

        for class_name, count in all_data.items():
            self.assertEqual(len(count), results[class_name], msg=f"Failed to load all {count} items in {class_name}")

    def test_insert_user_with_participant(self):
        u = self.construct_user()
        user_id = u.id
        u._password = b"xxxxx"
        u.email_verified = True
        self.session.commit()
        self.session.close()

        db_user = self.session.execute(select(User).filter(User.id == user_id)).unique().scalar_one_or_none()
        role = db_user.role
        email_verified = db_user.email_verified
        u_registration_date = db_user.registration_date
        u_last_updated = db_user.last_updated
        orig_user_dict = UserSchema().dump(db_user)  # Use standard schema

        p = self.construct_participant(user_id=user_id, relationship=Relationship.self_participant)
        p_last_updated = p.last_updated
        orig_p_dict = ParticipantSchema().dump(p)  # Use standard schema
        self.session.commit()
        self.session.close()

        data = self.get_export()

        for exported_user_dict in data["User"]:
            self.assertNotIn("_password", exported_user_dict, msg="Passwords should not be exported.")

        self.session.commit()
        self.session.close()

        # Wait a couple seconds to make sure the timestamps are different
        time.sleep(2)

        self.load_database(data)

        db_user = self.session.query(User).filter_by(id=orig_user_dict["id"]).first()
        self.assertIsNotNone(db_user, msg="User is recreated.")
        self.assertNotEqual(orig_user_dict["email"], db_user.email, msg="Email should be obfuscated")
        self.assertEqual(u_registration_date, db_user.registration_date, msg="Dates are kept intact")
        self.assertEqual(u_last_updated, db_user.last_updated, msg="Dates are kept intact")
        self.assertEqual(role, db_user.role)
        self.assertEqual(email_verified, db_user.email_verified)

        db_par = self.session.query(Participant).filter_by(id=orig_p_dict["id"]).first()
        self.assertIsNotNone(db_par, msg="Participant is recreated.")
        self.assertEqual(db_user, db_par.user, msg="Relationship intact")
        self.assertEqual(p_last_updated, db_par.last_updated, msg="Dates are kept intact")

    def test_re_insert_user_with_modifications(self):
        # Construct the base user.
        u = self.construct_user()
        user_id = u.id
        self.session.commit()
        self.session.close()

        data = self.get_export()
        self.reset_db()
        self.session.commit()
        self.load_database(data)

        db_user_before = self.session.execute(select(User).filter(User.id == user_id)).unique().scalar_one_or_none()
        self.assertFalse(db_user_before.email_verified, msg="Email should start off unverified")

        # Modify the exported data slightly, and reload
        for user in data["User"]:
            user["email_verified"] = True
        self.load_database(data)

        db_user_after = self.session.execute(select(User).filter(User.id == user_id)).unique().scalar_one_or_none()
        self.assertTrue(db_user_after.email_verified, msg="Email should now be verified.")

    def test_identifying_questionnaire_does_not_export(self):

        # Construct the base user.
        u = self.construct_user()
        p = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant)
        iq = self.construct_identification_questionnaire(user=u, participant=p)
        id = u.id
        self.session.commit()
        data = self.get_export()
        self.reset_db()
        self.session.commit()

        self.load_database(data)
        self.assertEqual(ExportService.TYPE_IDENTIFYING, IdentificationQuestionnaire().__question_type__)
        self.assertEqual(
            0,
            len(self.session.query(IdentificationQuestionnaire).all()),
            msg="Identifying Questionnaires should not import.",
        )

    def test_all_sensitive_exports_have_links_to_self(self):
        self.construct_everything()
        exports = ExportService.get_table_info()
        for export in exports:
            if export.question_type != ExportService.TYPE_SENSITIVE:
                continue
            rv = self.client.get(
                export.url, follow_redirects=True, content_type="application/json", headers=self.logged_in_headers()
            )
            data = rv.json
            for d in data:
                self.assertTrue("_links" in d, msg="%s should have links in json." % export.class_name)
                self.assertTrue("self" in d["_links"])
                self.assert_success(self.client.get(d["_links"]["self"], headers=self.logged_in_headers()))

                rv_link = self.client.get(
                    d["_links"]["self"],
                    follow_redirects=True,
                    content_type="application/json",
                    headers=self.logged_in_headers(),
                )
                rv_link_data = json.loads(rv_link.get_data(as_text=True))

    def test_sensitive_records_returned_can_be_deleted(self):
        self.construct_all_questionnaires()
        exports = ExportService.get_table_info()
        for export in exports:
            rv = self.client.get(
                export.url, follow_redirects=True, content_type="application/json", headers=self.logged_in_headers()
            )
            data = rv.json
            for d in data:
                if export.question_type == ExportService.TYPE_SENSITIVE:
                    del_rv = self.client.delete(d["_links"]["self"], headers=self.logged_in_headers())
                    self.assert_success(del_rv)

    def test_retrieve_records_later_than(self):
        self.construct_everything()
        date = self.get_local_now() + datetime.timedelta(seconds=1)  # One second in the future
        exports = ExportService.get_table_info()
        params = "?after=" + date.strftime(ExportService.DATE_FORMAT)
        for export in exports:
            rv = self.client.get(
                export.url + params,
                follow_redirects=True,
                content_type="application/json",
                headers=self.logged_in_headers(),
            )
            data = rv.json
            self.assertEqual(0, len(data), msg=export.url + " does not respect 'after' param in get request.")

    def test_export_list_count_is_date_based(self):
        self.construct_everything()
        future_date = self.get_local_now() + datetime.timedelta(days=1)
        params = "?after=" + future_date.strftime(ExportService.DATE_FORMAT)

        rv = self.client.get("/api/export", headers=self.logged_in_headers())
        response = rv.json
        for export in response:
            self.assertGreater(export["size"], 0, msg=export["class_name"] + " should have a count > 0")

        rv = self.client.get("/api/export" + params, headers=self.logged_in_headers())
        response = rv.json
        for export in response:
            self.assertEqual(export["size"], 0, msg=export["class_name"] + " should have a count of 0")

    def test_it_all_crazy_madness_wohoo(self):
        # Sanity check, can we load everything, export it, delete, and reload it all without error.
        self.construct_everything()
        data = self.get_export()
        self.session.commit()
        self.session.close()
        self.reset_db()
        self.session.commit()
        self.session.close()
        self.load_database(data)

    def test_export_admin_details(self):
        user = self.construct_user(email="testadmin@test.com", role=Role.admin)
        user.password = "This_is_my_password!12345"
        self.session.add(user)
        self.session.commit()

        rv = self.client.get(
            "/api/export/admin",
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertTrue(len(response) > 1)
        self.assertEqual(1, len(list(filter(lambda field: field["email"] == "testadmin@test.com", response))))
        self.assertEqual(1, len(list(filter(lambda field: field["_password"] is not None, response))))

    def test_exporter_logs_export_calls(self):
        rv = self.client.get(
            "/api/export", follow_redirects=True, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        export_logs = self.session.query(DataTransferLog).filter(DataTransferLog.type == "exporting").all()
        self.assertEqual(1, len(export_logs))
        self.assertIsNotNone(export_logs[0].last_updated)
        self.assertTrue(
            export_logs[0].total_records > 0,
            msg="The act of setting up this test harness should mean "
            "at least one user record is avialable for export",
        )
        self.assertEqual(1, len(export_logs[0].details))
        detail = export_logs[0].details[0]
        self.assertEqual("User", detail.class_name)
        self.assertEqual(True, detail.successful)
        self.assertEqual(1, detail.success_count)

    def test_exporter_sends_no_email_alert_if_less_than_30_minutes_pass_without_export(self):

        message_count = len(EmailService.TEST_MESSAGES)

        log = DataTransferLog(
            last_updated=self.get_local_now() - datetime.timedelta(minutes=28), total_records=2, type="exporting"
        )
        self.session.add(log)
        self.session.commit()
        ExportService.send_alert_if_exports_not_running()
        self.assertEqual(len(EmailService.TEST_MESSAGES), message_count)

    def test_exporter_sends_email_alert_if_30_minutes_pass_without_export(self):
        """
        If more than 30 minutes pass without an export from the Public Mirror to the Private Mirror, an email should be
        sent to an administrative email address.
        """
        message_count = len(EmailService.TEST_MESSAGES)

        log = DataTransferLog(
            last_updated=self.get_local_now() - datetime.timedelta(minutes=45), total_records=2, type="exporting"
        )
        self.session.add(log)
        self.session.commit()

        ExportService.send_alert_if_exports_not_running()
        self.assertGreater(len(EmailService.TEST_MESSAGES), message_count)
        self.assertEqual(
            "Autism DRIVE: Error - 45 minutes since last successful export",
            self.decode(EmailService.TEST_MESSAGES[-1]["subject"]),
        )
        ExportService.send_alert_if_exports_not_running()
        ExportService.send_alert_if_exports_not_running()
        ExportService.send_alert_if_exports_not_running()
        self.assertEqual(message_count + 1, len(EmailService.TEST_MESSAGES), msg="No more messages should be sent.")
        self.assertEqual("admin@tester.com", EmailService.TEST_MESSAGES[-1]["To"])

    def test_exporter_sends_second_email_after_2_hours(self):
        """
        If more than 2 hours pass without an export from the Public Mirror to the Private Mirror, an email will be
        sent to an administrative email address at the 30 minute and 2 hour marks.
        """
        message_count = len(EmailService.TEST_MESSAGES)

        log = DataTransferLog(
            last_updated=self.get_local_now() - datetime.timedelta(minutes=30), total_records=2, type="exporting"
        )
        self.session.add(log)
        self.session.commit()
        ExportService.send_alert_if_exports_not_running()
        print("@ 30 minutes:", len(EmailService.TEST_MESSAGES), "messages")
        self.assertGreater(len(EmailService.TEST_MESSAGES), message_count)
        self.assertEqual(
            "Autism DRIVE: Error - 30 minutes since last successful export",
            self.decode(EmailService.TEST_MESSAGES[-1]["subject"]),
        )

        log.last_updated = self.get_local_now() - datetime.timedelta(minutes=120)
        self.session.add(log)
        self.session.commit()
        ExportService.send_alert_if_exports_not_running()
        print("@ 2 hours:", len(EmailService.TEST_MESSAGES), "messages")
        self.assertGreater(len(EmailService.TEST_MESSAGES), message_count + 1, "another email should have gone out")
        self.assertEqual(
            "Autism DRIVE: Error - 2 hours since last successful export",
            self.decode(EmailService.TEST_MESSAGES[-1]["subject"]),
        )

    def test_exporter_sends_12_emails_over_first_24_hours(self):
        """
        If more than 24 hours pass without an export from the Public Mirror to the Private Mirror, an email will be
        sent to an administrative email address at the 30 minute and then every 2 hours after that.
        """
        message_count = len(EmailService.TEST_MESSAGES)
        date = self.get_local_now() - datetime.timedelta(hours=22)
        log = DataTransferLog(last_updated=date, total_records=2, type="exporting")
        self.session.add(log)
        self.session.commit()
        for i in range(12):
            ExportService.send_alert_if_exports_not_running()
        self.assertEqual(message_count + 12, len(EmailService.TEST_MESSAGES), msg="12 emails should have gone out.")

    def test_exporter_sends_20_emails_over_first_48_hours(self):
        message_count = len(EmailService.TEST_MESSAGES)
        log = DataTransferLog(
            last_updated=self.get_local_now() - datetime.timedelta(days=2), total_records=2, type="exporting"
        )
        self.session.add(log)
        self.session.commit()
        for i in range(20):
            ExportService.send_alert_if_exports_not_running()
        self.assertEqual(message_count + 20, len(EmailService.TEST_MESSAGES), msg="20 emails should have gone out.")

    def test_exporter_notifies_PI_after_24_hours(self):
        message_count = len(EmailService.TEST_MESSAGES)
        log = DataTransferLog(
            last_updated=self.get_local_now() - datetime.timedelta(hours=24), total_records=2, type="exporting"
        )
        self.session.add(log)
        self.session.commit()
        ExportService.send_alert_if_exports_not_running()
        self.assertTrue("pi@tester.com" in EmailService.TEST_MESSAGES[-1]["To"])
