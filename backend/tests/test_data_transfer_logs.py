from app.models import DataTransferLog, DataTransferLogDetail
from app.schemas import DataTransferLogSchema, DataTransferLogDetailSchema
from tests.base_test import BaseTest


class TestDataTransferLogs(BaseTest):
    def test_export_logs_endpoint(self):
        for i in range(20):
            elog = DataTransferLog(
                type="exporting" if i % 2 == 0 else "importing",
                alerts_sent=i,
            )
            for j in range(2):
                dlog = DataTransferLogDetail(errors="some error message")
                elog.details.append(dlog)
            self.session.add(elog)
            self.session.commit()
            self.session.close()

        rv = self.client.get(
            "/api/data_transfer_log?pageSize=10",
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(20, response["total"])
        self.assertEqual(2, response["pages"])
        self.assertEqual(10, len(response["items"]))
        results = DataTransferLogSchema(many=True, session=self.session).load(response["items"])
        self.assertEqual(10, len(results))

        # Each log should have 2 details
        for result in results:
            self.assertIn(result.type, ["exporting", "importing"])
            self.assertEqual(2, len(result.details))

            for detail in result.details:
                self.assertEqual(detail.errors, "some error message")
