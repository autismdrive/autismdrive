import datetime
import unittest

import httpretty
import requests
from flask import json

from app import app, db
from app.import_service import ImportService
from app.model.data_transfer_log import DataTransferLog, DataTransferLogDetail
from app.model.export_info import ExportInfo, ExportInfoSchema
from app.model.questionnaires.clinical_diagnoses_questionnaire import ClinicalDiagnosesQuestionnaireSchema
from app.model.questionnaires.employment_questionnaire import EmploymentQuestionnaireSchema
from app.model.user import User, Role
from app.schema.export_schema import UserExportSchema, AdminExportSchema
from tests.base_test_questionnaire import BaseTestQuestionnaire


class TestImportCase(BaseTestQuestionnaire, unittest.TestCase):
    """Please note that the actual loading of data is tested in the Export tests, this
    Is really assuring that the import service makes the right calls to the API with the
    right arguments."""

    def setUp(self):
        super().setUp()
        app.config["MASTER_URL"] = "http://na.edu"
        app.config["MASTER_EMAIL"] = "dan@test.com"
        app.config["MASTER_PASS"] = "12345"

    @httpretty.activate
    def test_httppretty(self):
        # Just wanted a simple exmple to show how to use HTTP Pretty
        httpretty.register_uri(
            httpretty.GET,
            "https://httpbin.org/ip",
            body='{"origin": "127.0.0.1"}'
        )

        response = requests.get('https://httpbin.org/ip')
        rv = response.json()
        self.assertTrue("origin" in rv)
        self.assertTrue(rv["origin"] == "127.0.0.1")
        self.assertEqual(1, len(httpretty.httpretty.latest_requests))
        self.assertIsNotNone(httpretty.last_request())
        self.assertEqual(httpretty.last_request().body, b'')

    @httpretty.activate
    def test_login(self):
        # Just wanted a simple exmple to show how to use HTTP Pretty
        httpretty.register_uri(
            httpretty.POST,
            "http://na.edu/api/login_password",
            body='{"token": "my_token"}'
        )
        data_importer = ImportService(app, db)
        data_importer.login()
        self.assertIsNotNone(httpretty.last_request())

    @httpretty.activate
    def test_headers(self):
        # Assure that a failed request to get_headers will cause a re-login attempt.
        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/session",
            body='{"error": "not logged in"}',
            status=400
        )
        httpretty.register_uri(
            httpretty.POST,
            "http://na.edu/api/login_password",
            body='{"token": "my_token"}',
        )

        app.config["MASTER_URL"] = "http://na.edu"
        app.config["MASTER_EMAIL"] = "dan@test.com"
        app.config["MASTER_PASS"] = "12345"
        data_importer = ImportService(app, db)
        headers = data_importer.get_headers()
        self.assertIsNotNone(httpretty.last_request())
        self.assertIsNotNone(headers)
        self.assertEqual("Bearer my_token", headers['Authorization'])
        self.assertEqual(2, len(httpretty.httpretty.latest_requests))

    def get_data_importer_setup_auth(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/session",
            body='{"email": "dan@test.com"}',
            status=200
        )
        data_importer = ImportService(app, db)
        data_importer.token = "my_token"
        return data_importer

    @httpretty.activate
    def test_get_export_list(self):
        info = [ExportInfo('my_table', 'my_class', size=0, url="http://na.edu/api/export/my_class")]
        info_json = ExportInfoSchema(many=True).jsonify(info).data
        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export",
            body=info_json,
            status=200
        )
        data_importer = self.get_data_importer_setup_auth()
        exportables = data_importer.get_export_list()
        self.assertEqual(1, len(exportables))

    @httpretty.activate
    def test_no_subsequent_requests_when_size_is_0(self):
        data_importer = self.get_data_importer_setup_auth()
        info = [ExportInfo('my_table', 'my_class', size=0, url="http://na.edu/api/export/my_class")]
        info_json = ExportInfoSchema(many=True).jsonify(info).data
        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export",
            body=info_json,
            status=200
        )
        export_list = data_importer.get_export_list()
        data_importer.request_data(export_list)
        self.assertEqual(2, len(httpretty.httpretty.latest_requests))  # Assumes one request for auth check.
        self.assertEqual("/api/export", httpretty.last_request().path)

    def request_user_setup(self):
        info = [ExportInfo('star_user', 'User', size=1, url="/api/export/user")]
        info_json = ExportInfoSchema(many=True).jsonify(info).data

        user = User(id=4, last_updated=datetime.datetime.now(), email="dan@test.com",
                    role=Role.user, email_verified=True, _password="m@kerspace")
        user_json = self.jsonify(UserExportSchema(many=True).dump([user]))
        admin_json = self.jsonify(AdminExportSchema(many=True).dump([user]))

        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export",
            body=info_json,
            status=200
        )
        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export/user",
            body=user_json,
            status=200
        )
        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export/admin",
            body=admin_json,
            status=200
        )

    @httpretty.activate
    def test_request_when_size_larger_than_0(self):
        data_importer = self.get_data_importer_setup_auth()
        self.request_user_setup()
        export_list = data_importer.get_export_list()
        data_importer.request_data(export_list)
        self.assertEqual("/api/export/user", httpretty.last_request().path)

    @httpretty.activate
    def test_import_logs_success(self):
        data_importer = self.get_data_importer_setup_auth()
        self.request_user_setup()
        data_importer.run_backup()

        self.assertEqual("/api/export/admin", httpretty.last_request().path)
        logs = db.session.query(DataTransferLog).all()
        self.assertTrue(len(logs) > 0)
        log = logs[0]
        self.assertIsNotNone(log.date_started)
        self.assertIsNotNone(log.last_updated)
        self.assertEqual(1, len(logs[0].details))
        detail = logs[0].details[0]
        self.assertEqual("User", detail.class_name)
        self.assertTrue(detail.successful)
        self.assertEqual(1, detail.success_count)
        self.assertEqual(0, detail.failure_count)

    @httpretty.activate
    def test_import_logs_schema_error(self):
        info = [ExportInfo('star_user', 'User', size=1, url="/api/export/user")]
        info_json = ExportInfoSchema(many=True).jsonify(info).data
        user_json = self.jsonify([{"id": "55", "pickes": "42"}])

        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export",
            body=info_json,
            status=200
        )
        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export/user",
            body=user_json,
            status=200
        )
        data_importer = self.get_data_importer_setup_auth()
        date = datetime.datetime.now()
        export_list = data_importer.get_export_list()
        log = data_importer.log_for_export(export_list, date)
        data = data_importer.request_data(export_list)
        try:
            data_importer.load_all_data(data, log)
        except:
            pass  # Totally should happen.
        self.assertEqual("/api/export/user", httpretty.last_request().path)
        logs = db.session.query(DataTransferLog).all()
        self.assertTrue(len(logs) > 0)
        log = logs[-1]
        self.assertIsNotNone(log.date_started)
        self.assertIsNotNone(log.last_updated)
        details = log.details
        self.assertEqual("User", log.details[0].class_name)
        self.assertFalse(log.details[0].successful)
        self.assertEqual(0, log.details[0].success_count)
        self.assertEqual(1, log.details[0].failure_count)

    @httpretty.activate
    def test_request_includes_date_param_if_log_exists(self):
        # log a previous success
        last_date = datetime.datetime.now() - datetime.timedelta(days=1)
        log = DataTransferLogDetail(date_started=last_date, class_name="User")
        db.session.add(log)

        data_importer = self.get_data_importer_setup_auth()
        self.request_user_setup()
        data_importer.run_backup(load_admin=False)

        self.assertTrue("after" in httpretty.last_request().querystring)

    @httpretty.activate
    def test_admin_accounts_should_be_requested_in_full_and_import_with_working_password(self):
        password = "Tacos are good! 823497!#%$^&*"
        data_importer = self.get_data_importer_setup_auth()
        user = User(id=4, last_updated=datetime.datetime.now(), email="dan@test.com",
                    role=Role.admin, email_verified=True)
        user.password = password
        user_json = self.jsonify(AdminExportSchema(many=True).dump([user]))
        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export/admin",
            body=user_json,
            status=200
        )
        data_importer.load_admin()

