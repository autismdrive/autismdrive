import unittest

from flask import json
from tests.base_test import BaseTest
from app import elastic_index
from app.model.resource_category import ResourceCategory


class TestSearch(BaseTest, unittest.TestCase):

    def search(self, query, user=None):
        """Executes a query as the given user, returning the resulting search results object."""
        rv = self.app.post(
            '/api/search',
            data=json.dumps(query),
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(user))
        self.assert_success(rv)
        return json.loads(rv.get_data(as_text=True))

    def search_anonymous(self, query):
        """Executes a query as an anonymous user, returning the resulting search results object."""
        rv = self.app.post(
            '/api/search',
            data=json.dumps(query),
            follow_redirects=True,
            content_type="application/json")
        self.assert_success(rv)
        return json.loads(rv.get_data(as_text=True))

    def test_search_facets(self):
        elastic_index.clear()
        type_query = {'words': '', 'facets': {"Type": "Resource"}}
        category_query = {'words': '', 'facets': {"Category": ["Space", "Rainbows"]}}
        search_results = self.search(type_query)
        self.assertEqual(0, len(search_results["hits"]))
        search_results = self.search(category_query)
        self.assertEqual(0, len(search_results["hits"]))

        # test that elastic resource is created with post
        c = self.construct_category(name="Rainbows")
        c2 = self.construct_category(name="Space")
        res = self.construct_resource(title="space unicorn", description="delivering rainbows")
        rc = ResourceCategory(resource_id=res.id, category=c, type='resource')
        rc2 = ResourceCategory(resource_id=res.id, category=c2, type='resource')
        rv = self.app.get('api/resource/%i' % res.id, content_type="application/json", follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(type_query)
        self.assertEqual(1, len(search_results["hits"]))
        search_results = self.search(category_query)
        self.assertEqual(1, len(search_results["hits"]))

    def test_study_search_basics(self):
        elastic_index.clear()
        umbrella_query = {'words': 'umbrellas', 'filters': []}
        universe_query = {'words': 'universe', 'filters': []}
        search_results = self.search(umbrella_query)
        self.assertEqual(0, len(search_results["hits"]))
        search_results = self.search(universe_query)
        self.assertEqual(0, len(search_results["hits"]))

        # test that elastic resource is created with post
        o_id = self.construct_organization().id
        study = {'title': "space platypus", 'description': "delivering umbrellas", 'organization_id': o_id}
        rv = self.app.post('api/study', data=json.dumps(study), content_type="application/json",
                           follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))

        search_results = self.search(umbrella_query)
        self.assertEqual(1, len(search_results["hits"]))
        self.assertEqual(search_results['hits'][0]['id'], response['id'])
        search_results = self.search(universe_query)
        self.assertEqual(0, len(search_results["hits"]))

    def test_search_basics(self):
        elastic_index.clear()
        rainbow_query = {'words': 'rainbows', 'filters': []}
        world_query = {'words': 'world', 'filters': []}
        search_results = self.search(rainbow_query)
        self.assertEqual(0, len(search_results["hits"]))
        search_results = self.search(world_query)
        self.assertEqual(0, len(search_results["hits"]))

        # test that elastic resource is created with post
        o_id = self.construct_organization().id
        resource = {'title': "space unicorn", 'description': "delivering rainbows", 'organization_id': o_id}
        rv = self.app.post('api/resource', data=json.dumps(resource), content_type="application/json",
                           follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))

        search_results = self.search(rainbow_query)
        self.assertEqual(1, len(search_results["hits"]))
        self.assertEqual(search_results['hits'][0]['id'], response['id'])
        self.assertEqual(search_results['hits'][0]['title'], response['title'])
        self.assertEqual(search_results['hits'][0]['type'], "Online Information")
        self.assertEqual(search_results['hits'][0]['highlights'], "delivering <em>rainbows</em>")
        self.assertIsNotNone(search_results['hits'][0]['last_updated'])
        search_results = self.search(world_query)
        self.assertEqual(0, len(search_results["hits"]))

    def test_modify_resource_search_basics(self):
        elastic_index.clear()
        rainbow_query = {'words': 'rainbows', 'filters': []}
        world_query = {'words': 'world', 'filters': []}
        # create the resource
        resource = self.construct_resource(
            title='space unicorn', description="delivering rainbows")
        # test that it indeed exists
        rv = self.app.get('/api/resource/%i' % resource.id, content_type="application/json",
                          follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(rainbow_query)
        self.assertEqual(1, len(search_results["hits"]))
        self.assertEqual(search_results['hits'][0]['id'], resource.id)

        response = json.loads(rv.get_data(as_text=True))
        response['description'] = 'all around the world'
        rv = self.app.put('/api/resource/%i' % resource.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(rainbow_query)
        self.assertEqual(0, len(search_results["hits"]))
        search_results = self.search(world_query)
        self.assertEqual(1, len(search_results["hits"]))
        self.assertEqual(resource.id, search_results['hits'][0]['id'])

    def test_delete_search_item(self):
        rainbow_query = {'words': 'rainbows', 'filters': []}
        resource = self.construct_resource(
            title='space unicorn', description="delivering rainbows")
        search_results = self.search(rainbow_query)
        self.assertEqual(1, len(search_results["hits"]))
        elastic_index.remove_document(resource, 'Resource')
        search_results = self.search(rainbow_query)
        self.assertEqual(0, len(search_results["hits"]))
