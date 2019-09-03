import unittest

from flask import json
from tests.base_test import BaseTest
from app import elastic_index
from app.model.resource_category import ResourceCategory


class TestSearch(BaseTest, unittest.TestCase):

    def search(self, query, user=None, path=''):
        """Executes a query as the given user, returning the resulting search results object."""
        rv = self.app.post(
            '/api/search' + path,
            data=json.dumps(query),
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(user))
        self.assert_success(rv)
        return json.loads(rv.get_data(as_text=True))

    def search_resources(self, query, user=None):
        return self.search(query, user, '/resources')

    def search_studies(self, query, user=None):
        return self.search(query, user, '/studies')

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
        self.assertEqual(0, len(search_results['hits']))
        search_results = self.search(category_query)
        self.assertEqual(0, len(search_results['hits']))

        # test that elastic resource is created with post
        c = self.construct_category(name="Rainbows")
        c2 = self.construct_category(name="Space")
        res = self.construct_resource(title="space unicorn", description="delivering rainbows")
        rc = ResourceCategory(resource_id=res.id, category=c, type='resource')
        rc2 = ResourceCategory(resource_id=res.id, category=c2, type='resource')
        rv = self.app.get('api/resource/%i' % res.id, content_type="application/json", follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(type_query)
        self.assertEqual(1, len(search_results['hits']))
        search_results = self.search(category_query)
        self.assertEqual(1, len(search_results['hits']))

    def test_study_search_basics(self):
        elastic_index.clear()
        umbrella_query = {'words': 'umbrellas', 'filters': []}
        universe_query = {'words': 'universe', 'filters': []}
        search_results = self.search(umbrella_query)
        self.assertEqual(0, len(search_results['hits']))
        search_results = self.search(universe_query)
        self.assertEqual(0, len(search_results['hits']))

        # test that elastic resource is created with post
        o_id = self.construct_organization().id
        study = {'title': "space platypus", 'description': "delivering umbrellas", 'organization_id': o_id}
        rv = self.app.post('api/study', data=json.dumps(study), content_type="application/json",
                           follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))

        search_results = self.search(umbrella_query)
        self.assertEqual(1, len(search_results['hits']))
        self.assertEqual(search_results['hits'][0]['id'], response['id'])
        search_results = self.search(universe_query)
        self.assertEqual(0, len(search_results['hits']))

    def test_search_basics(self):
        elastic_index.clear()
        rainbow_query = {'words': 'rainbows', 'filters': []}
        world_query = {'words': 'world', 'filters': []}
        search_results = self.search(rainbow_query)
        self.assertEqual(0, len(search_results['hits']))
        search_results = self.search(world_query)
        self.assertEqual(0, len(search_results['hits']))

        # test that elastic resource is created with post
        o_id = self.construct_organization().id
        resource = {'title': "space unicorn", 'description': "delivering rainbows", 'organization_id': o_id}
        rv = self.app.post('api/resource', data=json.dumps(resource), content_type="application/json",
                           follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))

        search_results = self.search(rainbow_query)
        self.assertEqual(1, len(search_results['hits']))
        self.assertEqual(search_results['hits'][0]['id'], response['id'])
        self.assertEqual(search_results['hits'][0]['title'], response['title'])
        self.assertEqual(search_results['hits'][0]['type'], "resource")
        self.assertEqual(search_results['hits'][0]['highlights'], "delivering <em>rainbows</em>")
        self.assertIsNotNone(search_results['hits'][0]['last_updated'])
        search_results = self.search(world_query)
        self.assertEqual(0, len(search_results['hits']))

    def test_search_location_by_geo_point(self):
        elastic_index.clear()
        geo_query = {
            'words': 'rainbows',
            'sort': {
                'field': 'geo_point',
                'latitude': 38.065229,
                'longitude': -79.079076,
                'order': 'asc',
                'unit': 'mi'
            }
        }

        # Add a location within the distance filter
        location_near = self.construct_location(title='local unicorn', description="delivering rainbows within the orbit of Uranus", latitude=38.149595, longitude=-79.072557)

        # Add a location beyond the distance filter
        location_far = self.construct_location(title='distant unicorn', description="delivering rainbows to the greater Trans-Neptunian Region", latitude=-38.149595, longitude=100.927443)

        # Add a location somewhere in between
        location_mid = self.construct_location(title='middle unicorn', description="delivering rainbows somewhere in between", latitude=37.5246403, longitude=-77.5633015)

        search_results = self.search(geo_query)
        self.assertEqual(3, len(search_results['hits']))
        self.assertIsNotNone(search_results['hits'][0]['latitude'])
        self.assertIsNotNone(search_results['hits'][0]['longitude'])
        self.assertEqual(search_results['hits'][0]['title'], location_near.title)
        self.assertEqual(search_results['hits'][1]['title'], location_mid.title)
        self.assertEqual(search_results['hits'][2]['title'], location_far.title)

        # Reverse the sort order
        geo_query['sort']['order'] = 'desc'
        search_results = self.search(geo_query)
        self.assertEqual(3, len(search_results['hits']))
        self.assertIsNotNone(search_results['hits'][0]['latitude'])
        self.assertIsNotNone(search_results['hits'][0]['longitude'])
        self.assertEqual(search_results['hits'][0]['title'], location_far.title)
        self.assertEqual(search_results['hits'][1]['title'], location_mid.title)
        self.assertEqual(search_results['hits'][2]['title'], location_near.title)

        # Change which point is closest
        geo_query['sort']['latitude'] = location_mid.latitude
        geo_query['sort']['longitude'] = location_mid.longitude
        geo_query['sort']['order'] = 'asc'
        search_results = self.search(geo_query)
        self.assertEqual(3, len(search_results['hits']))
        self.assertIsNotNone(search_results['hits'][0]['latitude'])
        self.assertIsNotNone(search_results['hits'][0]['longitude'])
        self.assertEqual(search_results['hits'][0]['title'], location_mid.title)
        self.assertEqual(search_results['hits'][1]['title'], location_near.title)
        self.assertEqual(search_results['hits'][2]['title'], location_far.title)

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
        self.assertEqual(1, len(search_results['hits']))
        self.assertEqual(search_results['hits'][0]['id'], resource.id)

        response = json.loads(rv.get_data(as_text=True))
        response['description'] = 'all around the world'
        rv = self.app.put('/api/resource/%i' % resource.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(rainbow_query)
        self.assertEqual(0, len(search_results['hits']))
        search_results = self.search(world_query)
        self.assertEqual(1, len(search_results['hits']))
        self.assertEqual(resource.id, search_results['hits'][0]['id'])

    def test_delete_search_item(self):
        rainbow_query = {'words': 'rainbows', 'filters': []}
        resource = self.construct_resource(
            title='space unicorn', description="delivering rainbows")
        search_results = self.search(rainbow_query)
        self.assertEqual(1, len(search_results['hits']))
        elastic_index.remove_document(resource, 'Resource')
        search_results = self.search(rainbow_query)
        self.assertEqual(0, len(search_results['hits']))

    def test_search_resources_returns_only_resources(self):
        elastic_index.clear()
        rainbow_query = {'words': 'rainbows', 'filters': []}

        r = self.construct_resource(title='space unicorn online resource', description="Electronically-delivered rainbows through the internets")
        l = self.construct_location(title='space unicorn main office', description="Where rainbows are manufactured for galactic distribution")
        e = self.construct_event(title='space unicorn workshop', description="Learn how to deliver sparkling rainbows in this interactive workshop")
        s = self.construct_study(title='space unicorn research study', description="Investigating the long-term outcomes of interstellar unicorn-based delivery of rainbows")

        search_results = self.search_resources(rainbow_query)
        self.assertEqual(3, len(search_results['hits']), 'should only return 3 results')

        expected_types = ['Online Information', 'Local Services', 'Events and Training']
        not_expected_types = ['Research Studies']
        self.check_search_results(search_results, expected_types, not_expected_types)

    def test_search_studies_returns_only_studies(self):
        elastic_index.clear()
        rainbow_query = {'words': 'rainbows', 'filters': []}

        r = self.construct_resource(title='space unicorn online resource', description="Electronically-delivered rainbows through the internets")
        l = self.construct_location(title='space unicorn main office', description="Where rainbows are manufactured for galactic distribution")
        e = self.construct_event(title='space unicorn workshop', description="Learn how to deliver sparkling rainbows in this interactive workshop")
        s = self.construct_study(title='space unicorn research study', description="Investigating the long-term outcomes of interstellar unicorn-based delivery of rainbows")

        search_results = self.search_studies(rainbow_query)

        self.assertEqual(1, len(search_results['hits']), 'should only return 1 result')

        expected_types = ['Research Studies']
        not_expected_types = ['Online Information', 'Local Services', 'Events and Training']
        self.check_search_results(search_results, expected_types, not_expected_types)

    def check_search_results(self, search_results, expected_types, not_expected_types):
        for hit in search_results['hits']:
            self.assertIn(hit['label'], expected_types)
            self.assertNotIn(hit['label'], not_expected_types)

        for facet in search_results['facets']:
            if facet['field'] == 'Type':
                for fc in facet['facetCounts']:
                    self.assertIn(fc['category'], expected_types)
                    self.assertNotIn(fc['category'], not_expected_types)
