import unittest

from flask import json

from app import db, data_loader
from app.model.webinar import Webinar
from tests.base_test import BaseTest
from app.model.resource_category import ResourceCategory
from app.model.resource_change_log import ResourceChangeLog
from app.model.user import Role


class TestWebinars(BaseTest, unittest.TestCase):

    def test_webinar_basics(self):
        self.construct_webinar()
        r = db.session.query(Webinar).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/webinar/%i' % r_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], r_id)
        self.assertEqual(response["title"], 'A+ Webinar')
        self.assertEqual(response["description"], 'A delightful webinar destined to create rejoicing')

    def test_modify_webinar_basics(self):
        data_loader.DataLoader().load_partial_zip_codes()
        self.construct_webinar()
        r = db.session.query(Webinar).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/webinar/%i' % r_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        response['website'] = 'http://sartography.com'
        orig_date = response['last_updated']
        rv = self.app.put('/api/webinar/%i' % r_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/webinar/%i' % r_id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['website'], 'http://sartography.com')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_webinar(self):
        r = self.construct_webinar()
        r_id = r.id
        rv = self.app.get('api/webinar/%i' % r_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.delete('api/webinar/%i' % r_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/webinar/%i' % r_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_webinar(self):
        data_loader.DataLoader().load_partial_zip_codes()
        webinar = {'title': "webinar of webinars", 'description': "You need this webinar in your life.", 'time': "4PM sharp",
                 'ticket_cost': "$500 suggested donation", 'organization_name': "Webinar Org"}
        rv = self.app.post('api/webinar', data=json.dumps(webinar), content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'webinar of webinars')
        self.assertEqual(response['description'], 'You need this webinar in your life.')
        self.assertEqual(response['time'], '4PM sharp')
        self.assertEqual(response['ticket_cost'], '$500 suggested donation')
        self.assertIsNotNone(response['id'])

    def test_get_webinar_by_category(self):
        c = self.construct_category()
        webinar = self.construct_webinar()
        rc = ResourceCategory(resource_id=webinar.id, category=c, type='webinar')
        db.session.add(rc)
        rv = self.app.get(
            '/api/category/%i/resource' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(webinar.id, response[0]["resource_id"])
        self.assertEqual(webinar.description, response[0]["resource"]["description"])

    def test_get_webinar_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        webinar = self.construct_webinar()
        rc = ResourceCategory(resource_id=webinar.id, category=c, type='webinar')
        rc2 = ResourceCategory(resource_id=webinar.id, category=c2, type='webinar')
        db.session.add_all([rc, rc2])
        rv = self.app.get(
            '/api/category/%i/resource' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(webinar.id, response[0]["resource_id"])
        self.assertEqual(2,
                         len(response[0]["resource"]["resource_categories"]))
        self.assertEqual(
            "c1", response[0]["resource"]["resource_categories"][0]["category"]
            ["name"])

    def test_category_webinar_count(self):
        c = self.construct_category()
        webinar = self.construct_webinar()
        rwebcat = self.construct_resource()
        rc = ResourceCategory(resource_id=webinar.id, category=c, type='webinar')
        rc2 = ResourceCategory(resource_id=rwebcat.id, category=c, type='resource')
        db.session.add_all([rc, rc2])
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["webinar_count"])

    def test_get_category_by_webinar(self):
        c = self.construct_category()
        webinar = self.construct_webinar()
        rc = ResourceCategory(resource_id=webinar.id, category=c, type='webinar')
        db.session.add(rc)
        rv = self.app.get(
            '/api/resource/%i/category' % webinar.id,
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["category_id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_webinar(self):
        c = self.construct_category()
        webinar = self.construct_webinar()

        webcat_data = {"resource_id": webinar.id, "category_id": c.id}

        rv = self.app.post(
            '/api/resource_category',
            data=json.dumps(webcat_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(webinar.id, response["resource_id"])

    def test_set_all_categories_on_webinar(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        webinar = self.construct_webinar()

        webcat_data = [
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
            '/api/resource/%i/category' % webinar.id,
            data=json.dumps(webcat_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        webcat_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/resource/%i/category' % webinar.id,
            data=json.dumps(webcat_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_webinar(self):
        self.test_add_category_to_webinar()
        rv = self.app.delete('/api/resource_category/%i' % 1)
        self.assert_success(rv)
        rv = self.app.get(
            '/api/resource/%i/category' % 1, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_resource_change_log(self):
        data_loader.DataLoader().load_partial_zip_codes()
        webinar = self.construct_webinar(title='A Webinar that is Super and Great')
        u = self.construct_user(email="editor@sartorgraphy.com", role=Role.admin)

        rv = self.app.get('api/webinar/%i' % webinar.id, content_type="application/json")
        self.assert_success(rv)

        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Super Great Webinar'
        rv = self.app.put('/api/webinar/%i' % webinar.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers(user=u))
        self.assert_success(rv)
        rv = self.app.get('/api/webinar/%i' % webinar.id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Super Great Webinar')

        logs = ResourceChangeLog.query.all()
        self.assertIsNotNone(logs[-1].resource_id)
        self.assertIsNotNone(logs[-1].user_id)

        rv = self.app.get('/api/resource/%i/change_log' % webinar.id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response[-1]['user_id'], u.id)

        rv = self.app.get('/api/user/%i/resource_change_log' % u.id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response[-1]['resource_id'], webinar.id)
