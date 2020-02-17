import unittest
from flask import json
from tests.base_test import BaseTest
from app import db
from app.model.category import Category


class TestCategory(BaseTest, unittest.TestCase):

    def test_category_basics(self):
        self.construct_category()
        c = db.session.query(Category).first()
        self.assertIsNotNone(c)
        c_id = c.id
        c.parent = self.construct_category(name="3d Printers")
        rv = self.app.get('/api/category/%i' % c_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], c_id)
        self.assertEqual(response["name"], 'Ultimakers')
        self.assertEqual(response["parent"]["name"], '3d Printers')

    def test_modify_category_basics(self):
        self.construct_category()
        c = db.session.query(Category).first()
        self.assertIsNotNone(c)
        c_id = c.id
        c.parent = self.construct_category(name="3d Printers")
        rv = self.app.get('/api/category/%i' % c_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['name'] = 'JellyBoxes'
        new_parent = self.construct_category(name="Strange Kitchen Gadgets")
        response['parent_id'] = new_parent.id
        rv = self.app.put('/api/category/%i' % c_id, data=json.dumps(response),
                          content_type="application/json", follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        db.session.commit()
        rv = self.app.get('/api/category/%i' % c_id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'JellyBoxes')
        self.assertEqual(response['parent']['name'], 'Strange Kitchen Gadgets')

    def test_delete_category(self):
        self.construct_category(name="Unicorns")
        self.construct_category(name="Typewriters")
        c = self.construct_category(name="Pianos")
        c_id = c.id
        rv = self.app.get('api/category/%i' % c_id, content_type="application/json")
        self.assert_success(rv)
        rv = self.app.get('api/category', content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        rv = self.app.delete('api/category/%i' % c_id,
                             content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/category/%i' % c_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)
        rv = self.app.get('api/category', content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(2, len(response))

    def test_delete_category_deletes_descendants(self):
        wool = self.construct_category(name='wool')
        yarn = self.construct_category(name='yarn', parent=wool)
        self.construct_category(name='roving', parent=wool)
        self.construct_category(name='worsted weight', parent=yarn)
        self.construct_category(name='sport weight', parent=yarn)

        rv = self.app.get('api/category/root', content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(2, len(response[0]['children']))

        rv = self.app.get('api/category', content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(5, len(response))

        rv = self.app.delete('api/category/%i' % wool.id,
                             content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/category', content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_create_category(self):
        category = {'name': "My Favorite Things"}
        rv = self.app.post('api/category', data=json.dumps(category),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'My Favorite Things')
        self.assertIsNotNone(response['id'])

    def test_category_has_links(self):
        c = self.construct_category()
        rv = self.app.get(
            '/api/category/' + str(c.id),
            follow_redirects=True,
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["_links"]["self"], '/api/category/' + str(c.id))
        self.assertEqual(response["_links"]["collection"], '/api/category')

    def test_category_has_children(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent=c1)
        rv = self.app.get(
            '/api/category/' + str(c1.id),
            follow_redirects=True,
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["children"][0]['id'], c2.id)
        self.assertEqual(response["children"][0]['name'], "I'm the kid")

    def test_category_has_parents_and_that_parent_has_no_children(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent=c1)
        c3 = self.construct_category(name="I'm the grand kid", parent=c2)
        rv = self.app.get(
            '/api/category/' + str(c3.id),
            follow_redirects=True,
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["parent"]['id'], c2.id)
        self.assertNotIn("children", response["parent"])

    def test_category_can_create_searchable_path(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent=c1)
        c3 = self.construct_category(name="I'm the grand kid", parent=c2)

        c1_path = str(c1.id)
        c2_path = str(c1.id) + "," + str(c2.id)
        c3_path = str(c1.id) + "," + str(c2.id) + "," + str(c3.id)

        self.assertEqual(1, len(c1.all_search_paths()))
        self.assertEqual(2, len(c2.all_search_paths()))
        self.assertEqual(3, len(c3.all_search_paths()))

        self.assertIn(c3_path, c3.all_search_paths())
        self.assertIn(c2_path, c3.all_search_paths())
        self.assertIn(c1_path, c3.all_search_paths())
        self.assertIn(c2_path, c2.all_search_paths())
        self.assertIn(c1_path, c2.all_search_paths())
        self.assertIn(c1_path, c1.all_search_paths())

    # def test_category_depth_is_limited(self):
    #     c1 = self.construct_category()
    #     c2 = self.construct_category(
    #         name="I'm the kid", parent=c1)
    #     c3 = self.construct_category(
    #         name="I'm the grand kid",
    #         parent=c2)
    #     c4 = self.construct_category(
    #         name="I'm the great grand kid",
    #         parent=c3)
    #
    #     rv = self.app.get(
    #         '/api/category',
    #         follow_redirects=True,
    #         content_type="application/json")
    #
    #     self.assert_success(rv)
    #     response = json.loads(rv.get_data(as_text=True))
    #
    #     self.assertEqual(1, len(response))
    #     self.assertEqual(1, len(response[0]["children"]))


