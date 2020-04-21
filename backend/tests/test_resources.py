import unittest

from flask import json

from tests.base_test import BaseTest
from app import db, elastic_index
from app.model.resource import Resource
from app.model.resource_category import ResourceCategory
from app.model.resource_change_log import ResourceChangeLog
from app.model.user import Role


class TestResources(BaseTest, unittest.TestCase):

    def test_resource_basics(self):
        self.construct_resource()
        r = db.session.query(Resource).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/resource/%i' % r_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], r_id)
        self.assertEqual(response["title"], 'A+ Resource')
        self.assertEqual(response["description"], 'A delightful Resource destined to create rejoicing')

    def test_modify_resource_basics(self):
        self.construct_resource()
        r = db.session.query(Resource).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/resource/%i' % r_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        response['website'] = 'http://sartography.com'
        orig_date = response['last_updated']
        rv = self.app.put('/api/resource/%i' % r_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/resource/%i' % r_id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['website'], 'http://sartography.com')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_resource(self):
        r = self.construct_resource()
        r_id = r.id
        rv = self.app.get('api/resource/%i' % r_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.delete('api/resource/%i' % r_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/resource/%i' % r_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_delete_resource_with_admin_note_and_no_elastic_record(self):
        r = self.construct_resource()
        r_id = r.id
        rv = self.app.get('api/resource/%i' % r_id, content_type="application/json")
        self.assert_success(rv)

        self.construct_admin_note(user=self.construct_user(), resource=r)
        elastic_index.remove_document(r, 'Resource')
        rv = self.app.delete('api/resource/%i' % r_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/resource/%i' % r_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_resource(self):
        resource = {'title': "Resource of Resources", 'description': "You need this resource in your life.",
                    'organization_name': "Resource Org"}
        rv = self.app.post('api/resource', data=json.dumps(resource), content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Resource of Resources')
        self.assertEqual(response['description'], 'You need this resource in your life.')
        self.assertIsNotNone(response['id'])

    def test_get_resource_by_category(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c, type='resource')
        db.session.add(cr)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/resource' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(r.id, response[0]["resource_id"])
        self.assertEqual(r.description, response[0]["resource"]["description"])

    def test_get_resource_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c, type='resource')
        cr2 = ResourceCategory(resource=r, category=c2, type='resource')
        db.session.add_all([cr, cr2])
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/resource' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(r.id, response[0]["resource_id"])
        self.assertEqual(2,
                         len(response[0]["resource"]["resource_categories"]))
        self.assertEqual(
            "c1", response[0]["resource"]["resource_categories"][0]["category"]
            ["name"])

    def test_category_resource_count(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c, type='resource')
        db.session.add(cr)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["resource_count"])

    def test_get_category_by_resource(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c, type='resource')
        db.session.add(cr)
        db.session.commit()
        rv = self.app.get(
            '/api/resource/%i/category' % r.id,
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_resource(self):
        c = self.construct_category()
        r = self.construct_resource()

        rc_data = {"resource_id": r.id, "category_id": c.id}

        rv = self.app.post(
            '/api/resource_category',
            data=json.dumps(rc_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(r.id, response["resource_id"])

    def test_set_all_categories_on_resource(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        r = self.construct_resource()

        rc_data = [
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
            '/api/resource/%i/category' % r.id,
            data=json.dumps(rc_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        rc_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/resource/%i/category' % r.id,
            data=json.dumps(rc_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_resource(self):
        self.test_add_category_to_resource()
        rv = self.app.delete('/api/resource_category/%i' % 1)
        self.assert_success(rv)
        rv = self.app.get(
            '/api/resource/%i/category' % 1, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_resource_change_log_types(self):
        u = self.construct_user(email="editor@sartorgraphy.com", role=Role.admin)
        r = {'id': 258, 'title': "A Resource that is Super and Great", 'description': "You need this resource in your life."}
        rv = self.app.post('api/resource', data=json.dumps(r), content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)

        logs = ResourceChangeLog.query.all()
        self.assertIsNotNone(logs[-1].resource_id)
        self.assertIsNotNone(logs[-1].user_id)
        self.assertEqual(logs[-1].type, 'create')

        rv = self.app.get('api/resource/%i' % r['id'], content_type="application/json")
        self.assert_success(rv)

        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Super Great Resource'
        rv = self.app.put('/api/resource/%i' % r['id'], data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers(user=u))
        self.assert_success(rv)
        rv = self.app.get('/api/resource/%i' % r['id'], content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Super Great Resource')

        logs = ResourceChangeLog.query.all()
        self.assertIsNotNone(logs[-1].resource_id)
        self.assertIsNotNone(logs[-1].user_id)
        self.assertEqual(logs[-1].type, 'edit')

        rv = self.app.delete('api/resource/%i' % r['id'], content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        logs = ResourceChangeLog.query.all()
        self.assertIsNotNone(logs[-1].resource_id)
        self.assertIsNotNone(logs[-1].user_id)
        self.assertEqual(logs[-1].type, 'delete')

    def test_get_resource_change_log_by_resource(self):
        r = self.construct_resource()
        u = self.construct_user(email="editor@sartorgraphy.com", role=Role.admin)
        rv = self.app.get('api/resource/%i' % r.id, content_type="application/json")
        self.assert_success(rv)

        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Super Great Resource'
        rv = self.app.put('/api/resource/%i' % r.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers(user=u))
        self.assert_success(rv)

        rv = self.app.get('/api/resource/%i/change_log' % r.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response[-1]['user_id'], u.id)

    def test_get_resource_change_log_by_user(self):
        r = self.construct_resource()
        u = self.construct_user(email="editor@sartorgraphy.com", role=Role.admin)
        rv = self.app.get('api/resource/%i' % r.id, content_type="application/json")
        self.assert_success(rv)

        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Super Great Resource'
        rv = self.app.put('/api/resource/%i' % r.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers(user=u))
        self.assert_success(rv)

        rv = self.app.get('/api/user/%i/resource_change_log' % u.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response[-1]['resource_id'], r.id)

    def test_covid19_resource_lists(self):
        self.construct_resource(covid19_categories=['COVID-19_for_Autism', 'Free_educational_resources'])
        self.construct_resource(covid19_categories=['COVID-19_for_Autism', 'Edu-tainment', 'Free_educational_resources'])
        self.construct_resource(covid19_categories=['COVID-19_for_Autism', 'Edu-tainment', 'Supports_with_Living'])
        self.construct_resource(covid19_categories=['COVID-19_for_Autism', 'Edu-tainment', 'Visual_Aids'])
        self.construct_resource(covid19_categories=['COVID-19_for_Autism', 'Edu-tainment', 'Health_and_Telehealth'])

        rv = self.app.get('api/resource/covid19/COVID-19_for_Autism', content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response), 5)
        rv = self.app.get('api/resource/covid19/Edu-tainment', content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response), 4)
        rv = self.app.get('api/resource/covid19/Free_educational_resources', content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response), 2)
        rv = self.app.get('api/resource/covid19/Supports_with_Living', content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response), 1)
        rv = self.app.get('api/resource/covid19/Visual_Aids', content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response), 1)
        rv = self.app.get('api/resource/covid19/Health_and_Telehealth', content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response), 1)
