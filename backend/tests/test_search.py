from datetime import datetime, timedelta

import dateutil.parser
from math import floor
from sqlalchemy import asc, select

from app.elastic_index import elastic_index
from app.enums import Role, Status
from app.models import Category, Resource
from fixtures.fixure_utils import fake
from fixtures.resource import MockResource
from fixtures.study import MockStudy
from tests.base_test import BaseTest


def fake_params(kw):
    return {
        "title": f"{fake.catch_phrase()} {kw} {fake.catch_phrase()}",
        "description": f"{fake.sentence()} {kw} {fake.sentence()}",
    }


class TestSearch(BaseTest):
    def construct_content(self, keyword, add_past_event=False):
        self.construct_resource(**fake_params(keyword))
        self.construct_location(**fake_params(keyword))
        self.construct_event(**fake_params(keyword))
        self.construct_study(**fake_params(keyword))
        if add_past_event:
            self.construct_event(
                **fake_params(keyword), post_event_description=fake.sentence(), date=fake.past_datetime()
            )

    def search(self, query, user=None, path=""):
        """Executes a query as the given user, returning the resulting search results object."""
        rv = self.client.post(
            "/api/search" + path,
            data=self.jsonify(query),
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(user),
        )
        self.assert_success(rv)
        return rv.json

    def search_resources(self, query, user=None):
        return self.search(query, user, "/resources")

    def search_studies(self, query, user=None):
        return self.search(query, user, "/studies")

    def search_anonymous(self, query):
        """Executes a query as an anonymous user, returning the resulting search results object."""
        rv = self.client.post(
            "/api/search", data=self.jsonify(query), follow_redirects=True, content_type="application/json"
        )
        self.assert_success(rv)
        return rv.json

    def test_config(self):
        self.assertEqual(
            elastic_index.index_name,
            "stardrive_test_resources",
            msg="Something is wrong with you configuration or import order.  "
            + "You are not working with the test index.  Make sure the "
            + "first thing you import in this file is base_test.",
        )

    def test_search_has_counts_by_type(self):
        kw = "unicorn"
        basic_query = {"words": kw}
        search_results = self.search(basic_query)
        self.assertEqual(0, len(search_results["hits"]))

        # test that elastic resource is created with post
        res = self.construct_resource(
            title=f"{fake.catch_phrase()} {kw} {fake.catch_phrase()}",
            description=f"{fake.sentence()} {kw} {fake.sentence()}",
            is_draft=False,
        )
        res2 = self.construct_location(
            title=f"{fake.catch_phrase()} {kw} {fake.catch_phrase()}",
            description=f"{fake.sentence()} {kw} {fake.sentence()}",
            is_draft=False,
        )
        rv = self.client.get("api/resource/%i" % res.id, content_type="application/json", follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(basic_query)
        self.assertEqual(2, len(search_results["hits"]))

        locations = next(x for x in search_results["type_counts"] if x["value"] == "location")
        resources = next(x for x in search_results["type_counts"] if x["value"] == "resource")
        self.assertEqual(1, locations["count"])
        self.assertEqual(1, resources["count"])

    def test_search_has_counts_by_age_range(self):

        basic_query = {"words": ""}
        search_results = self.search(basic_query)
        self.assertEqual(0, len(search_results["hits"]))

        # test that elastic resource is created with post
        res = self.construct_resource(title="Bart", description="free lovin young fella", ages=["young folks"])
        res2 = self.construct_resource(title="Abe", description="delightful grandpop.", ages=["old folks"])
        rv = self.client.get("api/resource/%i" % res.id, content_type="application/json", follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(basic_query)
        self.assertEqual(2, len(search_results["hits"]))

        young_folks = next(x for x in search_results["age_counts"] if x["value"] == "young folks")
        old_folks = next(x for x in search_results["age_counts"] if x["value"] == "old folks")

        self.assertEqual(1, young_folks["count"])
        self.assertEqual(1, old_folks["count"])

    def test_search_has_counts_by_languages(self):

        basic_query = {"words": ""}
        search_results = self.search(basic_query)
        self.assertEqual(0, len(search_results["hits"]))

        # test that elastic resource is created with post
        res = self.construct_resource(
            title="Bart", description="free lovin young fella", languages=["english", "spanish"]
        )
        res2 = self.construct_resource(
            title="Abe", description="delightful grandpop.", languages=["english", "tagalog"]
        )
        rv = self.client.get("api/resource/%i" % res.id, content_type="application/json", follow_redirects=True)
        self.assert_success(rv)
        rv = self.client.get("api/resource/%i" % res2.id, content_type="application/json", follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(basic_query)
        self.assertEqual(2, len(search_results["hits"]))

        english = next(x for x in search_results["language_counts"] if x["value"] == "english")
        spanish = next(x for x in search_results["language_counts"] if x["value"] == "spanish")
        tagalog = next(x for x in search_results["language_counts"] if x["value"] == "tagalog")

        self.assertEqual(2, english["count"])
        self.assertEqual(1, spanish["count"])
        self.assertEqual(1, tagalog["count"])

    def test_study_search_basics(self):
        umbrella_query = {"words": "umbrellas"}
        universe_query = {"words": "universe"}
        search_results = self.search(umbrella_query)
        self.assertEqual(0, len(search_results["hits"]))
        search_results = self.search(universe_query)
        self.assertEqual(0, len(search_results["hits"]))

        # test that elastic resource is created with post
        study = {"title": "space platypus", "description": "delivering umbrellas", "organization_name": "Study Org"}
        rv = self.client.post(
            "api/study", data=self.jsonify(study), content_type="application/json", follow_redirects=True
        )
        self.assert_success(rv)
        response = rv.json

        search_results = self.search(umbrella_query)
        self.assertEqual(1, len(search_results["hits"]))
        self.assertEqual(search_results["hits"][0]["id"], response["id"])
        search_results = self.search(universe_query)
        self.assertEqual(0, len(search_results["hits"]))

    def test_search_basics(self):
        rainbow_query = {"words": "rainbows"}
        world_query = {"words": "world"}
        search_results = self.search(rainbow_query)
        self.assertEqual(0, len(search_results["hits"]))
        search_results = self.search(world_query)
        self.assertEqual(0, len(search_results["hits"]))

        # test that elastic resource is created with post
        resource = MockResource(
            title="space unicorn", description="delivering rainbows", organization_name="Resource Org", is_draft=False
        )
        rv = self.client.post(
            "api/resource",
            data=self.jsonify(resource),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json

        search_results = self.search(rainbow_query)
        hits = search_results["hits"]
        self.assertEqual(1, len(hits))

        hit = hits[0]
        self.assertEqual(hit["id"], response["id"])
        self.assertEqual(hit["title"], response["title"])
        self.assertEqual(hit["type"], "resource")
        self.assertEqual(hit["highlights"], "space unicorn delivering <em>rainbows</em>")
        self.assertIsNotNone(hit["last_updated"])
        search_results = self.search(world_query)
        self.assertEqual(0, len(search_results["hits"]))

    def test_search_location_by_geo_point(self):
        geo_query = {
            "words": "rainbows",
            "sort": {
                "field": "geo_point",
                "latitude": 38.065229,
                "longitude": -79.079076,
                "order": "asc",
                "unit": "mi",
            },
        }

        # Add a location within the distance filter
        location_near = self.construct_location(
            title="local unicorn",
            description="delivering rainbows within the orbit of Uranus",
            latitude=38.149595,
            longitude=-79.072557,
        )

        # Add a location beyond the distance filter
        location_far = self.construct_location(
            title="distant unicorn",
            description="delivering rainbows to the greater Trans-Neptunian Region",
            latitude=-38.149595,
            longitude=100.927443,
        )

        # Add a location somewhere in between
        location_mid = self.construct_location(
            title="middle unicorn",
            description="delivering rainbows somewhere in between",
            latitude=37.5246403,
            longitude=-77.5633015,
        )

        search_results = self.search(geo_query)
        self.assertEqual(3, len(search_results["hits"]))
        self.assertIsNotNone(search_results["hits"][0]["latitude"])
        self.assertIsNotNone(search_results["hits"][0]["longitude"])
        self.assertEqual(search_results["hits"][0]["title"], location_near.title)
        self.assertEqual(search_results["hits"][1]["title"], location_mid.title)
        self.assertEqual(search_results["hits"][2]["title"], location_far.title)

        # Reverse the sort order
        geo_query["sort"]["order"] = "desc"
        search_results = self.search(geo_query)
        self.assertEqual(3, len(search_results["hits"]))
        self.assertIsNotNone(search_results["hits"][0]["latitude"])
        self.assertIsNotNone(search_results["hits"][0]["longitude"])
        self.assertEqual(search_results["hits"][0]["title"], location_far.title)
        self.assertEqual(search_results["hits"][1]["title"], location_mid.title)
        self.assertEqual(search_results["hits"][2]["title"], location_near.title)

        # Change which point is closest
        geo_query["sort"]["latitude"] = location_mid.latitude
        geo_query["sort"]["longitude"] = location_mid.longitude
        geo_query["sort"]["order"] = "asc"
        search_results = self.search(geo_query)
        self.assertEqual(3, len(search_results["hits"]))
        self.assertIsNotNone(search_results["hits"][0]["latitude"])
        self.assertIsNotNone(search_results["hits"][0]["longitude"])
        self.assertEqual(search_results["hits"][0]["title"], location_mid.title)
        self.assertEqual(search_results["hits"][1]["title"], location_near.title)
        self.assertEqual(search_results["hits"][2]["title"], location_far.title)

    def test_geo_box_query(self):
        location_near = self.construct_location(
            title="local unicorn",
            description="delivering rainbows within the orbit of Uranus",
            latitude=38.149595,
            longitude=-93,
        )

        location_not_near = self.construct_location(
            title="local", description="delivering rainbows", latitude=28.149595, longitude=-93
        )
        geo_query = {
            "geo_box": {
                "top_left": {"lat": 39, "lon": -94},
                "bottom_right": {"lat": 38, "lon": -92},
            }
        }
        search_results = self.search(geo_query)
        self.assertEqual(1, len(search_results["hits"]))

    def test_modify_resource_search_basics(self):
        rainbow_query = {"words": "rainbows"}
        world_query = {"words": "world"}
        # create the resource
        resource = self.construct_resource(title="space unicorn", description="delivering rainbows", is_draft=False)
        resource_id = resource.id
        # test that it indeed exists
        rv = self.client.get("/api/resource/%i" % resource_id, content_type="application/json", follow_redirects=True)
        self.assert_success(rv)

        search_results = self.search(rainbow_query)
        self.assertEqual(1, len(search_results["hits"]))
        self.assertEqual(search_results["hits"][0]["id"], resource_id)

        response = rv.json
        response["description"] = "all around the world"
        rv = self.client.put(
            "/api/resource/%i" % resource_id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)

        search_results = self.search(rainbow_query)
        self.assertEqual(0, len(search_results["hits"]))
        search_results = self.search(world_query)
        self.assertEqual(1, len(search_results["hits"]))
        self.assertEqual(resource_id, search_results["hits"][0]["id"])

    def test_delete_search_item(self):
        kw = "rainbows"
        kw_query = {"words": kw}
        resource = self.construct_resource(
            title=f"{fake.catch_phrase()} {kw} {fake.catch_phrase()}",
            description=f"{fake.paragraph()} {kw} {fake.paragraph()}",
            is_draft=False,
        )
        resource_id = resource.id

        search_results = self.search(kw_query)
        self.assertEqual(1, len(search_results["hits"]))

        db_resource = self.session.query(Resource).filter_by(id=resource_id).first()
        elastic_index.remove_document(db_resource)

        search_results = self.search(kw_query)
        self.assertEqual(0, len(search_results["hits"]))

    def test_filter_resources_returns_resources_and_past_events(self):
        kw = "rainbows"
        resource_query = {"types": ["resource"]}

        self.construct_content(kw, add_past_event=True)

        search_results = self.search_resources(resource_query)
        self.assertEqual(2, len(search_results["hits"]), "should only return 2 results")

        expected_types = ["resource", "event"]
        not_expected_types = ["study", "location"]
        self.check_search_results(search_results, expected_types, not_expected_types)

    def test_search_resources_returns_only_resources(self):
        kw = "rainbows"
        rainbow_query = {"words": kw}

        self.construct_content(kw)

        search_results = self.search_resources(rainbow_query)
        self.assertEqual(3, len(search_results["hits"]), "should only return 3 results")

        expected_types = ["resource", "location", "event"]
        not_expected_types = ["study"]
        self.check_search_results(search_results, expected_types, not_expected_types)

    def test_search_studies_returns_only_studies(self):
        kw = "rainbows"
        rainbow_query = {"words": kw}

        self.construct_content(kw)

        search_results = self.search_studies(rainbow_query)

        self.assertEqual(1, len(search_results["hits"]), "should only return 1 result")

        expected_types = ["study"]
        not_expected_types = ["resource", "location", "event"]
        self.check_search_results(search_results, expected_types, not_expected_types)

    def check_search_results(self, search_results, expected_types, not_expected_types):
        for hit in search_results["hits"]:
            self.assertIn(hit["type"], expected_types)
            self.assertNotIn(hit["type"], not_expected_types)

        for expected in expected_types:
            value = next(x for x in search_results["type_counts"] if x["value"] == expected)
            self.assertTrue(value["count"] > 0)

        for expected in not_expected_types:
            for value in search_results["type_counts"]:
                if value["value"] == expected:
                    self.assertTrue(value["count"] == 0)

    def setup_category_aggregations(self, num_cats=7, num_resources=4) -> tuple[list[Category], list[Resource]]:
        names: list[str] = fake.words(nb=num_cats, part_of_speech="noun")
        categories = []
        resources = []
        for i, name in enumerate(names):
            _top = i <= 1
            parent_index = None if _top else floor((i - 1) / 2)
            categories.append(self.construct_category(name=name, parent=None if _top else categories[parent_index]))

        for i in range(num_resources):
            r_cat = categories[len(categories) - 1 - i]
            r_cats = [r_cat] if i < num_resources - 1 else [categories[1], r_cat]
            resources.append(
                self.construct_resource(
                    title=fake.catch_phrase(), description=fake.sentence(), categories=r_cats, is_draft=False
                )
            )

        db_categories = list(self.session.execute(select(Category).order_by(asc(Category.id))).unique().scalars().all())
        db_resources = list(self.session.execute(select(Resource).order_by(asc(Resource.id))).unique().scalars().all())

        return db_categories, db_resources

    def test_top_level_category_counts(self):
        num_cats = 7
        num_resources = 4
        categories, resources = self.setup_category_aggregations(num_cats, num_resources)
        type_query = {"words": ""}
        search_results = self.search(type_query)
        self.assertEqual(num_resources, len(search_results["hits"]))
        self.assertIsNotNone(search_results["category"], msg="A category should always exist")
        self.assertEqual(
            "Topics", search_results["category"]["name"], msg="It is a top level category if no filters are applied"
        )
        self.assertEqual(
            2,
            len(search_results["category"]["children"]),
            msg="The two true Top level categories are returned as children",
        )

        for i, cat in enumerate(search_results["category"]["children"]):
            self.assertEqual(categories[i].name, cat["name"], f"The first category should be {categories[i].name}")
            self.assertEqual(2, cat["hit_count"], f"There should be 2 resources in {categories[i].name}")

    def test_top_level_category_repost_does_not_create_error(self):
        self.setup_category_aggregations()
        type_query = {"words": ""}
        search_results = self.search(type_query)
        self.search(search_results)  # This should not create an error.

    def test_second_level_filtered_category_counts(self):
        categories, resources = self.setup_category_aggregations()
        type_query = {"words": "", "category": {"id": categories[1].id}}
        search_results = self.search(type_query)

        self.assertEqual(2, len(search_results["hits"]))
        self.assertIsNotNone(search_results["category"], msg="A category should always exist")
        self.assertEqual(
            categories[1].name,
            search_results["category"]["name"],
            msg="Selected Category Id should be the category returned",
        )
        self.assertEqual(
            2,
            len(search_results["category"]["children"]),
            msg="The two true Top level categories are returned as children",
        )
        children = search_results["category"]["children"]
        for cat in children:
            num_db_resources = len(categories[cat["id"] - 1].resources)
            self.assertGreater(num_db_resources, 0, f"There should be resources in category {cat['id']}")
            self.assertEqual(
                num_db_resources,
                cat["hit_count"],
                f"There should be {num_db_resources} resource in search results for category {cat['id']}",
            )

    def test_third_level_filtered_category_counts(self):
        categories, resources = self.setup_category_aggregations()
        cat = categories[0].children[0]
        type_query = {"words": "", "category": {"id": cat.id}}
        search_results = self.search(type_query)
        self.assertEqual(2, len(search_results["hits"]))
        self.assertIsNotNone(search_results["category"], msg="A category should always exist")
        self.assertEqual(
            cat.name,
            search_results["category"]["name"],
            msg="Selected Category Id should be the category returned",
        )
        self.assertEqual(
            2, len(search_results["category"]["children"]), msg=f"Category {cat.id} should have 2 child categories"
        )
        grandchild = search_results["category"]["children"][0]
        self.assertEqual(1, grandchild["hit_count"], f"Category {cat.id} search results should have one resource")

    def test_that_top_level_category_is_always_present(self):
        categories, resources = self.setup_category_aggregations()
        cat = categories[0].children[0]
        query = {"words": "", "category": {"id": cat.id}}
        search_results = self.search(query)
        self.assertEqual(cat.parent.name, search_results["category"]["parent"]["name"])
        self.assertEqual("Topics", search_results["category"]["parent"]["parent"]["name"])

    def test_find_related_resource(self):
        resource_id: int
        category_name: str

        num_categories = 3
        categories = []
        for _ in range(num_categories):
            categories.append(self.construct_category(name=fake.word()))

        num_resources = 24
        resources = []
        for i in range(num_resources):
            category = categories[i % 3]
            title = f"{category.name} {fake.sentence()}"
            resource = self.construct_resource(**MockResource(title=title).__dict__, categories=[category])
            if i == 0:
                resource_id = resource.id
                category_name = resource.categories[0].name
            resources.append(resource)

        num_studies = 24
        studies = []
        for i in range(num_studies):
            category = categories[i % 3]
            title = f"{category.name} {fake.sentence()}"
            studies.append(self.construct_study(**MockStudy(title=title).__dict__, categories=[category]))

        rv = self.client.post(
            "/api/related", data=self.jsonify({"resource_id": resource_id}), content_type="application/json"
        )
        self.assert_success(rv)
        response = rv.json
        self.assertTrue("resources" in response.keys())
        self.assertGreater(len(response["resources"]), 0)

        self.assertTrue("studies" in response.keys())
        self.assertGreater(len(response["studies"]), 0)

        # Most relevant result should also have category name in title
        for r in response["resources"]:
            self.assertIn(category_name, r["title"])
            self.assertEqual(category_name, r["resource_categories"][0]["category"]["name"])

        for s in response["studies"]:
            self.assertIn(category_name, s["title"])
            self.assertEqual(category_name, s["study_categories"][0]["category"]["name"])

    def test_search_paginates(self):
        self.construct_location(title="one")
        self.construct_location(title="two")
        self.construct_location(title="three")

        query = {"start": 0, "size": 1}
        search_results = self.search(query)
        self.assertEqual(1, len(search_results["hits"]))
        title1 = search_results["hits"][0]["title"]

        query = {"start": 1, "size": 1}
        search_results = self.search(query)
        self.assertEqual(1, len(search_results["hits"]))
        title2 = search_results["hits"][0]["title"]

        query = {"start": 2, "size": 1}
        search_results = self.search(query)
        self.assertEqual(1, len(search_results["hits"]))
        title3 = search_results["hits"][0]["title"]

        self.assertNotEqual(title1, title2)
        self.assertNotEqual(title2, title3)

    def test_search_sort_by_date_filters_out_past_events(self):
        now = datetime.utcnow()
        last_year = self.construct_event(title="A year ago", date=now + timedelta(days=-365))
        last_week = self.construct_event(title="A week ago", date=now + timedelta(days=-7))
        yesterday = self.construct_event(title="Yesterday", date=now + timedelta(days=-1))

        # Events earlier in the day are included. They aren't excluded until the local time is past midnight.
        earlier_today = self.construct_event(title="Earlier today", date=now - timedelta(hours=1))
        later_today = self.construct_event(title="Later today", date=now + timedelta(hours=1))
        tomorrow = self.construct_event(title="Tomorrow", date=now + timedelta(days=1))
        next_week = self.construct_event(title="Next week", date=now + timedelta(days=7))
        next_year = self.construct_event(title="Next year", date=now + timedelta(days=365))

        query = {"date": now, "sort": {"field": "date", "order": "asc"}}
        search_results = self.search(query)
        self.assertEqual(5, len(search_results["hits"]))
        self.assertEqual(search_results["hits"][0]["title"], earlier_today.title)
        self.assertEqual(search_results["hits"][1]["title"], later_today.title)
        self.assertEqual(search_results["hits"][2]["title"], tomorrow.title)
        self.assertEqual(search_results["hits"][3]["title"], next_week.title)
        self.assertEqual(search_results["hits"][4]["title"], next_year.title)

    def test_search_filters_out_past_events(self):
        now = datetime.utcnow()
        self.construct_resource(title="How to style unicorn hair")
        self.construct_resource(title="Rainbow-emitting capabilities of unicorn horns")
        self.construct_resource(title="Tips for time travel with a unicorn")
        self.construct_event(
            title="Unicorn council last year",
            date=now + timedelta(days=-365),
            description="Upcoming unicorn council",
            post_event_description="Previously recorded unicorn council",
        )
        self.construct_event(title="Unicorn meetup a week ago", date=now + timedelta(days=-7))
        self.construct_event(title="Unicorn workshop yesterday", date=now + timedelta(days=-1))
        self.construct_event(title="Unicorn playdate tomorrow", date=now + timedelta(days=1))
        self.construct_event(title="Unicorn training next week", date=now + timedelta(days=7))
        self.construct_event(title="Unicorn conference next year", date=now + timedelta(days=365))

        # Should return future events, plus past events that have a post_event_description
        query = {"words": "unicorn"}
        search_results = self.search(query)
        self.assertEqual(7, len(search_results["hits"]))
        for hit in search_results["hits"]:
            if hit["type"] == "event":
                hit_date = dateutil.parser.parse(hit["date"])
                if hit_date >= now:
                    self.assertGreaterEqual(hit_date, now)
                else:
                    self.assertTrue("post_event_description" in hit, "Hit has no post-event description.")
                    self.assertIsNotNone(hit["post_event_description"], "Post-event description is empty.")
            else:
                self.assertTrue(hit["date"] is None)

        # Should only return future events when filtering by event type
        event_query = {"words": "unicorn", "types": ["event"]}
        event_search_results = self.search(event_query)
        self.assertEqual(3, len(event_search_results["hits"]))
        for hit in event_search_results["hits"]:
            self.assertEqual(hit["type"], "event")
            hit_date = dateutil.parser.parse(hit["date"])
            self.assertGreaterEqual(hit_date, now)

    def test_search_for_map_points_only(self):

        # Add some locations with coordinates, and some with out.
        location_near = self.construct_location(
            title="local unicorn",
            description="delivering rainbows within the orbit of Uranus",
            latitude=38.149595,
            longitude=-79.072557,
        )
        location_far = self.construct_location(
            title="distant unicorn",
            description="delivering rainbows to the greater Trans-Neptunian Region",
            latitude=-38.149595,
            longitude=100.927443,
        )
        location_mid = self.construct_location(
            title="middle unicorn",
            description="delivering rainbows somewhere in between",
            latitude=37.5246403,
            longitude=-77.5633015,
        )
        self.construct_resource(title="Rainbow with a bad hair day and no place to be.")
        self.construct_resource(title="A non-rainbow blue sky that covers nearly all locations.")
        self.construct_resource(title="A very very tiny rainbow in a sprinkler, that occurs in various places.")

        query = {"words": "rainbows"}
        search_results = self.search(query)
        self.assertEqual(6, len(search_results["hits"]))

        query = {"words": "rainbows", "map_data_only": True}
        search_results = self.search(query)
        self.assertEqual(3, len(search_results["hits"]))
        self.assertTrue("latitude" in search_results["hits"][0])
        self.assertTrue("longitude" in search_results["hits"][0])
        self.assertFalse("content" in search_results["hits"][0])
        self.assertFalse("description" in search_results["hits"][0])
        self.assertFalse("highlights" in search_results["hits"][0])

    def test_study_search_record_updates(self):
        from fixtures.fixure_utils import fake

        keyword = fake.word()
        kw_query = {"words": keyword}

        # test that elastic resource is created with post
        study = MockStudy(
            description=f"{fake.sentence()} {keyword} {fake.sentence()}", status=Status.currently_enrolling.name
        )
        rv = self.client.post(
            "api/study", data=self.jsonify(study), content_type="application/json", follow_redirects=True
        )
        self.assert_success(rv)
        response = rv.json
        s_id = response["id"]

        search_results = self.search(kw_query)
        self.assertEqual(1, len(search_results["hits"]))
        self.assertEqual(search_results["hits"][0]["id"], s_id)
        self.assertEqual(search_results["hits"][0]["status"], Status.currently_enrolling.value)

        response["status"] = Status.study_in_progress.name
        rv = self.client.put(
            "/api/study/%i" % s_id, data=self.jsonify(response), content_type="application/json", follow_redirects=True
        )
        self.assert_success(rv)
        rv = self.client.get("/api/study/%i" % s_id, content_type="application/json")
        self.assert_success(rv)

        search_results = self.search(kw_query)
        self.assertEqual(1, len(search_results["hits"]))
        self.assertEqual(search_results["hits"][0]["id"], s_id)
        self.assertEqual(search_results["hits"][0]["status"], Status.study_in_progress.value)

    def test_search_with_drafts(self):
        resource_query = {"words": "resource"}
        password = "Silly password 305 for all the pretend users"

        self.construct_resource(title="Drafty Draft Draft Resource", is_draft=True)
        self.construct_resource(title="Published Resource", is_draft=False)
        self.construct_resource(title="Officially Published Resource", is_draft=False)
        self.construct_resource(title="A Draft Resource for the ages", is_draft=True)
        admin = self.construct_user(email="admin@sartography.com", role=Role.admin)
        editor = self.construct_user(email="editor@sartography.com", role=Role.editor)
        researcher = self.construct_user(email="researcher@sartography.com", role=Role.researcher)
        user = self.construct_user(email="user@sartography.com", role=Role.user)

        self.login_user(admin, password)
        search_results = self.search(resource_query, user=admin)
        self.assertEqual(4, len(search_results["hits"]))
        self.login_user(editor, password)
        search_results = self.search(resource_query, user=editor)
        self.assertEqual(4, len(search_results["hits"]))
        self.login_user(researcher, password)
        search_results = self.search(resource_query, user=researcher)
        self.assertEqual(2, len(search_results["hits"]))
        self.login_user(user, password)
        search_results = self.search(resource_query, user=user)
        self.assertEqual(2, len(search_results["hits"]))

    def login_user(self, user, password):
        user.email_verified = True
        user.password = password
        self.session.add(user)
        self.session.commit()

        data = {"email": user.email, "password": password}
        rv = self.client.post("/api/login_password", data=self.jsonify(data), content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertIsNotNone(response["token"])