#        encoded = base64.encodestring(user._password)
#        data = {'email': 'dan@test.com', 'password': encoded.decode()}
        data = {'email': 'dan@test.com', 'password': password}
        rv = self.app.post(
            '/api/login_password',
            data=self.jsonify(data),
            content_type="application/json")
        self.assertEqual(200, rv.status_code)

    @httpretty.activate
    def test_import_calls_delete_on_sensitive_data(self):
        export_list = [ExportInfo('clinical_diagnoses_questionnaire', 'ClinicalDiagnosesQuestionnaire', size=1,
                           url="/api/export/clinical_diagnoses_questionnaire")]

        q = self.construct_clinical_diagnoses_questionnaire()
        id = q.id
        json_q = self.jsonify(ClinicalDiagnosesQuestionnaireSchema(many=True).dump([q]))
        db.session.delete(q)

        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export/clinical_diagnoses_questionnaire",
            body=json_q,
            status=200
        )
        expected_delete_url = "http://na.edu/api/q/clinical_diagnoses_questionnaire/" + str(id)
        httpretty.register_uri(
            httpretty.DELETE,
            expected_delete_url,
            body=json_q,
            status=200
        )
        app.config['DELETE_RECORDS'] = True
        data_importer = self.get_data_importer_setup_auth()
        date = datetime.datetime.now()
        data = data_importer.request_data(export_list)
        log = data_importer.log_for_export(data, date)
        data_importer.load_all_data(data, log)
        self.assertEqual("/api/q/clinical_diagnoses_questionnaire/" + str(id), httpretty.last_request().path)
        self.assertEqual("DELETE", httpretty.last_request().method)

    @httpretty.activate
    def test_import_does_not_call_delete_on_non_sensitive_data(self):
        export_list = [ExportInfo('employment_questionnaire', 'EmploymentQuestionnaire', size=1,
                           url="/api/export/employment_questionnaire")]

        q = self.construct_employment_questionnaire()
        id = q.id
        json_q = self.jsonify(EmploymentQuestionnaireSchema(many=True).dump([q]))
        db.session.delete(q)

        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export/employment_questionnaire",
            body=json_q,
            status=200
        )
        data_importer = self.get_data_importer_setup_auth()
        date = datetime.datetime.now()
        data = data_importer.request_data(export_list)
        log = data_importer.log_for_export(data, date)
        data_importer.load_all_data(data, log)
        self.assertEqual("GET", httpretty.last_request().method)  # Last call should not be a delete call.
