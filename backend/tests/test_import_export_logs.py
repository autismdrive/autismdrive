import unittest

from flask import json

from app import db
from app.model.export_log import ExportLog, ExportLogSchema, ExportLogPagesSchema
from app.model.import_log import ImportLog, ImportLogSchema
from tests.base_test import BaseTest


class TestStatus(BaseTest, unittest.TestCase):

    def test_export_logs_endpoint(self):
        for i in range(20):
            elog = ExportLog()
            db.session.add(elog)

        rv = self.app.get('/api/export_log?pageSize=10',
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEquals(20, response['total'])
        self.assertEquals(2, response['pages'])
        self.assertEquals(10, len(response['items']))
        results = ExportLogSchema(many=True, session=db.session).load(response['items']).data
        self.assertEquals(10, len(results))

    def test_import_logs_endpoint(self):
        for i in range(20):
            log = ImportLog()
            db.session.add(log)

        rv = self.app.get('/api/import_log?pageSize=10',
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEquals(20, response['total'])
        self.assertEquals(2, response['pages'])
        self.assertEquals(10, len(response['items']))
        results = ImportLogSchema(many=True, session=db.session).load(response['items']).data
        self.assertEquals(10, len(results))