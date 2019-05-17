import unittest
from tests.base_test import BaseTest

class TestImportExportCase(BaseTest, unittest.TestCase):


    def test_get_list_of_exportables(self):
        rv = self.app.get('/api/export',
                          follow_redirects=True,
                          content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                          headers=self.logged_in_headers())
        #self.assert_success(rv)

