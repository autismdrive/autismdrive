import smtplib
from unittest.mock import MagicMock, patch

from tests.base_test_questionnaire import BaseTestQuestionnaire  # isort:skip
import datetime
import os
import time

from fixtures.fixture_utils import fake, fake_password
from flask import json
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.enums import Relationship, Role
from app.export_service import ExportService
from app.import_service import ImportService
from app.models import DataTransferLog, IdentificationQuestionnaire, Participant, User
from app.resources.UserEndpoint import get_user_by_id
from app.schemas import SchemaRegistry
from app.utils import utcnow

os.environ["ENV_NAME"] = "testing"
os.environ["TESTING"] = "true"


class TestExportService(BaseTestQuestionnaire):
    def test_get_list_of_exportables_requires_admin(self):
        rv = self.client.get("/api/export")
        self.assertEqual(401, rv.status_code)

        u = self.construct_user(email="joe@smoe.com", role=Role.user)
        u_id = u.id
        headers = self.logged_in_headers(user_id=u_id)
        rv = self.client.get("/api/export", headers=headers)
        self.assertEqual(403, rv.status_code)

    def test_get_list_of_exportables_contains_common_tables(self):
        rv = self.client.get(
            "/api/export",
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
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
        rv = self.client.get("/api/export", headers=self.default_logged_in_headers)
        self.assert_success(rv)
        response = rv.json
        user_data = list(filter(lambda field: field["class_name"] == "User", response))
        self.assertTrue(len(user_data) > 0)
        self.assertEqual("/api/export/user", user_data[0]["url"])
        self.assertEqual("User", user_data[0]["class_name"])
        self.assertEqual("stardrive_user", user_data[0]["table_name"])

    def test_get_list_of_exportables_has_url_for_all_endpoints(self):
        rv = self.client.get("/api/export", headers=self.default_logged_in_headers)
        self.assert_success(rv)
        response = rv.json
        for entry in response:
            self.assertTrue("url" in entry, msg="No url provided for " + entry["class_name"])
            self.assertNotEqual("", entry["url"], msg="No url provided for " + entry["class_name"])

    def test_all_urls_respond_with_success(self):
        from inspect import currentframe, getframeinfo

        frameinfo = getframeinfo(currentframe())

        times = []
        times.append((frameinfo.lineno, time.perf_counter_ns()))
        self.assertIsNotNone(self.default_user.id)
        self.assertIsNotNone(self.default_logged_in_headers)

        print(f"User ID: {self.default_user.id}")
        print(f"Headers: {self.default_logged_in_headers}")

        rv = self.client.get(
            "/api/export",
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        times.append((frameinfo.lineno, time.perf_counter_ns()))
        self.assert_success(rv)
        times.append((frameinfo.lineno, time.perf_counter_ns()))
        exports = rv.json
        times.append((frameinfo.lineno, time.perf_counter_ns()))
        for export in exports:
            times.append((frameinfo.lineno, time.perf_counter_ns()))
            rv = self.client.get(
                export["url"],
                follow_redirects=True,
                content_type="application/json",
                headers=self.default_logged_in_headers,
            )
            times.append((frameinfo.lineno, time.perf_counter_ns()))
            self.assert_success(rv, msg="Failed to retrieve a list for " + export["class_name"])
            times.append((frameinfo.lineno, time.perf_counter_ns()))
            print("Successful export of " + export["class_name"])
            times.append((frameinfo.lineno, time.perf_counter_ns()))

        for i, (line_number, t_ns) in enumerate(times):
            if i == 0:
                continue

            _, prev_t_ns = times[i - 1]
            print(f"t{line_number} = {t_ns - prev_t_ns:.6f}")

    def test_user_has_no_identifying_information(self):
        rv = self.client.get("/api/export/User", headers=self.default_logged_in_headers)
        self.assert_success(rv)
        response = rv.json
        self.assertFalse("email" in response)
        print(response)

    def test_user_with_participant_properly_exported(self):
        u = self.default_user
        self.construct_participant(user_id=u.id, relationship=Relationship.self_participant)
        self.session.commit()
        rv = self.client.get("/api/export/user", headers=self.default_logged_in_headers)
        self.assert_success(rv)
        rv = self.client.get("/api/export/participant", headers=self.default_logged_in_headers)
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(u.id, response[0]["user_id"])

    def get_export(self):
        """Grabs everything exportable via the API, and returns it fully serialized ss json"""
        headers = self.default_logged_in_headers
        all_data = {}

        rv = self.client.get("/api/export", headers=headers)
        response = rv.json
        exports = SchemaRegistry.ExportInfoSchema(many=True).load(response)
        for export in exports:
            rv = self.client.get(export.url, follow_redirects=True, content_type="application/json", headers=headers)
            all_data[export.class_name] = rv.json
            if export.class_name == "ResourceCategory":
                print(all_data[export.class_name])
        return all_data

    def load_database(self, all_data):
        rv = self.client.get("/api/export", headers=self.default_logged_in_headers)
        response = rv.json
        exports = SchemaRegistry.ExportInfoSchema(many=True).load(response)
        importer = ImportService()
        log = importer.log_for_export(exports, utcnow())
        results = {}
        for export in exports:
            export.json_data = all_data[export.class_name]
            results[export.class_name] = importer.load_data(export, log)

        for class_name, class_items in all_data.items():
            count = len(class_items) if class_items else 0
            self.assertEqual(count, results[class_name], msg=f"Failed to load all {count} items in {class_name}")

    def test_insert_user_with_participant(self):
        u = self.default_user
        user_id = u.id
        user_email = u.email
        u._password = b"xxxxx"
        u.email_verified = True
        self.session.commit()
        self.session.close()

        db_user = get_user_by_id(user_id)
        role = db_user.role
        email_verified = db_user.email_verified
        u_registration_date = db_user.registration_date
        u_last_updated = db_user.last_updated
        self.session.commit()
        self.session.close()

        p = self.construct_participant(user_id=user_id, relationship=Relationship.self_participant)
        p_last_updated = p.last_updated
        p_id = p.id
        self.session.commit()
        self.session.close()

        data = self.get_export()

        for exported_user_dict in data["User"]:
            self.assertNotIn("_password", exported_user_dict, msg="Passwords should not be exported.")

        self.session.commit()
        self.session.close()

        # Wait a couple milliseconds to make sure the timestamps are different
        time.sleep(2)

        self.load_database(data)

        db_user = self.session.query(User).filter_by(id=user_id).first()
        self.assertIsNotNone(db_user, msg="User is recreated.")
        self.assertNotEqual(user_email, db_user.email, msg="Email should be obfuscated")
        self.assertEqual(u_registration_date, db_user.registration_date, msg="Dates are kept intact")
        self.assertEqual(u_last_updated, db_user.last_updated, msg="Dates are kept intact")
        self.assertEqual(role, db_user.role)
        self.assertEqual(email_verified, db_user.email_verified)

        db_par = self.session.query(Participant).filter_by(id=p_id).first()
        self.assertIsNotNone(db_par, msg="Participant is recreated.")
        self.assertEqual(db_user, db_par.user, msg="Relationship intact")
        self.assertEqual(p_last_updated, db_par.last_updated, msg="Dates are kept intact")

    def test_re_insert_user_with_modifications(self):
        # Construct the base user.
        u = self.construct_user(email=fake.email(), role=Role.user)
        user_id = u.id
        self.session.commit()
        self.session.close()

        data = self.get_export()

        # Run teardown and setup to clear out the database
        self.tearDown()
        self.setUp()

        # Load the exported data into the database
        self.load_database(data)

        db_user_before = (
            self.session.execute(select(User).options(joinedload(User.participants)).filter(User.id == user_id))
            .unique()
            .scalar_one_or_none()
        )
        self.assertFalse(db_user_before.email_verified, msg="Email should start off unverified")

        # Modify the exported data slightly, and reload
        for user in data["User"]:
            user["email_verified"] = True
        self.load_database(data)

        db_user_after = (
            self.session.execute(select(User).options(joinedload(User.participants)).filter(User.id == user_id))
            .unique()
            .scalar_one_or_none()
        )
        self.assertTrue(db_user_after.email_verified, msg="Email should now be verified.")

    def test_identifying_questionnaire_does_not_export(self):
        # Construct the base user.
        u = self.default_user
        u_id = u.id
        p = self.construct_participant(user_id=u_id, relationship=Relationship.self_participant)
        p_id = p.id
        self.construct_identification_questionnaire(user_id=u_id, participant_id=p_id)
        self.session.commit()
        data = self.get_export()

        # Run teardown and setup to clear out the database
        self.tearDown()
        self.setUp()

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
        headers = self.default_logged_in_headers
        for export in exports:
            if export.question_type != ExportService.TYPE_SENSITIVE:
                continue
            rv = self.client.get(export.url, follow_redirects=True, content_type="application/json", headers=headers)
            data = rv.json
            for d in data:
                self.assertTrue("_links" in d, msg="%s should have links in json." % export.class_name)
                self.assertTrue("self" in d["_links"])
                self.assert_success(self.client.get(d["_links"]["self"], headers=headers))

                rv_link = self.client.get(
                    d["_links"]["self"],
                    follow_redirects=True,
                    content_type="application/json",
                    headers=headers,
                )
                rv_link_data = json.loads(rv_link.get_data(as_text=True))

                self.assertEqual(d, rv_link_data, msg="Data returned from link does not match original data.")

    def test_sensitive_records_returned_can_be_deleted(self):
        self.construct_all_questionnaires()
        exports = ExportService.get_table_info()
        for export in exports:
            rv = self.client.get(
                export.url,
                follow_redirects=True,
                content_type="application/json",
                headers=self.default_logged_in_headers,
            )
            data = rv.json
            for d in data:
                if export.question_type == ExportService.TYPE_SENSITIVE:
                    del_rv = self.client.delete(d["_links"]["self"], headers=self.default_logged_in_headers)
                    self.assert_success(del_rv)

    def test_retrieve_records_later_than(self):
        self.construct_everything()
        date = utcnow() + datetime.timedelta(seconds=1)  # One second in the future
        exports = ExportService.get_table_info()
        params = "?after=" + date.strftime(ExportService.DATE_FORMAT)
        headers = self.default_logged_in_headers
        for export in exports:
            url = export.url + params
            rv = self.client.get(
                url,
                follow_redirects=True,
                content_type="application/json",
                headers=headers,
            )
            data = rv.json
            self.assertEqual(0, len(data), msg=export.url + " does not respect 'after' param in get request.")

    def test_export_list_count_is_date_based(self):
        self.construct_everything()
        future_date = utcnow() + datetime.timedelta(days=1)
        params = "?after=" + future_date.strftime(ExportService.DATE_FORMAT)

        rv = self.client.get("/api/export", headers=self.default_logged_in_headers)
        response = rv.json
        for export in response:
            self.assertGreater(export["size"], 0, msg=export["class_name"] + " should have a count > 0")

        rv = self.client.get("/api/export" + params, headers=self.default_logged_in_headers)
        response = rv.json
        for export in response:
            self.assertEqual(export["size"], 0, msg=export["class_name"] + " should have a count of 0")

    def test_export_and_reimport_all(self):
        # Sanity check, can we load everything, export it, delete, and reload it all without error.
        self.construct_everything()
        data = self.get_export()

        # Run teardown and setup to clear out the database
        self.tearDown()
        self.setUp()

        self.load_database(data)

    def test_export_admin_details(self):
        u1_email = fake.email()
        u1 = self.construct_user(email=u1_email, role=Role.admin)
        u1_id = u1.id

        # Create another admin user
        u2_email = fake.email()
        u2 = self.construct_user(email=u2_email, role=Role.admin)
        u2_id = u2.id
        u2_headers = self.logged_in_headers(user_id=u2_id)

        db_u1 = get_user_by_id(u1_id)
        db_u1.password = fake_password()
        self.session.add(db_u1)
        self.session.commit()
        self.session.close()

        rv = self.client.get(
            "/api/export/admin",
            follow_redirects=True,
            content_type="application/json",
            headers=u2_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertGreaterEqual(len(response), 2)

        # Filter response to ensure both users are present
        u_response = [u for u in response if u["email"] in (u1_email, u2_email)]
        self.assertEqual(len(u_response), 2)

        for u_dict in u_response:
            self.assertIn("_password", u_dict)
            self.assertIsNotNone(u_dict["_password"])

    def test_exporter_logs_export_calls(self):
        start_time = utcnow()
        num_users_before = self.session.query(User).count()

        rv = self.client.get(
            "/api/export",
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        export_logs = (
            self.session.query(DataTransferLog)
            .filter(DataTransferLog.type == "exporting")
            .filter(DataTransferLog.date_started >= start_time)
            .all()
        )
        self.assertEqual(1, len(export_logs))
        self.assertIsNotNone(export_logs[0].last_updated)
        self.assertTrue(export_logs[0].total_records > 0, msg="At least one user record should be available for export")
        self.assertEqual(1, len(export_logs[0].details))
        detail = export_logs[0].details[0]
        self.assertEqual("User", detail.class_name)
        self.assertEqual(True, detail.successful)
        self.assertEqual(num_users_before, detail.success_count)

    @patch("smtplib.SMTP", autospec=True)
    def test_exporter_sends_no_email_alert_if_less_than_30_minutes_pass_without_export(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        log = DataTransferLog(last_updated=utcnow() - datetime.timedelta(minutes=28), total_records=2, type="exporting")
        self.session.add(log)
        self.session.commit()
        ExportService.send_alert_if_exports_not_running()
        mock_sendmail.assert_not_called()

    @patch("smtplib.SMTP", autospec=True)
    def test_exporter_sends_email_alert_if_30_minutes_pass_without_export(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        """
        If more than 30 minutes pass without an export from the Public Mirror to the Private Mirror, an email should be
        sent to an administrative email address.
        """
        log = DataTransferLog(last_updated=utcnow() - datetime.timedelta(minutes=45), total_records=2, type="exporting")
        self.session.add(log)
        self.session.commit()

        ExportService.send_alert_if_exports_not_running()
        self.assert_email_sent(
            mock_sendmail, self.settings.ADMIN_EMAIL, "Autism DRIVE: Error - 45 minutes since last successful export"
        )
        mock_sendmail.reset_mock()
        ExportService.send_alert_if_exports_not_running()
        ExportService.send_alert_if_exports_not_running()
        ExportService.send_alert_if_exports_not_running()
        mock_sendmail.assert_not_called()

    @patch("smtplib.SMTP", autospec=True)
    def test_exporter_sends_second_email_after_2_hours(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        """
        If more than 2 hours pass without an export from the Public Mirror to the Private Mirror, an email will be
        sent to an administrative email address at the 30 minute and 2 hour marks.
        """
        log = DataTransferLog(last_updated=utcnow() - datetime.timedelta(minutes=30), total_records=2, type="exporting")
        self.session.add(log)
        self.session.commit()
        ExportService.send_alert_if_exports_not_running()
        self.assert_email_sent(
            mock_sendmail, self.settings.ADMIN_EMAIL, "Autism DRIVE: Error - 30 minutes since last successful export"
        )
        mock_sendmail.reset_mock()

        log.last_updated = utcnow() - datetime.timedelta(minutes=120)
        self.session.add(log)
        self.session.commit()
        ExportService.send_alert_if_exports_not_running()
        self.assert_email_sent(
            mock_sendmail, self.settings.ADMIN_EMAIL, "Autism DRIVE: Error - 2 hours since last successful export"
        )

    def assert_export_alerts_sent(self, mock_sendmail: MagicMock, expected_count: int):
        """
        Helper function to assert that the correct number of export alerts were sent via email.
        """
        # Create a log entry for the first 30 minutes, then every 2 hours up to 24 hours
        hr_offsets: list[float] = [((i + 1) * 2) for i in range(expected_count - 1)]

        # Create list of expected email subjects
        expected_subjects = [
            f"Autism DRIVE: Error - {hr_offset} hours since last successful export" for hr_offset in hr_offsets
        ]

        # Insert the first 30 minutes at the start of the list, because the first email subject is slightly different
        hr_offsets.insert(0, 0.5)
        expected_subjects.insert(0, "Autism DRIVE: Error - 30 minutes since last successful export")

        for hr_offset in hr_offsets:
            start_time = utcnow()
            last_updated = start_time - datetime.timedelta(hours=hr_offset)
            log = DataTransferLog(last_updated=last_updated, total_records=2, type="exporting")
            self.session.add(log)
            self.session.commit()
            self.session.close()

            # Send email alerts for exports
            ExportService.send_alert_if_exports_not_running()

            self.session.delete(log)
            self.session.commit()
            self.session.close()

        self.assert_emails_sent(mock_sendmail, self.settings.ADMIN_EMAIL, expected_subjects)

    @patch("smtplib.SMTP", autospec=True)
    def test_exporter_sends_12_emails_over_first_24_hours(self, mock_smtp: MagicMock):
        """
        If more than 24 hours pass without an export from the Public Mirror to the Private Mirror, an email will be
        sent to an administrative email address at the 30 minute mark and then every 2 hours after that.
        """
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        self.assert_export_alerts_sent(mock_sendmail, 12)

    @patch("smtplib.SMTP", autospec=True)
    def test_exporter_sends_20_emails_over_first_48_hours(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        self.assert_export_alerts_sent(mock_sendmail, 20)

    @patch("smtplib.SMTP", autospec=True)
    def test_exporter_notifies_PI_after_24_hours(self, mock_smtp: MagicMock):
        mock_sendmail: MagicMock[smtplib.SMTP.sendmail] = mock_smtp.return_value.sendmail
        log = DataTransferLog(last_updated=utcnow() - datetime.timedelta(hours=24), total_records=2, type="exporting")
        self.session.add(log)
        self.session.commit()
        ExportService.send_alert_if_exports_not_running()
        self.assert_email_sent(
            mock_sendmail,
            f"{self.settings.ADMIN_EMAIL}, {self.settings.PRINCIPAL_INVESTIGATOR_EMAIL}",
            "Autism DRIVE: Error - 24 hours since last successful export",
        )
