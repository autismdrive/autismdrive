from app.model.data_transfer_log import DataTransferLog, DataTransferLogDetail, DataTransferLogSchema
from tests.base_test import BaseTest


class TestDataTransferLogs(BaseTest):
    def test_export_logs_endpoint(self):
        for i in range(20):
            elog = DataTransferLog()
            for x in range(2):
                dlog = DataTransferLogDetail()
                elog.details.append(dlog)
            self.session.add(elog)

        self.session.commit()

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
