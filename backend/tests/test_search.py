import unittest

from flask import json

from tests.base_test import BaseTest

from app.model.category import Category
from app import elastic_index, db, app


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

    def test_config(self):
        self.assertEqual(elastic_index.index_name, "stardrive_test_resources",
                         msg="Something is wrong with you configuration or import order.  " +
                             "You are not working with the test index.  Make sure the " +
                             "first thing you import in this file is base_test.")

    def test_search_has_counts_by_type(self):
        basic_query = {'words': ''}
        search_results = self.search(basic_query)
        self.assertEqual(0, len(search_results['hits']))

        # test that elastic resource is created with post
        res = self.construct_resource(title="space unicorn", description="delivering rainbows")
        res2 = self.construct_location(title="space unicorn Palace", description="come buy unicorn poop here.")
        rv = self.app.get('api/resource/%i' % res.id, content_type="application/json", follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(basic_query)
        self.assertEqual(2, len(search_results['hits']))

        locations = next(x for x in search_results['type_counts'] if x['value'] == "location")
        resources = next(x for x in search_results['type_counts'] if x['value'] == "resource")
        self.assertEqual(1, locations["count"])
        self.assertEqual(1, resources["count"])

    def test_search_has_counts_by_age_range(self):

        basic_query = {'words': ''}
        search_results = self.search(basic_query)
        self.assertEqual(0, len(search_results['hits']))

        # test that elastic resource is created with post
        res = self.construct_resource(title="Bart", description="free lovin young fella", ages=['young folks'])
        res2 = self.construct_resource(title="Abe", description="delightful grandpop.", ages=['old folks'])
        rv = self.app.get('api/resource/%i' % res.id, content_type="application/json", follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(basic_query)
        self.assertEqual(2, len(search_results['hits']))

        young_folks = next(x for x in search_results['age_counts'] if x['value'] == "young folks")
        old_folks = next(x for x in search_results['age_counts'] if x['value'] == "old folks")

        self.assertEqual(1, young_folks["count"])
        self.assertEqual(1, old_folks["count"])

    def test_study_search_basics(self):
        umbrella_query = {'words': 'umbrellas'}
        universe_query = {'words': 'universe'}
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
        rainbow_query = {'words': 'rainbows'}
        world_query = {'words': 'world'}
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
        location_near = self.construct_location(title='local unicorn',
                                                description="delivering rainbows within the orbit of Uranus",
                                                latitude=38.149595, longitude=-79.072557)

        # Add a location beyond the distance filter
        location_far = self.construct_location(title='distant unicorn',
                                               description="delivering rainbows to the greater Trans-Neptunian Region",
                                               latitude=-38.149595, longitude=100.927443)

        # Add a location somewhere in between
        location_mid = self.construct_location(title='middle unicorn',
                                               description="delivering rainbows somewhere in between",
                                               latitude=37.5246403, longitude=-77.5633015)

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
        rainbow_query = {'words': 'rainbows'}
        world_query = {'words': 'world'}
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
        rainbow_query = {'words': 'rainbows'}
        resource = self.construct_resource(
            title='space unicorn', description="delivering rainbows")
        search_results = self.search(rainbow_query)
        self.assertEqual(1, len(search_results['hits']))
        elastic_index.remove_document(resource, 'Resource')
        search_results = self.search(rainbow_query)
        self.assertEqual(0, len(search_results['hits']))

    def test_search_resources_returns_only_resources(self):
        rainbow_query = {'words': 'rainbows'}

        r = self.construct_resource(title='space unicorn online resource',
                                    description="Electronically-delivered rainbows through the internets")
        l = self.construct_location(title='space unicorn main office',
                                    description="Where rainbows are manufactured for galactic distribution")
        e = self.construct_event(title='space unicorn workshop',
                                 description="Learn how to deliver sparkling rainbows in this interactive workshop")
        s = self.construct_study(title='space unicorn research study',
                                 description="Investigating the long-term outcomes of interstellar unicorn-based delivery of rainbows")

        search_results = self.search_resources(rainbow_query)
        self.assertEqual(3, len(search_results['hits']), 'should only return 3 results')

        expected_types = ['resource', 'location', 'event']
        not_expected_types = ['study']
        self.check_search_results(search_results, expected_types, not_expected_types)

    def test_search_studies_returns_only_studies(self):
        rainbow_query = {'words': 'rainbows'}

        r = self.construct_resource(title='space unicorn online resource',
                                    description="Electronically-delivered rainbows through the internets")
        l = self.construct_location(title='space unicorn main office',
                                    description="Where rainbows are manufactured for galactic distribution")
        e = self.construct_event(title='space unicorn workshop',
                                 description="Learn how to deliver sparkling rainbows in this interactive workshop")
        s = self.construct_study(title='space unicorn research study',
                                 description="Investigating the long-term outcomes of interstellar unicorn-based delivery of rainbows")

        search_results = self.search_studies(rainbow_query)

        self.assertEqual(1, len(search_results['hits']), 'should only return 1 result')

        expected_types = ['study']
        not_expected_types = ['resource', 'location', 'event']
        self.check_search_results(search_results, expected_types, not_expected_types)

    def check_search_results(self, search_results, expected_types, not_expected_types):
        for hit in search_results['hits']:
            self.assertIn(hit['type'], expected_types)
            self.assertNotIn(hit['type'], not_expected_types)

        for expected in expected_types:
            value = next(x for x in search_results['type_counts'] if x['value'] == expected)
            self.assertTrue(value['count'] > 0)

        for expected in not_expected_types:
            for value in search_results['type_counts']:
                if value['value'] == expected:
                    self.assertTrue(value['count'] == 0)

    def setup_category_aggregations(self):
        # There are two types of people in this world.
        makers = self.construct_category(name="Makers")
        talkers = self.construct_category(name="Talkers")
        maker_wood = self.construct_category(name="Woodworkers", parent=makers)
        maker_pot = self.construct_category(name="Potters", parent=makers)
        talker_dreamer = self.construct_category(name="Dreamers", parent=talkers)
        talker_yaya = self.construct_category(name="Le-Me-Tell-Ya-Somethins", parent=talkers)
        maker_wood_cabinet = self.construct_category(name="Cabinet Makers", parent=maker_wood)

        rick = self.construct_resource(title="Rick Hubbard", description="Cabinet maker extrordinair",
                                       categories=[maker_wood_cabinet])
        meghan = self.construct_resource(title="Meghan Williamson", description="A darn good potter",
                                         categories=[maker_pot])
        jon_yap = self.construct_resource(title="Jonny Yapper", description="He shows up to lots of meetins",
                                          categories=[talker_yaya])
        joe_dream_do = self.construct_resource(title="Joe Dream Maker", description="He does it all.",
                                               categories=[makers, talker_dreamer])

    def test_top_level_category_counts(self):
        self.setup_category_aggregations()
        type_query = {'words': ''}
        search_results = self.search(type_query)
        self.assertEqual(4, len(search_results['hits']))
        self.assertIsNotNone(search_results['category'], msg="A category should alwasy exists")
        self.assertEqual("Topics", search_results['category']['name'],
                         msg="It is a top level category if no filters are applied")
        self.assertEqual(2, len(search_results['category']['children']),
                         msg="The two true Top level categories are returned as children")
        maker_cat = search_results['category']['children'][0]
        talker_cat = search_results['category']['children'][1]
        self.assertEquals("Makers", maker_cat['name'], "The first category returned is 'makers'")
        self.assertEquals("Talkers", talker_cat['name'], "The second category returned is 'talkers'")
        self.assertEquals(3, maker_cat['hit_count'], "There are three makers present.")

    def test_top_level_category_repost_does_not_create_error(self):
        self.setup_category_aggregations()
        type_query = {'words': ''}
        search_results = self.search(type_query)
        self.search(search_results)  # This should not create an error.

    def test_second_level_filtered_category_counts(self):
        self.setup_category_aggregations()
        type_query = {'words': '', 'category': {'id': 1}}
        search_results = self.search(type_query)
        self.assertEqual(3, len(search_results['hits']))
        self.assertIsNotNone(search_results['category'], msg="A category should alwasy exists")
        self.assertEqual("Makers", search_results['category']['name'],
                         msg="Selected Category Id should be the category returned")
        self.assertEqual(2, len(search_results['category']['children']),
                         msg="The two true Top level categories are returned as children")
        children = search_results['category']['children']
        self.assertEqual(1, len(list(filter(lambda cat: cat['name'] == 'Woodworkers', children))))
        self.assertEqual(1, len(list(filter(lambda cat: cat['name'] == 'Potters', children))))
        woodworkers = next(x for x in children if x['name'] == "Woodworkers")
        self.assertEquals(1, woodworkers['hit_count'], "There is one wood worker.")

    def test_thrid_level_filtered_category_counts(self):
        self.setup_category_aggregations()
        maker_wood_cat = db.session.query(Category).filter(Category.name == 'Woodworkers').first()
        type_query = {'words': '', 'category': {'id': maker_wood_cat.id}}
        search_results = self.search(type_query)
        self.assertEqual(1, len(search_results['hits']))
        self.assertIsNotNone(search_results['category'], msg="A category should alwasy exists")
        self.assertEqual("Woodworkers", search_results['category']['name'],
                         msg="Selected Category Id should be the category returned")
        self.assertEqual(1, len(search_results['category']['children']), msg="Woodworkers has only one child")
        cabinet_maker = search_results['category']['children'][0]
        self.assertEquals(1, cabinet_maker['hit_count'], "There is one cabinet maker.")

    def test_that_top_level_category_is_always_present(self):
        self.setup_category_aggregations()
        maker_wood_cat = db.session.query(Category).filter(Category.name == 'Woodworkers').first()
        query = {'words': '', 'category': {'id': maker_wood_cat.id}}
        search_results = self.search(query)
        self.assertEquals("Makers", search_results['category']['parent']['name'])
        self.assertEquals("Topics", search_results['category']['parent']['parent']['name'])

    def test_find_related_resource(self):
        # You have to build a lot of documents for this to start working ....  And I liked 1985.

        breakfast_club = self.construct_resource(title="The Breakfast Club",
                                                 description="A 1985 American comedy-drama film written, produced, and "
                                                             "directed by John Hughes. Teenagers from different high "
                                                             "school cliques who spend a Saturday in detention with "
                                                             "their authoritarian assistant principal")
        back_to_the_future = self.construct_location(title="Back to the Future",
                                                     description="1985 American comedy science fiction film directed by"
                                                                 " Robert Zemeckisteenager. Marty McFly, who "
                                                                 "accidentally travels back in time from 1985 to 1955, "
                                                                 "where he meets his future parents and becomes his "
                                                                 "mother's romantic interest.")
        andouillette = self.construct_location(title="Andouillette",
                                               description="A coarse-grained sausage made with pork (or occasionally "
                                                           "veal), intestines or chitterlings, pepper, wine, onions, "
                                                           "and seasonings.")
        goonies = self.construct_location(title="The Goonies",
                                          description="a 1985 American adventure comedy film co-produced"
                                                      " and directed by Richard Donner from a screenplay "
                                                      "by Chris Columbus, based on a story by executive "
                                                      "producer Steven Spielberg. In the film, a band of"
                                                      " kids who live in the \"Goon Docks\" neighborhood")
        weird_sicene = self.construct_location(title="Weird Science",
                                               description="a 1985 American teen comic science fiction film "
                                                           "written and directed by John Hughes and starring "
                                                           "Anthony Michael Hall, Ilan Mitchell-Smith and "
                                                           "Kelly LeBrock.")
        weird_sicene = self.construct_location(title="Weird Science",
                                               description="a 1985 American teen comic science fiction film "
                                                           "written and directed by John Hughes and starring "
                                                           "Anthony Michael Hall, Ilan Mitchell-Smith and "
                                                           "Kelly LeBrock.")
        cocoon = self.construct_location(title="Cocoon",
                                         description="a 1985 American science-fiction fantasy comedy-drama "
                                                     "film directed by Ron Howard about a group of elderly "
                                                     "people rejuvenated by aliens")

        rv = self.app.get('/api/resource/%i/related' % breakfast_club.id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(2, len(response))  # Not really sure why it is just 2, but rolling with it.
        self.assertEqual("Back to the Future", response[0]['title'])

    def test_search_paginates(self):
        self.construct_location(title="one")
        self.construct_location(title="two")
        self.construct_location(title="three")

        query = {'start': 0, 'size': 1}
        search_results = self.search(query)
        self.assertEqual(1, len(search_results['hits']))
        title1 = search_results['hits'][0]['title']

        query = {'start': 1, 'size': 1}
        search_results = self.search(query)
        self.assertEqual(1, len(search_results['hits']))
        title2 = search_results['hits'][0]['title']

        query = {'start': 2, 'size': 1}
        search_results = self.search(query)
        self.assertEqual(1, len(search_results['hits']))
        title3 = search_results['hits'][0]['title']

        self.assertNotEqual(title1, title2)
        self.assertNotEqual(title2, title3)

