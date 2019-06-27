import unittest

from flask import json
from tests.base_test import BaseTest
from app import db, elastic_index
from app.model.event import Event
from app.model.location import Location
from app.model.resource_category import ResourceCategory


class TestLocations(BaseTest, unittest.TestCase):

    def test_location_basics(self):
        self.construct_location()
        r = db.session.query(Location).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/location/%i' % r_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], r_id)
        self.assertEqual(response["title"], 'A+ location')
        self.assertEqual(response["description"], 'A delightful location destined to create rejoicing')
        self.assertEqual(response["latitude"], 38.98765)
        self.assertEqual(response["longitude"], -93.12345)

    def test_modify_location_basics(self):
        self.construct_location()
        r = db.session.query(Location).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/location/%i' % r_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        response['website'] = 'http://sartography.com'
        response['latitude'] = 34.5678
        response['longitude'] = -98.7654
        orig_date = response['last_updated']
        rv = self.app.put('/api/location/%i' % r_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assert_success(rv)
        rv = self.app.get('/api/location/%i' % r_id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['website'], 'http://sartography.com')
        self.assertEqual(response['latitude'], 34.5678)
        self.assertEqual(response['longitude'], -98.7654)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_location(self):
        r = self.construct_location()
        r_id = r.id
        rv = self.app.get('api/location/%i' % r_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.delete('api/location/%i' % r_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.get('api/location/%i' % r_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_location(self):
        o_id = self.construct_organization().id
        location = {'title': "location of locations", 'description': "You need this location in your life.", 'organization_id': o_id}
        rv = self.app.post('api/location', data=json.dumps(location), content_type="application/json",
                           follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'location of locations')
        self.assertEqual(response['description'], 'You need this location in your life.')
        self.assertIsNotNone(response['id'])

    def test_get_location_by_category(self):
        loc = self.construct_location()
        c = self.construct_location_category(loc.id, "c1")

        rv = self.app.get(
            '/api/category/%i/location' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(loc.id, response[0]["resource_id"])
        self.assertEqual(loc.description, response[0]["resource"]["description"])

    def test_get_location_by_category_includes_category_details(self):
        loc = self.construct_location()
        c1 = self.construct_location_category(loc.id, "c1")
        c2 = self.construct_location_category(loc.id, "c2")

        rv = self.app.get(
            '/api/category/%i/location' % c1.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(loc.id, response[0]["resource_id"])
        self.assertEqual(2, len(response[0]["resource"]["resource_categories"]))
        self.assertEqual("c1", response[0]["resource"]["resource_categories"][0]["category"]["name"])

    def test_category_location_count(self):
        loc = self.construct_location()
        c = self.construct_location_category(loc.id, "c1")
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["location_count"])

    def test_get_category_by_location(self):
        c = self.construct_category()
        loc = self.construct_location()
        rc = ResourceCategory(resource_id=loc.id, category=c, type='location')
        db.session.add(rc)
        db.session.commit()
        rv = self.app.get(
            '/api/location/%i/category' % loc.id,
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_location(self):
        c = self.construct_category()
        loc = self.construct_location()

        rc_data = {"resource_id": loc.id, "category_id": c.id}

        rv = self.app.post(
            '/api/resource_category',
            data=json.dumps(rc_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(loc.id, response["resource_id"])

    def test_set_all_categories_on_location(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        loc = self.construct_location()

        lc_data = [
            {
                "category_id": c1.id
            },
            {
                "category_id": c2.id
            },
            {
                "category_id": c3.id
            },
        ]
        rv = self.app.post(
            '/api/location/%i/category' % loc.id,
            data=json.dumps(lc_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        lc_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/location/%i/category' % loc.id,
            data=json.dumps(lc_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_location(self):
        self.test_add_category_to_location()
        rv = self.app.delete('/api/resource_category/%i' % 1)
        self.assert_success(rv)
        rv = self.app.get(
            '/api/location/%i/category' % 1, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))
