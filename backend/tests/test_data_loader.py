from typing import Callable

import math
from datetime import datetime
from unittest.mock import patch

from app.elastic_index import elastic_index
from app.models import (
    Category,
    ChainStep,
    Resource,
    ResourceCategory,
    Location,
    Event,
    Participant,
    Search,
    Study,
    StudyCategory,
    User,
    ZipCode,
)
from app.models import ResourceCategory
from app.models import StudyCategory
from app.models import User
from app.models import ZipCode
from tests.base_test import BaseTest
from utils import MockGoogleMapsClient


class TestDataLoader(BaseTest):
    def _load_and_assert_success(self, class_to_load, load_method=Callable, category_class=None, category_type=""):
        num_rc_after = -math.inf
        num_rc_before = math.inf

        if category_class is not None:
            num_rc_before = self._count(category_class, category_type)

        num_before = self._count(class_to_load)
        load_method()
        num_after = self._count(class_to_load)
        self.assertGreater(num_after, num_before)

        if category_class is not None:
            num_rc_after = self._count(category_class, category_type)
            self.assertGreater(num_rc_after, num_rc_before)

    def _count(self, class_to_query, type_to_filter=""):
        if type_to_filter != "":
            return self.session.query(class_to_query).filter(class_to_query.type == type_to_filter).count()
        else:
            return self.session.query(class_to_query).count()

    def test_load_categories(self):
        self._load_and_assert_success(Category, self.loader.load_categories)

    @patch("googlemaps.Client", return_value=MockGoogleMapsClient(), autospec=True)
    def test_load_events(self, mock_gmaps_client):
        self.test_load_categories()
        self.test_load_users()
        self._load_and_assert_success(Event, self.loader.load_events, ResourceCategory, "event")

    @patch("googlemaps.Client", return_value=MockGoogleMapsClient(), autospec=True)
    def test_load_locations(self, mock_gmaps_client):
        self.test_load_categories()
        self._load_and_assert_success(Location, self.loader.load_locations, ResourceCategory, "location")

    def test_load_resources(self):
        self.test_load_categories()
        self._load_and_assert_success(Resource, self.loader.load_resources, ResourceCategory, "resource")

    def test_load_studies(self):
        self.test_load_categories()
        self._load_and_assert_success(Study, self.loader.load_studies, StudyCategory)

    def test_load_users(self):
        self._load_and_assert_success(User, self.loader.load_users)

    # Participants depends on Users
    def test_load_participants(self):
        self._load_and_assert_success(User, self.loader.load_users)
        self._load_and_assert_success(Participant, self.loader.load_participants)

    def test_load_zip_codes(self):
        self._load_and_assert_success(ZipCode, self.loader.load_zip_codes)

    def test_load_chain_steps(self):
        self._load_and_assert_success(ChainStep, self.loader.load_chain_steps)

    def test_get_category_by_name(self):
        expected_name = "Schools of Witchcraft and Wizardry"
        cat = self.loader.get_category_by_name(expected_name, create_missing=True)
        self.assertIsNotNone(cat)
        self.assertEqual(cat.name, expected_name)

    @patch("googlemaps.Client", return_value=MockGoogleMapsClient(), autospec=True)
    def test_build_index(self, mock_gmaps_client):
        elastic_index.clear()

        # Populate the database
        self._load_and_assert_success(User, self.loader.load_users)
        self._load_and_assert_success(Category, self.loader.load_categories)
        self._load_and_assert_success(Resource, self.loader.load_resources, ResourceCategory, "resource")
        self._load_and_assert_success(Event, self.loader.load_events, ResourceCategory, "event")
        self._load_and_assert_success(Location, self.loader.load_locations, ResourceCategory, "location")
        self._load_and_assert_success(Study, self.loader.load_studies, StudyCategory)

        # Build the index
        self.loader.build_index()

        # Get the number of items in the database
        num_db_resources = self.session.query(Resource).filter(Resource.type == "resource").count()
        num_db_events = self.session.query(Event).filter(Event.date >= datetime.now()).count()
        num_db_locations = self.session.query(Resource).filter(Resource.type == "location").count()
        num_db_studies = self.session.query(Study).count()

        # Get the number of items in the search index
        es_resources = elastic_index.search(Search(types=[Resource.__tablename__]))
        es_events = elastic_index.search(Search(types=[Event.__tablename__]))
        es_locations = elastic_index.search(Search(types=[Location.__tablename__]))
        es_studies = elastic_index.search(Search(types=[Study.__tablename__]))

        # Verify that the number of items in the database match the number of items in the search index
        self.assertEqual(num_db_resources, es_resources.hits.total["value"])
        self.assertEqual(num_db_events, es_events.hits.total["value"])
        self.assertEqual(num_db_locations, es_locations.hits.total["value"])
        self.assertEqual(num_db_studies, es_studies.hits.total["value"])

        # Assure there are not age related categories.
        self.assertEqual(0, self.session.query(Category).filter(Category.name == "Age Range").count())
        self.assertEqual(0, self.session.query(Category).filter(Category.name == "Pre-K (0 - 5 years)").count())
