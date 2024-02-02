import datetime
import random
from unittest.mock import patch, MagicMock, call

import requests
from sqlalchemy import select

from app.enums import Role
from app.export_service import ExportService
from app.import_service import ImportService
from app.models import DataTransferLog, DataTransferLogDetail, ExportInfo, User
from app.schemas import (
    ExportInfoSchema,
    ExportSchemas,
    ClinicalDiagnosesQuestionnaireSchema,
    EmploymentQuestionnaireSchema,
)
from config.load import settings
from fixtures.fixure_utils import fake
from mocks.mock_response import MockRequestsResponse
from tests.base_test_questionnaire import BaseTestQuestionnaire

fake_token = fake.md5()
fake_headers = {"Authorization": f"Bearer {fake_token}", "Accept": "application/json"}


class TestImportCase(BaseTestQuestionnaire):
    """Please note that the actual loading of data is tested in the Export tests, this
    Is really assuring that the import service makes the right calls to the API with the
    right arguments."""

    api_url = settings.API_URL

    def setUp(self):
        super().setUp()

    @patch("requests.get", return_value=MockRequestsResponse({"token": fake_token}, 200))
    def test_mock_patch(self, mock_get: MagicMock):
        response = requests.get("https://httpbin.org/ip")
        result = response.json()
        self.assertTrue("token" in result)
        self.assertTrue(result["token"] == fake_token)
        mock_get.should_be_called_once()

    @patch("requests.post", return_value=MockRequestsResponse({"token": fake_token}, 200))
    def test_login(self, mock_post: MagicMock):
        data_importer = ImportService()
        data_importer.login()
        mock_post.should_be_called_once()

    @patch("requests.get", return_value=MockRequestsResponse({"error": "not logged in"}, 400))
    @patch("requests.post", return_value=MockRequestsResponse({"token": fake_token}, 200))
    def test_headers(self, mock_post: MagicMock, mock_get: MagicMock):
        # Assure that a failed request to get_headers will cause a re-login attempt.
        data_importer = ImportService()

        headers = data_importer.get_headers()
        self.assertIsNotNone(headers)
        self.assertEqual(f"Bearer {fake_token}", headers["Authorization"])

        expected_json = {"email": settings.MASTER_EMAIL, "password": settings.MASTER_PASS}
        mock_post.assert_called_with(f"{self.api_url}/api/login_password", json=expected_json)
        mock_get.assert_called_with(
            f"{self.api_url}/api/session", headers={"Authorization": "Bearer invalid", "Accept": "application/json"}
        )

    def get_data_importer_setup_auth(self):
        data_importer = ImportService()
        data_importer.token = fake_token
        return data_importer

    @patch("requests.get")
    def test_get_export_list(self, mock_get):
        info = [ExportInfo("my_table", "my_class", size=0, url=f"{self.api_url}/api/export/my_class")]
        info_json = ExportInfoSchema().dump(info, many=True)
        mock_get.return_value = MockRequestsResponse(info_json, 200)
        data_importer = self.get_data_importer_setup_auth()
        exportables = data_importer.get_export_list()
        self.assertEqual(1, len(exportables))

    def test_no_subsequent_requests_when_size_is_0(self):
        data_importer = self.get_data_importer_setup_auth()
        info = [ExportInfo("my_table", "my_class", size=0, url=f"{self.api_url}/api/export/my_class")]
        info_json = ExportInfoSchema().dump(info, many=True)

        with patch("requests.get") as mock_get:
            mock_get.return_value = MockRequestsResponse(info_json, 200)
            export_list = data_importer.get_export_list()

        with patch("requests.get") as mock_get:
            mock_get.return_value = MockRequestsResponse(info_json, 200)
            data_importer.request_data(export_list)

    def request_user_setup(self):
        info = [ExportInfo("star_user", "User", size=1, url="/api/export/user")]
        info_json = ExportInfoSchema().dump(info, many=True)

        user = User(
            id=random.randint(10000, 99999),
            last_updated=datetime.datetime.now(),
            email=fake.email(),
            role=Role.user,
            email_verified=True,
        )
        user.password = fake.password(length=25, special_chars=True, upper_case=True)
        user.token = user.encode_auth_token()
        user_json = ExportSchemas.UserExportSchema(many=True).dump([user])
        admin_json = ExportSchemas.AdminExportSchema(many=True).dump([user])

        return info_json, user_json, admin_json

    @patch("requests.get")
    def test_request_when_size_larger_than_0(self, mock_get: MagicMock):
        data_importer = self.get_data_importer_setup_auth()
        info_json, user_json, _ = self.request_user_setup()
        mock_get.side_effect = [
            MockRequestsResponse(user_json, 200),
            MockRequestsResponse(info_json, 200),
            MockRequestsResponse(user_json, 200),
            MockRequestsResponse(user_json, 200),
        ]

        export_list = data_importer.get_export_list()
        data_importer.request_data(export_list)

        mock_get.assert_has_calls(
            [
                call(f"{self.api_url}/api/session", headers=fake_headers),
                call(f"{self.api_url}/api/export", headers=fake_headers),
                call(f"{self.api_url}/api/session", headers=fake_headers),
                call(f"{self.api_url}/api/export/user", headers=fake_headers),
            ]
        )

    @patch("requests.get")
    def test_import_logs_success(self, mock_get: MagicMock):
        data_importer = self.get_data_importer_setup_auth()
        info_json, user_json, admin_json = self.request_user_setup()
        mock_get.side_effect = [
            MockRequestsResponse(user_json, 200),
            MockRequestsResponse(info_json, 200),
            MockRequestsResponse(user_json, 200),
            MockRequestsResponse(user_json, 200),
            MockRequestsResponse(user_json, 200),
            MockRequestsResponse(admin_json, 200),
        ]

        data_importer.run_backup()

        expected_calls = [
            call(f"{self.api_url}/api/session", headers=fake_headers),
            call(f"{self.api_url}/api/export", headers=fake_headers),
            call(f"{self.api_url}/api/session", headers=fake_headers),
            call(f"{self.api_url}/api/export/user", headers=fake_headers),
            call(f"{self.api_url}/api/session", headers=fake_headers),
            call(f"{self.api_url}/api/export/admin", headers=fake_headers),
        ]

        mock_get.assert_has_calls(expected_calls)

        logs = self.session.execute(select(DataTransferLog)).unique().scalars().all()
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

    @patch("requests.get")
    def test_import_logs_schema_error(self, mock_get):
        info_json, user_json, _ = self.request_user_setup()

        mock_get.side_effect = [
            MockRequestsResponse(user_json, 200),
            MockRequestsResponse(info_json, 200),
            MockRequestsResponse(user_json, 200),
            MockRequestsResponse(user_json, 200),
        ]

        data_importer = self.get_data_importer_setup_auth()
        date = datetime.datetime.now()
        export_list = data_importer.get_export_list()
        log = data_importer.log_for_export(export_list, date)
        data = data_importer.request_data(export_list)

        data[0].json_data[0].update(
            {
                "email": "invalid_email",
                "role": "invalid_role",
            }
        )

        with self.assertRaises(Exception):
            data_importer.load_all_data(data, log)

        mock_get.assert_has_calls(
            [
                call(f"{self.api_url}/api/session", headers=fake_headers),
                call(f"{self.api_url}/api/export", headers=fake_headers),
                call(f"{self.api_url}/api/session", headers=fake_headers),
                call(f"{self.api_url}/api/export/user", headers=fake_headers),
            ]
        )

        logs = self.session.query(DataTransferLog).all()
        self.assertTrue(len(logs) > 0)
        log = logs[-1]
        self.assertIsNotNone(log.date_started)
        self.assertIsNotNone(log.last_updated)
        details = log.details[0]
        self.assertEqual("User", details.class_name)
        self.assertFalse(details.successful)
        self.assertEqual(0, details.success_count)
        self.assertEqual(1, details.failure_count)

    @patch("requests.get")
    def test_request_includes_date_param_if_log_exists(self, mock_get: MagicMock):
        mock_get.return_value = MockRequestsResponse({}, 200)

        # log a previous success
        last_date = datetime.datetime.now() - datetime.timedelta(days=1)
        log = DataTransferLog(date_started=last_date, last_updated=last_date)
        log.details.append(DataTransferLogDetail(date_started=last_date, class_name="User"))
        self.session.add(log)
        self.session.commit()

        data_importer = self.get_data_importer_setup_auth()
        info_json, user_json, admin_json = self.request_user_setup()

        mock_get.side_effect = [
            MockRequestsResponse(user_json, 200),
            MockRequestsResponse(info_json, 200),
            MockRequestsResponse(user_json, 200),
            MockRequestsResponse(user_json, 200),
        ]
        data_importer.run_backup(load_admin=False)

        mock_get.assert_has_calls(
            [
                call(f"{self.api_url}/api/session", headers=fake_headers),
                call(f"{self.api_url}/api/export", headers=fake_headers),
                call(f"{self.api_url}/api/session", headers=fake_headers),
                call(
                    f"{self.api_url}/api/export/user?after=" + last_date.strftime(ExportService.DATE_FORMAT),
                    headers=fake_headers,
                ),
            ]
        )

    @patch("requests.get")
    def test_admin_accounts_should_be_requested_in_full_and_import_with_working_password(self, mock_get):
        num_admins = 5
        admin_accounts = []
        admin_users = []
        for i in range(num_admins):
            admin_accounts.append(
                {
                    "id": random.randint(10000, 99999),
                    "email": fake.email(),
                    "password": fake.password(length=25, special_chars=True, upper_case=True),
                }
            )

        for a in admin_accounts:
            admin_user = User(
                id=a["id"],
                email=a["email"],
                role=Role.admin,
                email_verified=True,
                last_updated=datetime.datetime.now(),
            )
            admin_user.password = a["password"]
            admin_user.token = admin_user.encode_auth_token()
            admin_users.append(admin_user)

        exported_admins = ExportSchemas.AdminExportSchema().dump(admin_users, many=True)
        mock_get.return_value = MockRequestsResponse(exported_admins, 200)
        data_importer = self.get_data_importer_setup_auth()
        data_importer.load_admin()

        for a in admin_accounts:
            data = {"email": a["email"], "password": a["password"]}
            rv = self.client.post("/api/login_password", json=data, content_type="application/json")
            self.assertEqual(200, rv.status_code)

    @patch("requests.get")
    @patch("requests.delete")
    def test_import_calls_delete_on_sensitive_data(self, mock_delete: MagicMock, mock_get: MagicMock):
        export_list = [
            ExportInfo(
                "clinical_diagnoses_questionnaire",
                "ClinicalDiagnosesQuestionnaire",
                size=1,
                url="/api/export/clinical_diagnoses_questionnaire",
            )
        ]

        q = self.construct_clinical_diagnoses_questionnaire()
        id = q.id
        json_q = ClinicalDiagnosesQuestionnaireSchema(many=True).dump([q])
        self.session.delete(q)

        settings.DELETE_RECORDS = True
        data_importer = self.get_data_importer_setup_auth()
        _, user_json, _ = self.request_user_setup()

        mock_get.side_effect = [
            MockRequestsResponse(user_json, 200),
            MockRequestsResponse(json_q, 200),
            MockRequestsResponse(user_json, 200),
        ]
        mock_delete.return_value = MockRequestsResponse(json_q, 200)

        date = datetime.datetime.now()
        data = data_importer.request_data(export_list)
        log = data_importer.log_for_export(data, date)
        data_importer.load_all_data(data, log)

        mock_get.assert_has_calls(
            [
                call(f"{self.api_url}/api/session", headers=fake_headers),
                call(f"{self.api_url}/api/export/clinical_diagnoses_questionnaire", headers=fake_headers),
                call(f"{self.api_url}/api/session", headers=fake_headers),
            ]
        )
        mock_delete.assert_called_with(
            f"{self.api_url}/api/q/clinical_diagnoses_questionnaire/" + str(id), headers=fake_headers
        )

    @patch("requests.get")
    @patch("requests.delete")
    def test_import_does_not_call_delete_on_non_sensitive_data(self, mock_delete: MagicMock, mock_get: MagicMock):
        export_list = [
            ExportInfo(
                "employment_questionnaire",
                "EmploymentQuestionnaire",
                size=1,
                url="/api/export/employment_questionnaire",
            )
        ]

        q = self.construct_employment_questionnaire()
        id = q.id
        json_q = EmploymentQuestionnaireSchema(many=True).dump([q])
        self.session.delete(q)

        mock_get.return_value = MockRequestsResponse(json_q, 200)
        mock_delete.return_value = MockRequestsResponse(json_q, 200)

        data_importer = self.get_data_importer_setup_auth()
        date = datetime.datetime.now()
        data = data_importer.request_data(export_list)
        log = data_importer.log_for_export(data, date)
        data_importer.load_all_data(data, log)
        mock_get.assert_called_with(f"{self.api_url}/api/export/employment_questionnaire", headers=fake_headers)
        mock_delete.assert_not_called()
