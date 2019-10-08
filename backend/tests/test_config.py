import unittest

from flask import json
from tests.base_test import BaseTest


class TestConfig(BaseTest, unittest.TestCase):

    def test_config(self):
        rv = self.app.get('/api/config',
                          follow_redirects=True,
                          content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["mirroring"], False)
        self.assertEqual(response["testing"], True)
        self.assertEqual(response["development"], False)

