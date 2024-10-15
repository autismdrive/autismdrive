from tests.base_test import BaseTest


class TestConfig(BaseTest):
    def test_config(self):
        rv = self.client.get("/api/config", follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["mirroring"], False)
        self.assertEqual(response["testing"], True)
        self.assertEqual(response["development"], False)
