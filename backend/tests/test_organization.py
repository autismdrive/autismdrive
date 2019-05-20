import unittest

from flask import json
from tests.base_test import BaseTest
from app import db
from app.model.organization import Organization


class TestOrganizations(BaseTest, unittest.TestCase):

    def test_organization_basics(self):
        self.construct_organization()
        o = db.session.query(Organization).first()
        self.assertIsNotNone(o)
        rv = self.app.get('/api/organization/%i' % o.id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], o.id)
        self.assertEqual(response["name"], 'Staunton Makerspace')
        self.assertEqual(response["description"],
                         'A place full of surprise, delight, and amazing people. And tools. Lots of exciting tools.')

    def test_modify_organization_basics(self):
        self.construct_organization()
        o = db.session.query(Organization).first()
        self.assertIsNotNone(o)
        rv = self.app.get('/api/organization/%i' % o.id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['name'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        orig_date = response['last_updated']
        rv = self.app.put('/api/organization/%i' % o.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assert_success(rv)
        rv = self.app.get('/api/organization/%i' % o.id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_organization(self):
        o = self.construct_organization()
        o_id = o.id
        rv = self.app.get('api/organization/%i' % o_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.delete('api/organization/%i' % o_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.get('api/organization/%i' % o_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_organization(self):
        organization = {'name': "Organization of Champions", 'description': "All the best people, all the time."}
        rv = self.app.post('api/organization', data=json.dumps(organization), content_type="application/json",
                           follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'Organization of Champions')
        self.assertEqual(response['description'], 'All the best people, all the time.')
        self.assertIsNotNone(response['id'])
