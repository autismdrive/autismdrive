import unittest
import json
import dateutil.parser
from datetime import datetime, timedelta

from tests.base_test import BaseTest
from app import elastic_index, db
from app.model.category import Category
from app.model.role import Role


class TestSearch(BaseTest, unittest.TestCase):

    def search(self, query, user=None, path=''):
        """Executes a query as the given user, returning the resulting search results object."""
        rv = self.app.post(
            '/api/search' + path,
            data=self.jsonify(query),
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
            data=self.jsonify(query),
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

    def test_search_has_counts_by_languages(self):

        basic_query = {'words': ''}
        search_results = self.search(basic_query)
        self.assertEqual(0, len(search_results['hits']))

        # test that elastic resource is created with post
        res = self.construct_resource(title="Bart", description="free lovin young fella", languages=['english', 'spanish'])
        res2 = self.construct_resource(title="Abe", description="delightful grandpop.", languages=['english', 'tagalog'])
        rv = self.app.get('api/resource/%i' % res.id, content_type="application/json", follow_redirects=True)
        self.assert_success(rv)
        rv = self.app.get('api/resource/%i' % res2.id, content_type="application/json", follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(basic_query)
        self.assertEqual(2, len(search_results['hits']))

        english = next(x for x in search_results['language_counts'] if x['value'] == "english")
        spanish = next(x for x in search_results['language_counts'] if x['value'] == "spanish")
        tagalog = next(x for x in search_results['language_counts'] if x['value'] == "tagalog")

        self.assertEqual(2, english["count"])
        self.assertEqual(1, spanish["count"])
        self.assertEqual(1, tagalog["count"])

    def test_study_search_basics(self):
        umbrella_query = {'words': 'umbrellas'}
        universe_query = {'words': 'universe'}
        search_results = self.search(umbrella_query)
        self.assertEqual(0, len(search_results['hits']))
        search_results = self.search(universe_query)
        self.assertEqual(0, len(search_results['hits']))

        # test that elastic resource is created with post
        study = {'title': "space platypus", 'description': "delivering umbrellas", 'organization_name': "Study Org"}
        rv = self.app.post('api/study', data=self.jsonify(study), content_type="application/json",
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
        resource = {'title': "space unicorn", 'description': "delivering rainbows", 'organization_name': "Resource Org"}
        rv = self.app.post('api/resource', data=self.jsonify(resource), content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))

        search_results = self.search(rainbow_query)
        self.assertEqual(1, len(search_results['hits']))
        self.assertEqual(search_results['hits'][0]['id'], response['id'])
        self.assertEqual(search_results['hits'][0]['title'], response['title'])
        self.assertEqual(search_results['hits'][0]['type'], "resource")
        self.assertEqual(search_results['hits'][0]['highlights'], "space unicorn delivering <em>rainbows</em>")
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
        rv = self.app.put('/api/resource/%i' % resource.id, data=self.jsonify(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
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

    def test_filter_resources_returns_resources_and_past_events(self):
        rainbow_query = {'types': ['resource']}

        r = self.construct_resource(title='space unicorn online resource',
                                    description="Electronically-delivered rainbows through the internets")
        l = self.construct_location(title='space unicorn main office',
                                    description="Where rainbows are manufactured for galactic distribution")
        future_date = datetime.now() + timedelta(days=7)
        future_event = self.construct_event(title='space unicorn workshop',
                                 description="Learn how to deliver sparkling rainbows in this interactive workshop",
                                 date=future_date)
        past_date = datetime.now() + timedelta(days=-7)
        past_event = self.construct_event(title='space rainbows webinar',
                                 description="Future practical tips on how to generate interplanetary sparkly colors",
                                 post_event_description="Past practical tips on how to generate interplanetary sparkly colors",
                                 date=past_date)
        s = self.construct_study(title='space unicorn research study',
                                 description="Investigating the long-term outcomes of interstellar unicorn-based delivery of rainbows")

        search_results = self.search_resources(rainbow_query)
        self.assertEqual(2, len(search_results['hits']), 'should only return 2 results')

        expected_types = ['resource', 'event']
        not_expected_types = ['study', 'location']
        self.check_search_results(search_results, expected_types, not_expected_types)

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
        self.assertIsNotNone(search_results['category'], msg="A category should always exist")
        self.assertEqual("Topics", search_results['category']['name'],
                         msg="It is a top level category if no filters are applied")
        self.assertEqual(2, len(search_results['category']['children']),
                         msg="The two true Top level categories are returned as children")
        talker_cat = search_results['category']['children'][0]
        maker_cat = search_results['category']['children'][1]
        self.assertEqual("Talkers", talker_cat['name'], "The first category returned is 'talkers'")
        self.assertEqual("Makers", maker_cat['name'], "The second category returned is 'makers'")
        self.assertEqual(3, maker_cat['hit_count'], "There are three makers present.")

    def test_top_level_category_repost_does_not_create_error(self):
        self.setup_category_aggregations()
        type_query = {'words': ''}
        search_results = self.search(type_query)
        self.search(search_results)  # This should not create an error.

    def test_second_level_filtered_category_counts(self):
        self.setup_category_aggregations()
        maker_cat = db.session.query(Category).filter(Category.name == 'Makers').first()
        type_query = {'words': '', 'category': {'id': maker_cat.id}}
        search_results = self.search(type_query)
        self.assertEqual(3, len(search_results['hits']))
        self.assertIsNotNone(search_results['category'], msg="A category should always exist")
        self.assertEqual("Makers", search_results['category']['name'],
                         msg="Selected Category Id should be the category returned")
        self.assertEqual(2, len(search_results['category']['children']),
                         msg="The two true Top level categories are returned as children")
        children = search_results['category']['children']
        self.assertEqual(1, len(list(filter(lambda cat: cat['name'] == 'Woodworkers', children))))
        self.assertEqual(1, len(list(filter(lambda cat: cat['name'] == 'Potters', children))))
        woodworkers = next(x for x in children if x['name'] == "Woodworkers")
        self.assertEqual(1, woodworkers['hit_count'], "There is one wood worker.")

    def test_third_level_filtered_category_counts(self):
        self.setup_category_aggregations()
        maker_wood_cat = db.session.query(Category).filter(Category.name == 'Woodworkers').first()
        type_query = {'words': '', 'category': {'id': maker_wood_cat.id}}
        search_results = self.search(type_query)
        self.assertEqual(1, len(search_results['hits']))
        self.assertIsNotNone(search_results['category'], msg="A category should always exist")
        self.assertEqual("Woodworkers", search_results['category']['name'],
                         msg="Selected Category Id should be the category returned")
        self.assertEqual(1, len(search_results['category']['children']), msg="Woodworkers has only one child")
        cabinet_maker = search_results['category']['children'][0]
        self.assertEqual(1, cabinet_maker['hit_count'], "There is one cabinet maker.")

    def test_that_top_level_category_is_always_present(self):
        self.setup_category_aggregations()
        maker_wood_cat = db.session.query(Category).filter(Category.name == 'Woodworkers').first()
        query = {'words': '', 'category': {'id': maker_wood_cat.id}}
        search_results = self.search(query)
        self.assertEqual("Makers", search_results['category']['parent']['name'])
        self.assertEqual("Topics", search_results['category']['parent']['parent']['name'])

    def test_find_related_resource(self):
        # You have to build a lot of documents for this to start working ....  And I liked 1985.
        movie = self.construct_category("Movies Vaguely Remembered by Middle-Aged Gen Xers")
        sausage = self.construct_category("Sausages of the World")
        sweets = self.construct_category("Delicious Treats Full of Sugar")

        breakfast_club = self.construct_resource(title="The Breakfast Club",
                                                 description="A 1985 American comedy-drama film written, produced, and "
                                                             "directed by John Hughes. Teenagers from different high "
                                                             "school cliques who spend a Saturday in detention with "
                                                             "their authoritarian assistant principal",
                                                 categories=[movie])
        back_to_the_future = self.construct_resource(title="Back to the Future",
                                                     description="1985 American comedy science fiction film directed by"
                                                                 " Robert Zemeckisteenager. Marty McFly, who "
                                                                 "accidentally travels back in time from 1985 to 1955, "
                                                                 "where he meets his future parents and becomes his "
                                                                 "mother's romantic interest.",
                                                     categories=[movie])
        goonies = self.construct_resource(title="The Goonies",
                                          description="a 1985 American adventure comedy film co-produced"
                                                      " and directed by Richard Donner from a screenplay "
                                                      "by Chris Columbus, based on a story by executive "
                                                      "producer Steven Spielberg. In the film, a band of"
                                                      " kids who live in the \"Goon Docks\" neighborhood",
                                          categories=[movie])
        weird_science = self.construct_resource(title="Weird Science",
                                                description="a 1985 American teen comic science fiction film "
                                                            "written and directed by John Hughes and starring "
                                                            "Anthony Michael Hall, Ilan Mitchell-Smith and "
                                                            "Kelly LeBrock.",
                                                categories=[movie])
        cocoon = self.construct_resource(title="Cocoon",
                                         description="a 1985 American science-fiction fantasy comedy-drama "
                                                     "film directed by Ron Howard about a group of elderly "
                                                     "people rejuvenated by aliens",
                                         categories=[movie])
        study = self.construct_study(title="Narrative analysis of 1985 movies vaguely remembered by Middle-Aged Gen Xers",
                                     description="If you remember Marty McFly, who accidentally traveled back in time "
                                                 "from 1985 to 1955, or have watched every John Hughes movie starring "
                                                 "Anthony Michael Hall, feel like you lived in the Goon Docks with "
                                                 "the Goonies, you might be interested in this study.",
                                     participant_description="We're looking for elderly people rejuvenated by aliens, "
                                                             "teens conducting weird science experiments, and parents "
                                                             "who have gone back to the future to spend detention "
                                                             "with their authoritarian assistant principal.",
                                     benefit_description="Participants will receive a cocoon breakfast screenplay "
                                                         "treatment, delivered by a club of band kids from an 1985 "
                                                         "American teen comic science fiction film format.",
                                     categories=[movie])

        # Add a bunch of other irrelevant stuff
        for i in range(10):
            self.construct_resource(title="Andouillette %d" % i,
                                    description="Chorizo Bratwurst Hot Dog Sausage Andouillette Chorizo Bratwurst Hot "
                                                "Dog Sausage Andouillette Chorizo Bratwurst Hot Dog Sausage "
                                                "Andouillette Chorizo Bratwurst Hot Dog Sausage Andouillette Chorizo "
                                                "Bratwurst Hot Dog Sausage Andouillette Chorizo Bratwurst Hot Dog "
                                                "Sausage Andouillette Chorizo Bratwurst Hot Dog Sausage Andouillette "
                                                "Chorizo Bratwurst Hot Dog Sausage Andouillette Chorizo Bratwurst Hot "
                                                "Dog Sausage Andouillette Chorizo Bratwurst Hot Dog Sausage "
                                                "Andouillette %d" % i,
                                    categories=[sausage])
            self.construct_resource(title="Snickers Candy Bar %d" % i,
                                    description="Jaw Breakers Brach's Royals Necco Wafers Snickers Candy Bar Jaw "
                                                "Breakers Brach's Royals Necco Wafers Snickers Candy Bar Jaw Breakers "
                                                "Brach's Royals Necco Wafers Snickers Candy Bar Jaw Breakers Brach's "
                                                "Royals Necco Wafers Snickers Candy Bar Jaw Breakers Brach's Royals "
                                                "Necco Wafers Snickers Candy Bar Jaw Breakers Brach's Royals Necco "
                                                "Wafers Snickers Candy Bar Jaw Breakers Brach's Royals Necco Wafers "
                                                "Snickers Candy Bar Jaw Breakers Brach's Royals Necco Wafers Snickers "
                                                "Candy Bar Jaw Breakers Brach's Royals Necco Wafers Snickers Candy "
                                                "Bar %d" % i,
                                    categories=[sweets])
            self.construct_study(title="The correlation between sausage and beer consumption %d" % i,
                                 description="Chorizo Bratwurst Hot Dog Sausage Andouillette Chorizo Bratwurst Hot "
                                             "Dog Sausage Andouillette Chorizo Bratwurst Hot Dog Sausage Andouillette "
                                             "Chorizo Bratwurst Hot Dog Sausage Andouillette Chorizo Bratwurst Hot "
                                             "Dog Sausage Andouillette Chorizo Bratwurst Hot Dog Sausage Andouillette "
                                             "Chorizo Bratwurst Hot Dog Sausage Andouillette Chorizo Bratwurst Hot "
                                             "Dog Sausage Andouillette Chorizo Bratwurst Hot Dog Sausage Andouillette "
                                             "Chorizo Bratwurst Hot Dog Sausage Andouillette %d" % i,
                                 categories=[sausage])
            self.construct_study(title="Ethnographic study of sugar as a construction material %d" % i,
                                 description="Jaw Breakers Brach's Royals Necco Wafers Snickers Candy Bar Jaw "
                                             "Breakers Brach's Royals Necco Wafers Snickers Candy Bar Jaw Breakers "
                                             "Brach's Royals Necco Wafers Snickers Candy Bar Jaw Breakers Brach's "
                                             "Royals Necco Wafers Snickers Candy Bar Jaw Breakers Brach's Royals "
                                             "Necco Wafers Snickers Candy Bar Jaw Breakers Brach's Royals Necco "
                                             "Wafers Snickers Candy Bar Jaw Breakers Brach's Royals Necco Wafers "
                                             "Snickers Candy Bar Jaw Breakers Brach's Royals Necco Wafers Snickers "
                                             "Candy Bar Jaw Breakers Brach's Royals Necco Wafers Snickers Candy "
                                             "Bar %d" % i,
                                 categories=[sweets])

        rv = self.app.post('/api/related', data=self.jsonify({'resource_id': breakfast_club.id}), content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertTrue('resources' in response.keys())
        self.assertGreater(len(response['resources']), 0)

        self.assertTrue('studies' in response.keys())
        self.assertGreater(len(response['studies']), 0)

        # Most relevant result should be another movie, not sausage or candy
        self.assertIn(response['resources'][0]['title'], [
            back_to_the_future.title,
            goonies.title,
            weird_science.title,
            cocoon.title
        ])
        self.assertIn(study.title, list(map(lambda s: s['title'], response['studies'])))

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

    def test_search_sort_by_date_filters_out_past_events(self):
        now = datetime.now()
        last_year = self.construct_event(title="A year ago", date=now + timedelta(days=-365))
        last_week = self.construct_event(title="A week ago", date=now + timedelta(days=-7))
        yesterday = self.construct_event(title="Yesterday", date=now + timedelta(days=-1))
        tomorrow = self.construct_event(title="Tomorrow", date=now + timedelta(days=1))
        next_week = self.construct_event(title="Next week", date=now + timedelta(days=7))
        next_year = self.construct_event(title="Next year", date=now + timedelta(days=365))

        query = {
            'date': now,
            'sort': {
                'field': 'date',
                'order': 'asc'
            }
        }
        search_results = self.search(query)
        self.assertEqual(3, len(search_results['hits']))
        self.assertEqual(search_results['hits'][0]['title'], tomorrow.title)
        self.assertEqual(search_results['hits'][1]['title'], next_week.title)
        self.assertEqual(search_results['hits'][2]['title'], next_year.title)

    def test_search_filters_out_past_events(self):
        now = datetime.now()
        self.construct_resource(title="How to style unicorn hair")
        self.construct_resource(title="Rainbow-emitting capabilities of unicorn horns")
        self.construct_resource(title="Tips for time travel with a unicorn")
        self.construct_event(
            title="Unicorn council last year",
            date=now + timedelta(days=-365),
            description="Upcoming unicorn council",
            post_event_description="Previously recorded unicorn council"
        )
        self.construct_event(title="Unicorn meetup a week ago", date=now + timedelta(days=-7))
        self.construct_event(title="Unicorn workshop yesterday", date=now + timedelta(days=-1))
        self.construct_event(title="Unicorn playdate tomorrow", date=now + timedelta(days=1))
        self.construct_event(title="Unicorn training next week", date=now + timedelta(days=7))
        self.construct_event(title="Unicorn conference next year", date=now + timedelta(days=365))

        # Should return future events, plus past events that have a post_event_description
        query = {'words': 'unicorn'}
        search_results = self.search(query)
        self.assertEqual(7, len(search_results['hits']))
        for hit in search_results['hits']:
            if hit['type'] == 'event':
                hit_date = dateutil.parser.parse(hit['date'])
                if hit_date >= now:
                    self.assertGreaterEqual(hit_date, now)
                else:
                    self.assertTrue('post_event_description' in hit, 'Hit has no post-event description.')
                    self.assertIsNotNone(hit['post_event_description'], 'Post-event description is empty.')
            else:
                self.assertTrue(hit['date'] is None)

        # Should only return future events when filtering by event type
        event_query = {'words': 'unicorn', 'types': ['event']}
        event_search_results = self.search(event_query)
        self.assertEqual(3, len(event_search_results['hits']))
        for hit in event_search_results['hits']:
            self.assertEqual(hit['type'], 'event')
            hit_date = dateutil.parser.parse(hit['date'])
            self.assertGreaterEqual(hit_date, now)

    def test_search_for_map_points_only(self):

        # Add some locations with coordinates, and some with out.
        location_near = self.construct_location(title='local unicorn',
                                                description="delivering rainbows within the orbit of Uranus",
                                                latitude=38.149595, longitude=-79.072557)
        location_far = self.construct_location(title='distant unicorn',
                                               description="delivering rainbows to the greater Trans-Neptunian Region",
                                               latitude=-38.149595, longitude=100.927443)
        location_mid = self.construct_location(title='middle unicorn',
                                               description="delivering rainbows somewhere in between",
                                               latitude=37.5246403, longitude=-77.5633015)
        self.construct_resource(title="Rainbow with a bad hair day and no place to be.")
        self.construct_resource(title="A non-rainbow blue sky that covers nearly all locations.")
        self.construct_resource(title="A very very tiny rainbow in a sprinkler, that occurs in various places.")


        query = {'words': 'rainbows'}
        search_results = self.search(query)
        self.assertEqual(6, len(search_results['hits']))

        query = {'words': 'rainbows', 'map_data_only': True}
        search_results = self.search(query)
        self.assertEqual(3, len(search_results['hits']))
        self.assertTrue('latitude' in search_results['hits'][0])
        self.assertTrue('longitude' in search_results['hits'][0])
        self.assertFalse('content' in search_results['hits'][0])
        self.assertFalse('description' in search_results['hits'][0])
        self.assertFalse('highlights' in search_results['hits'][0])

    def test_study_search_record_updates(self):
        umbrella_query = {'words': 'umbrellas'}

        # test that elastic resource is created with post
        study = {'status': "currently_enrolling", 'title': "space platypus", 'description': "delivering umbrellas",
                 'organization_name': "Study Org"}
        rv = self.app.post('api/study', data=self.jsonify(study), content_type="application/json",
                           follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        s_id = response['id']

        search_results = self.search(umbrella_query)
        self.assertEqual(1, len(search_results['hits']))
        self.assertEqual(search_results['hits'][0]['id'], s_id)
        self.assertEqual(search_results['hits'][0]['status'], 'Currently enrolling')

        response['status'] = "study_in_progress"
        rv = self.app.put('/api/study/%i' % s_id, data=self.jsonify(response), content_type="application/json",
                          follow_redirects=True)
        self.assert_success(rv)
        rv = self.app.get('/api/study/%i' % s_id, content_type="application/json")
        self.assert_success(rv)

        search_results = self.search(umbrella_query)
        self.assertEqual(1, len(search_results['hits']))
        self.assertEqual(search_results['hits'][0]['id'], s_id)
        self.assertEqual(search_results['hits'][0]['status'], 'Study in progress')

    def test_search_with_drafts(self):
        resource_query = {'words': 'resource'}
        password = 'Silly password 305 for all the pretend users'

        self.construct_resource(title="Drafty Draft Draft Resource", is_draft=True)
        self.construct_resource(title="Published Resource", is_draft=False)
        self.construct_resource(title="Officially Published Resource", is_draft=False)
        self.construct_resource(title="A Draft Resource for the ages", is_draft=True)
        admin = self.construct_user(email='admin@sartography.com', role=Role.admin)
        editor = self.construct_user(email='editor@sartography.com', role=Role.editor)
        researcher = self.construct_user(email='researcher@sartography.com', role=Role.researcher)
        user = self.construct_user(email='user@sartography.com', role=Role.user)

        self.login_user(admin, password)
        search_results = self.search(resource_query, user=admin)
        self.assertEqual(4, len(search_results['hits']))
        self.login_user(editor, password)
        search_results = self.search(resource_query, user=editor)
        self.assertEqual(4, len(search_results['hits']))
        self.login_user(researcher, password)
        search_results = self.search(resource_query, user=researcher)
        self.assertEqual(2, len(search_results['hits']))
        self.login_user(user, password)
        search_results = self.search(resource_query, user=user)
        self.assertEqual(2, len(search_results['hits']))

    def login_user(self, user, password):
        user.email_verified = True
        user.password = password
        db.session.add(user)
        data = {'email': user.email, 'password': password}
        rv = self.app.post(
            '/api/login_password',
            data=self.jsonify(data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response["token"])
