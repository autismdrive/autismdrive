import unittest

from flask import json

from app import db, data_loader
from app.model.event import Event
from tests.base_test import BaseTest
from app.model.resource_category import ResourceCategory
from app.model.resource_change_log import ResourceChangeLog
from app.model.user import Role


class TestEvents(BaseTest, unittest.TestCase):

    def test_event_basics(self):
        self.construct_event()
        r = db.session.query(Event).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/event/%i' % r_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], r_id)
        self.assertEqual(response["title"], 'A+ Event')
        self.assertEqual(response["description"], 'A delightful event destined to create rejoicing')

    def test_modify_event_basics(self):
        data_loader.DataLoader().load_partial_zip_codes()
        self.construct_event()
        r = db.session.query(Event).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/event/%i' % r_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        response['website'] = 'http://sartography.com'
        orig_date = response['last_updated']
        rv = self.app.put('/api/event/%i' % r_id, data=self.jsonify(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/event/%i' % r_id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['website'], 'http://sartography.com')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_event(self):
        r = self.construct_event()
        r_id = r.id
        rv = self.app.get('api/event/%i' % r_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.delete('api/event/%i' % r_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/event/%i' % r_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_event(self):
        data_loader.DataLoader().load_partial_zip_codes()
        event = {'title': "event of events", 'description': "You need this event in your life.", 'time': "4PM sharp",
                 'ticket_cost': "$500 suggested donation", 'organization_name': "Event Org"}
        rv = self.app.post('api/event', data=self.jsonify(event), content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'event of events')
        self.assertEqual(response['description'], 'You need this event in your life.')
        self.assertEqual(response['time'], '4PM sharp')
        self.assertEqual(response['ticket_cost'], '$500 suggested donation')
        self.assertIsNotNone(response['id'])

    def test_get_event_by_category(self):
        c = self.construct_category()
        event = self.construct_event()
        rc = ResourceCategory(resource_id=event.id, category=c, type='event')
        db.session.add(rc)
        rv = self.app.get(
            '/api/category/%i/resource' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(event.id, response[0]["resource_id"])
        self.assertEqual(event.description, response[0]["resource"]["description"])

    def test_get_event_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        event = self.construct_event()
        rc = ResourceCategory(resource_id=event.id, category=c, type='event')
        rc2 = ResourceCategory(resource_id=event.id, category=c2, type='event')
        db.session.add_all([rc, rc2])
        rv = self.app.get(
            '/api/category/%i/resource' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(event.id, response[0]["resource_id"])
        self.assertEqual(2,
                         len(response[0]["resource"]["resource_categories"]))
        self.assertEqual(
            "c1", response[0]["resource"]["resource_categories"][0]["category"]
            ["name"])

    def test_category_event_count(self):
        c = self.construct_category()
        event = self.construct_event()
        revcat = self.construct_resource()
        rc = ResourceCategory(resource_id=event.id, category=c, type='event')
        rc2 = ResourceCategory(resource_id=revcat.id, category=c, type='resource')
        db.session.add_all([rc, rc2])
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["event_count"])

    def test_get_category_by_event(self):
        c = self.construct_category()
        event = self.construct_event()
        rc = ResourceCategory(resource_id=event.id, category=c, type='event')
        db.session.add(rc)
        rv = self.app.get(
            '/api/resource/%i/category' % event.id,
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["category_id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_event(self):
        c = self.construct_category()
        event = self.construct_event()

        evcat_data = {"resource_id": event.id, "category_id": c.id}

        rv = self.app.post(
            '/api/resource_category',
            data=self.jsonify(ec_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(event.id, response["resource_id"])

    def test_set_all_categories_on_event(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        event = self.construct_event()

        evcat_data = [
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
            '/api/event/%i/category' % ev.id,
            data=self.jsonify(ec_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        evcat_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/event/%i/category' % ev.id,
            data=self.jsonify(ec_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_event(self):
        self.test_add_category_to_event()
        rv = self.app.delete('/api/resource_category/%i' % 1)
        self.assert_success(rv)
        rv = self.app.get(
            '/api/resource/%i/category' % 1, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_resource_change_log(self):
        data_loader.DataLoader().load_partial_zip_codes()
        event = self.construct_event(title='A Event that is Super and Great')
        u = self.construct_user(email="editor@sartorgraphy.com", role=Role.admin)

        rv = self.app.get('api/event/%i' % event.id, content_type="application/json")
        self.assert_success(rv)

        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Super Great Event'
        rv = self.app.put('/api/event/%i' % ev.id, data=self.jsonify(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers(user=u))
        self.assert_success(rv)
        rv = self.app.get('/api/event/%i' % event.id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Super Great Event')

        logs = ResourceChangeLog.query.all()
        self.assertIsNotNone(logs[-1].resource_id)
        self.assertIsNotNone(logs[-1].user_id)

        rv = self.app.get('/api/resource/%i/change_log' % event.id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response[-1]['user_id'], u.id)

        rv = self.app.get('/api/user/%i/resource_change_log' % u.id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response[-1]['resource_id'], event.id)
