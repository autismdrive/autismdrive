import datetime
import unittest

import httpretty
import requests

from app import app, db
from app.data_importer import DataImporter
from app.model.export_info import ExportInfo, ExportInfoSchema
from app.model.user import User, Role
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
        self.assertEquals(1, len(httpretty.httpretty.latest_requests))
        self.assertIsNotNone(httpretty.last_request())
        self.assertEquals(httpretty.last_request().body, b'')

    @httpretty.activate
    def test_login(self):
        # Just wanted a simple exmple to show how to use HTTP Pretty
        httpretty.register_uri(
            httpretty.POST,
            "http://na.edu/api/login_password",
            body='{"token": "my_token"}'
        )
        data_importer = DataImporter(app, db)
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
        data_importer = DataImporter(app, db)
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
        data_importer = DataImporter(app, db)
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
        data_importer.load_data()
        self.assertEqual(2, len(httpretty.httpretty.latest_requests)) # Assumes one request for auth check.
        self.assertEqual("/api/export", httpretty.last_request().path)

    @httpretty.activate
    def test_request_when_size_larger_than_0(self):
        data_importer = self.get_data_importer_setup_auth()
        user = User(id=4, last_updated=datetime.datetime.now(), email="dan@test.com",
                    role=Role.user, email_verified=True)
        info = [ExportInfo('star_user', 'User', size=1, url="http://na.edu/api/export/user")]
        info_json = ExportInfoSchema(many=True).jsonify(info).data
        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export",
            body=info_json,
            status=200
        )
        httpretty.register_uri(
            httpretty.GET,
            "http://na.edu/api/export/user",
            body='[{"a":"b"}]',
            status=200
        )
        data_importer.request_data()
        self.assertEqual("/api/export/user", httpretty.last_request().path)

    @httpretty.activate
    def test_request_includes_date_param_and_record_last_update_status(self):
        self.assertFalse(True, msg="Requests for data should include the date")

    def test_admin_accounts_should_be_requested_in_full(self):
        self.assertTrue(False, msg="Admin accounts should be replicated so folks can log into the private systems.")
