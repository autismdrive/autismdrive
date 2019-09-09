import math
import unittest

from app import db, data_loader, elastic_index
from app.model.category import Category
from app.model.event import Event
from app.model.location import Location
from app.model.participant import Participant
from app.model.resource import Resource
from app.model.resource_category import ResourceCategory
from app.model.search import Search, Filter
from app.model.study import Study
from app.model.study_category import StudyCategory
from app.model.user import User
from app.model.zip_code import ZipCode
from tests.base_test import BaseTest, clean_db


class TestDataLoader(BaseTest, unittest.TestCase):

    def setUp(self):
        self.ctx.push()
        clean_db(db)
        elastic_index.clear()
        self.auths = {}

    def _load_and_assert_success(self, class_to_load, load_method='', category_class=None, category_type=''):
        num_rc_after = -math.inf
        num_rc_before = math.inf

        if category_class is not None:
            num_rc_before = self._count(category_class, category_type)

        num_before = self._count(class_to_load)
        data_loader.DataLoader().__getattribute__(load_method)()
        num_after = self._count(class_to_load)
        self.assertGreater(num_after, num_before)

        if category_class is not None:
            num_rc_after = self._count(category_class, category_type)
            self.assertGreater(num_rc_after, num_rc_before)

    def _count(self, class_to_query, type_to_filter=''):
        if type_to_filter is not '':
            return db.session.query(class_to_query).filter(class_to_query.type == type_to_filter).count()
        else:
            return db.session.query(class_to_query).count()

    def test_load_categories(self):
        self._load_and_assert_success(Category, 'load_categories')

    def test_load_events(self):
        self._load_and_assert_success(Event, 'load_events', ResourceCategory, 'event')

    def test_load_locations(self):
        self._load_and_assert_success(Location, 'load_locations', ResourceCategory, 'location')

    def test_load_resources(self):
        self._load_and_assert_success(Resource, 'load_resources', ResourceCategory, 'resource')

    def test_load_studies(self):
        self._load_and_assert_success(Study, 'load_studies', StudyCategory)

    def test_load_users(self):
        self._load_and_assert_success(User, 'load_users')

    # Participants depends on Users
    def test_load_participants(self):
        self._load_and_assert_success(User, 'load_users')
        self._load_and_assert_success(Participant, 'load_participants')

    def test_load_zip_codes(self):
        self._load_and_assert_success(ZipCode, 'load_zip_codes')

    def test_get_org_by_name(self):
        expected_name = 'The Graham Institute for Magical Misfits'
        loader = data_loader.DataLoader()
        org = loader.get_org_by_name(expected_name)
        self.assertIsNotNone(org)
        self.assertEqual(org.name, expected_name)

    def test_get_category_by_name(self):
        expected_name = 'Schools of Witchcraft and Wizardry'
        loader = data_loader.DataLoader()
        cat = loader.get_category_by_name(expected_name)
        self.assertIsNotNone(cat)
        self.assertEqual(cat.name, expected_name)

    def test_build_index(self):
        elastic_index.clear()

        # Populate the database
        self._load_and_assert_success(Resource, 'load_resources', ResourceCategory, 'resource')
        self._load_and_assert_success(Event, 'load_events', ResourceCategory, 'event')
        self._load_and_assert_success(Location, 'load_locations', ResourceCategory, 'location')
        self._load_and_assert_success(Study, 'load_studies', StudyCategory)

        # Build the index
        data_loader.DataLoader().build_index()

        # Get the number of items in the database
        num_db_resources = db.session.query(Resource).filter(Resource.type == 'resource').count()
        num_db_events = db.session.query(Resource).filter(Resource.type == 'event').count()
        num_db_locations = db.session.query(Resource).filter(Resource.type == 'location').count()
        num_db_studies = db.session.query(Study).count()

        # Get the number of items in the search index
        es_resources = elastic_index.search(Search(filters=[Filter('type', [Resource.__tablename__])]))
        es_events = elastic_index.search(Search(filters=[Filter('type', [Event.__tablename__])]))
        es_locations = elastic_index.search(Search(filters=[Filter('type', [Location.__tablename__])]))
        es_studies = elastic_index.search(Search(filters=[Filter('type', [Study.__tablename__])]))

        # Verify that the number of items in the database match the number of items in the search index
        self.assertEqual(num_db_resources, es_resources.hits.total)
        self.assertEqual(num_db_events, es_events.hits.total)
        self.assertEqual(num_db_locations, es_locations.hits.total)
        self.assertEqual(num_db_studies, es_studies.hits.total)
