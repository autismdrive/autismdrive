import unittest

from flask import json

from app.model.user import Role, User
from tests.base_test import BaseTest


class TestImportExportCase(BaseTest, unittest.TestCase):

    def test_get_list_of_exportables_requires_admin(self):
        rv = self.app.get('/api/export')
        self.assertEquals(401, rv.status_code)

        headers = self.logged_in_headers(self.construct_user(email="joe@smoe.com", role=Role.user))
        rv = self.app.get('/api/export', headers=headers)
        self.assertEquals(403, rv.status_code)

    def test_get_list_of_exportables_contains_common_tables(self):
        rv = self.app.get('/api/export',
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertTrue(len(response) > 1)
        self.assertEqual(1, len(list(filter(lambda field: field['name'] == 'Category', response))))
        self.assertEqual(1, len(list(filter(lambda field: field['name'] == 'Participant', response))))
        self.assertEqual(1, len(list(filter(lambda field: field['name'] == 'User', response))))

    def test_get_list_of_exportables_has_basic_attributes(self):
        rv = self.app.get('/api/export', headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        user_data = list(filter(lambda field: field['name'] == 'User', response))
        self.assertTrue(len(user_data) > 0)
        self.assertEquals("/api/export/user", user_data[0]['url'])

    def test_get_list_of_exportables_has_url_for_all_endpoints(self):
        rv = self.app.get('/api/export', headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        for entry in response:
            self.assertTrue('url' in entry, msg="No url provided for " + entry["name"])
            self.assertNotEqual("", entry['url'], msg="No url provided for " + entry["name"])

    def test_al_urls_respond_with_success(self):
        rv = self.app.get('/api/export',
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        exports = json.loads(rv.get_data(as_text=True))
        for export in exports:
            rv = self.app.get(export['url'],
                              follow_redirects=True,
                              content_type="application/json",
                              headers=self.logged_in_headers())
            self.assert_success(rv, msg="Failed to retrieve a list for " + export['name'])
            print("Successful export of " + export['name'])
    def test_fetch_users_works(self):
        rv = self.app.get('/api/export/user', headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        print(response)
