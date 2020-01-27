import unittest
from flask import json
from tests.base_test import BaseTest
from app import db
from app.model.investigator import Investigator


class TestStudy(BaseTest, unittest.TestCase):

    def test_investigator_basics(self):
        self.construct_investigator()
        i = db.session.query(Investigator).first()
        self.assertIsNotNone(i)
        i_id = i.id
        rv = self.app.get('/api/investigator/%i' % i_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], i_id)
        self.assertEqual(response["name"], i.name)

    def test_modify_investigator_basics(self):
        self.construct_investigator()
        i = db.session.query(Investigator).first()
        self.assertIsNotNone(i)

        rv = self.app.get('/api/investigator/%i' % i.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'dungeon master'
        orig_date = response['last_updated']
        rv = self.app.put('/api/investigator/%i' % i.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)

        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'dungeon master')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_investigator(self):
        i = self.construct_investigator()
        i_id = i.id

        rv = self.app.get('api/investigator/%i' % i_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/investigator/%i' % i_id, content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/investigator/%i' % i_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_investigator(self):
        o_id = self.construct_organization().id
        investigator = {'name': "Tara Tarantula", 'title': "Assistant Professor of Arachnology", 'organization_id': o_id}
        rv = self.app.post('api/investigator', data=json.dumps(investigator), content_type="application/json",
                           headers=self.logged_in_headers(), follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'Tara Tarantula')
        self.assertEqual(response['title'], 'Assistant Professor of Arachnology')
        self.assertIsNotNone(response['id'])

    def test_investigator_list_alphabetical_by_name(self):
        self.construct_investigator(name="Adelaide Smith")
        self.construct_investigator(name="Sarah Blakemore")
        self.construct_investigator(name="Zelda Cat")
        self.construct_investigator(name="Benjamin Jensen")

        rv = self.app.get('api/investigator', content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response[0]['name'], 'Adelaide Smith')
        self.assertEqual(response[1]['name'], 'Benjamin Jensen')
        self.assertEqual(response[2]['name'], 'Sarah Blakemore')
        self.assertEqual(response[3]['name'], 'Zelda Cat')

    def test_create_investigator_checks_for_name(self):
        self.test_create_investigator()
        rv = self.app.get('api/investigator', content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response[0]['name'], 'Tara Tarantula')
        self.assertEqual(response[0]['title'], 'Assistant Professor of Arachnology')

        investigator = {'name': "Tara Tarantula", 'title': "Spider"}
        rv = self.app.post('api/investigator', data=json.dumps(investigator), content_type="application/json",
                           headers=self.logged_in_headers(), follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'Tara Tarantula')
        self.assertEqual(response['title'], 'Assistant Professor of Arachnology')
