import unittest

from flask import json
from tests.base_test import BaseTest
from app import db, elastic_index
from app.model.event import Event
from app.model.resource_category import ResourceCategory


class TestEvents(BaseTest, unittest.TestCase):

    def construct_event(self, title="A+ Event", description="A delightful event destined to create rejoicing",
                           street_address1="123 Some Pl", street_address2="Apt. 45",
                           city="Stauntonville", state="QX", zip="99775", phone="555-555-5555",
                           website="http://stardrive.org"):

        event = Event(title=title, description=description, street_address1=street_address1, street_address2=street_address2, city=city,
                                state=state, zip=zip, phone=phone, website=website)
        event.organization_id = self.construct_organization().id
        db.session.add(event)
        db.session.commit()

        db_event = db.session.query(Event).filter_by(title=event.title).first()
        self.assertEqual(db_event.website, event.website)
        elastic_index.add_document(db_event, 'Event')
        return db_event

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
        rv = self.app.put('/api/event/%i' % r_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
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

        rv = self.app.delete('api/event/%i' % r_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.get('api/event/%i' % r_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_event(self):
        event = {'title': "event of events", 'description': "You need this event in your life.", 'time': "4PM sharp",
                 'ticket_cost': "$500 suggested donation"}
        rv = self.app.post('api/event', data=json.dumps(event), content_type="application/json",
                           follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'event of events')
        self.assertEqual(response['description'], 'You need this event in your life.')
        self.assertEqual(response['time'], '4PM sharp')
        self.assertEqual(response['ticket_cost'], '$500 suggested donation')
        self.assertIsNotNone(response['id'])

    def test_get_event_by_category(self):
        c = self.construct_category()
        ev = self.construct_event()
        rc = ResourceCategory(resource_id=ev.id, category=c, type='event')
        db.session.add(rc)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/event' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(ev.id, response[0]["id"])
        self.assertEqual(ev.description, response[0]["resource"]["description"])

    def test_get_event_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        ev = self.construct_event()
        rc = ResourceCategory(resource_id=ev.id, category=c, type='event')
        rc2 = ResourceCategory(resource_id=ev.id, category=c2, type='event')
        db.session.add_all([rc, rc2])
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/event' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(ev.id, response[0]["id"])
        self.assertEqual(2,
                         len(response[0]["resource"]["resource_categories"]))
        self.assertEqual(
            "c1", response[0]["resource"]["resource_categories"][0]["category"]
            ["name"])

    def test_category_event_count(self):
        c = self.construct_category()
        ev = self.construct_event()
        rec = self.construct_resource()
        rc = ResourceCategory(resource_id=ev.id, category=c, type='event')
        rc2 = ResourceCategory(resource_id=rec.id, category=c, type='resource')
        db.session.add_all([rc, rc2])
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["event_count"])

    def test_get_category_by_event(self):
        c = self.construct_category()
        ev = self.construct_event()
        rc = ResourceCategory(resource_id=ev.id, category=c, type='event')
        db.session.add(rc)
        db.session.commit()
        rv = self.app.get(
            '/api/event/%i/category' % ev.id,
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_event(self):
        c = self.construct_category()
        ev = self.construct_event()

        ec_data = {"resource_id": ev.id, "category_id": c.id}

        rv = self.app.post(
            '/api/resource_category',
            data=json.dumps(ec_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(ev.id, response["resource_id"])

    def test_set_all_categories_on_event(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        ev = self.construct_event()

        ec_data = [
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
            data=json.dumps(ec_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        ec_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/event/%i/category' % ev.id,
            data=json.dumps(ec_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_event(self):
        self.test_add_category_to_event()
        rv = self.app.delete('/api/resource_category/%i' % 1)
        self.assert_success(rv)
        rv = self.app.get(
            '/api/event/%i/category' % 1, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))
