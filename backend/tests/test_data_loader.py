import math
import unittest

from app import db, data_loader, elastic_index
from app.model.category import Category
from app.model.event import Event
from app.model.location import Location
from app.model.participant import Participant
from app.model.questionnaires.alternative_augmentative import AlternativeAugmentative
from app.model.questionnaires.assistive_device import AssistiveDevice
from app.model.questionnaires.clinical_diagnoses_questionnaire import ClinicalDiagnosesQuestionnaire
from app.model.questionnaires.contact_questionnaire import ContactQuestionnaire
from app.model.questionnaires.current_behaviors_dependent_questionnaire import CurrentBehaviorsDependentQuestionnaire
from app.model.questionnaires.current_behaviors_self_questionnaire import CurrentBehaviorsSelfQuestionnaire
from app.model.questionnaires.demographics_questionnaire import DemographicsQuestionnaire
from app.model.questionnaires.developmental_questionnaire import DevelopmentalQuestionnaire
from app.model.questionnaires.education_dependent_questionnaire import EducationDependentQuestionnaire
from app.model.questionnaires.education_self_questionnaire import EducationSelfQuestionnaire
from app.model.questionnaires.employment_questionnaire import EmploymentQuestionnaire
from app.model.questionnaires.evaluation_history_dependent_questionnaire import EvaluationHistoryDependentQuestionnaire
from app.model.questionnaires.evaluation_history_self_questionnaire import EvaluationHistorySelfQuestionnaire
from app.model.questionnaires.home_dependent_questionnaire import HomeDependentQuestionnaire
from app.model.questionnaires.home_self_questionnaire import HomeSelfQuestionnaire
from app.model.questionnaires.housemate import Housemate
from app.model.questionnaires.identification_questionnaire import IdentificationQuestionnaire
from app.model.questionnaires.medication import Medication
from app.model.questionnaires.professional_profile_questionnaire import ProfessionalProfileQuestionnaire
from app.model.questionnaires.supports_questionnaire import SupportsQuestionnaire
from app.model.questionnaires.therapy import Therapy
from app.model.resource import StarResource
from app.model.resource_category import ResourceCategory
from app.model.search import Search, Filter
from app.model.study import Study
from app.model.study_category import StudyCategory
from app.model.user import User
from tests.base_test import BaseTest


class TestDataLoader(BaseTest, unittest.TestCase):

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
        self._load_and_assert_success(StarResource, 'load_resources', ResourceCategory, 'resource')

    def test_load_studies(self):
        self._load_and_assert_success(Study, 'load_studies', StudyCategory)

    def test_load_users(self):
        self._load_and_assert_success(User, 'load_users')

    # Participants depends on Users
    def test_load_participants(self):
        self._load_and_assert_success(User, 'load_users')
        self._load_and_assert_success(Participant, 'load_participants')

    def test_load_clinical_diagnoses_questionnaire(self):
        self._load_and_assert_success(ClinicalDiagnosesQuestionnaire, 'load_clinical_diagnoses_questionnaire')

    def test_load_contact_questionnaire(self):
        self._load_and_assert_success(ContactQuestionnaire, 'load_contact_questionnaire')

    def test_load_current_behaviors_questionnaires(self):
        self._load_and_assert_success(CurrentBehaviorsDependentQuestionnaire, 'load_current_behaviors_questionnaires',
                                      CurrentBehaviorsSelfQuestionnaire)

    # DemographicsQuestionnaire depends on Users
    def test_load_demographics_questionnaire(self):
        self._load_and_assert_success(User, 'load_users')
        self._load_and_assert_success(DemographicsQuestionnaire, 'load_demographics_questionnaire')

    def test_load_developmental_questionnaire(self):
        self._load_and_assert_success(DevelopmentalQuestionnaire, 'load_developmental_questionnaire')

    def test_load_education_questionnaires(self):
        self._load_and_assert_success(EducationDependentQuestionnaire, 'load_education_questionnaires',
                                      EducationSelfQuestionnaire)

    def test_load_employment_questionnaire(self):
        self._load_and_assert_success(EmploymentQuestionnaire, 'load_employment_questionnaire')

    def test_load_evaluation_history_questionnaires(self):
        self._load_and_assert_success(EvaluationHistoryDependentQuestionnaire, 'load_evaluation_history_questionnaires',
                                      EvaluationHistorySelfQuestionnaire)

    def test_load_home_questionnaires(self):
        self._load_and_assert_success(HomeDependentQuestionnaire, 'load_home_questionnaires', HomeSelfQuestionnaire)

    def test_load_identification_questionnaire(self):
        self._load_and_assert_success(IdentificationQuestionnaire, 'load_identification_questionnaire')

    def test_load_professional_profile_questionnaire(self):
        self._load_and_assert_success(ProfessionalProfileQuestionnaire, 'load_professional_profile_questionnaire')

    def test_load_supports_questionnaire(self):
        self._load_and_assert_success(SupportsQuestionnaire, 'load_supports_questionnaire')

    def test_load_alternative_augmentative(self):
        self._load_and_assert_success(AlternativeAugmentative, 'load_alternative_augmentative')

    def test_load_assistive_devices(self):
        self._load_and_assert_success(AssistiveDevice, 'load_assistive_devices')

    def test_load_housemate(self):
        self._load_and_assert_success(Housemate, 'load_housemate')

    def test_load_medication(self):
        self._load_and_assert_success(Medication, 'load_medication')

    def test_load_therapy(self):
        self._load_and_assert_success(Therapy, 'load_therapy')

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
        self._load_and_assert_success(StarResource, 'load_resources', ResourceCategory, 'resource')
        self._load_and_assert_success(Event, 'load_events', ResourceCategory, 'event')
        self._load_and_assert_success(Location, 'load_locations', ResourceCategory, 'location')
        self._load_and_assert_success(Study, 'load_studies', StudyCategory)

        # Build the index
        data_loader.DataLoader().build_index()

        # Get the number of items in the database
        num_db_resources = db.session.query(StarResource).filter(StarResource.type == 'resource').count()
        num_db_events = db.session.query(StarResource).filter(StarResource.type == 'event').count()
        num_db_locations = db.session.query(StarResource).filter(StarResource.type == 'location').count()
        num_db_studies = db.session.query(Study).count()

        # Get the number of items in the search index
        es_resources = elastic_index.search(Search(filters=[Filter('Type', StarResource.__label__)]))
        es_events = elastic_index.search(Search(filters=[Filter('Type', Event.__label__)]))
        es_locations = elastic_index.search(Search(filters=[Filter('Type', Location.__label__)]))
        es_studies = elastic_index.search(Search(filters=[Filter('Type', Study.__label__)]))

        # Verify that the number of items in the database match the number of items in the search index
        self.assertEqual(num_db_resources, es_resources.hits.total)
        self.assertEqual(num_db_events, es_events.hits.total)
        self.assertEqual(num_db_locations, es_locations.hits.total)
        self.assertEqual(num_db_studies, es_studies.hits.total)
