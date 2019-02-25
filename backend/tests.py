# Set environment variable to testing before loading.
# IMPORTANT - Environment must be loaded before app, models, etc....
import os

os.environ["APP_CONFIG_FILE"] = '../config/testing.py'

from app.model.flow import Step
from app.model.step_log import StepLog
from app.question_service import QuestionService
import re
import json
import base64
import quopri
import random
import string
import datetime
import unittest
from app import db, app
from app.model.user import User, Role
from app.model.study import Study
from app.email_service import TEST_MESSAGES
from app.model.category import Category
from app.model.resource import StarResource
from app.model.training import Training
from app.model.email_log import EmailLog
from app.model.organization import Organization
from app.model.participant import Participant, Relationship
from app.model.study_category import StudyCategory
from app.model.resource_category import ResourceCategory
from app.model.training_category import TrainingCategory
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
from app.model.questionnaires.supports_questionnaire import SupportsQuestionnaire
from app.model.questionnaires.therapy import Therapy


class TestCase(unittest.TestCase):

    def setUp(self):
        self.ctx = app.test_request_context()
        self.app = app.test_client()
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.ctx.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # elastic_index.clear()
        self.ctx.pop()

    def assertSuccess(self, rv):
        try:
            data = json.loads(rv.get_data(as_text=True))
            self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                            "BAD Response: %i. \n %s" %
                            (rv.status_code, json.dumps(data)))
        except:
            self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                            "BAD Response: %i." % rv.status_code)

    def randomString(self):
        char_set = string.ascii_uppercase + string.digits
        return ''.join(random.sample(char_set * 6, 6))

    def test_base_endpoint(self):
        rv = self.app.get('/',
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))

        endpoints = [
            ('api.categorybyresourceendpoint', '/api/resource/<resource_id>/category'),
            ('api.categorybystudyendpoint', '/api/study/<study_id>/category'),
            ('api.categorybytrainingendpoint', '/api/training/<training_id>/category'),
            ('api.categoryendpoint', '/api/category/<id>'),
            ('api.categorylistendpoint', '/api/category'),
            ('api.questionnaireendpoint', '/api/q/<name>/<id>'),
            ('api.organizationendpoint', '/api/organization/<id>'),
            ('api.organizationlistendpoint', '/api/organization'),
            ('api.resourcebycategoryendpoint', '/api/category/<category_id>/resource'),
            ('api.resourcecategoryendpoint', '/api/resource_category/<id>'),
            ('api.resourcecategorylistendpoint', '/api/resource_category'),
            ('api.resourceendpoint', '/api/resource/<id>'),
            ('api.resourcelistendpoint', '/api/resource'),
            ('api.rootcategorylistendpoint', '/api/category/root'),
            ('api.sessionendpoint', '/api/session'),
            ('api.studybycategoryendpoint', '/api/category/<category_id>/study'),
            ('api.studycategoryendpoint', '/api/study_category/<id>'),
            ('api.studycategorylistendpoint', '/api/study_category'),
            ('api.studyendpoint', '/api/study/<id>'),
            ('api.studylistendpoint', '/api/study'),
            ('api.trainingbycategoryendpoint', '/api/category/<category_id>/training'),
            ('api.trainingcategoryendpoint', '/api/training_category/<id>'),
            ('api.trainingcategorylistendpoint', '/api/training_category'),
            ('api.trainingendpoint', '/api/training/<id>'),
            ('api.traininglistendpoint', '/api/training'),
            ('api.userendpoint', '/api/user/<id>'),
            ('api.userlistendpoint', '/api/user'),
            ('auth.forgot_password', '/api/forgot_password'),
            ('auth.login_password', '/api/login_password'),
            ('auth.reset_password', '/api/reset_password'),
        ]

        for endpoint in endpoints:
            self.assertEqual(response[endpoint[0]], endpoint[1])

    def construct_resource(self, title="A+ Resource", description="A delightful Resource destined to create rejoicing",
                           image_url="assets/image.svg", image_caption="An inspiring photograph of great renown",
                           street_address1="123 Some Pl", street_address2="Apt. 45",
                           city="Stauntonville", state="QX", zip="99775", county="Augustamarle", phone="555-555-5555",
                           website="http://stardrive.org"):

        resource = StarResource(title=title, description=description, image_url=image_url, image_caption=image_caption,
                                street_address1=street_address1, street_address2=street_address2, city=city,
                                state=state, zip=zip, county=county, phone=phone, website=website)
        resource.organization_id = self.construct_organization().id
        db.session.add(resource)
        db.session.commit()

        db_resource = db.session.query(StarResource).filter_by(title=resource.title).first()
        self.assertEqual(db_resource.website, resource.website)
        return db_resource

    def construct_study(self, title="Fantastic Study", description="A study that will go down in history",
                        researcher_description="Fantastic people work on this fantastic study. You should be impressed",
                        participant_description="Even your pet hamster could benefit from participating in this study",
                        outcomes_description="You can expect to have your own rainbow following you around after participating",
                        enrollment_start_date=datetime.date(2019, 1, 20), current_num_participants="54", max_num_participants="5000",
                        start_date=datetime.date(2019, 2, 1), end_date=datetime.date(2019, 3, 31)):

        study = Study(title=title, description=description, researcher_description=researcher_description,
                      participant_description=participant_description, outcomes_description=outcomes_description,
                      enrollment_start_date=enrollment_start_date, current_num_participants=current_num_participants,
                      max_num_participants=max_num_participants, start_date=start_date, end_date=end_date)
        study.organization_id = self.construct_organization().id
        db.session.add(study)
        db.session.commit()

        db_study = db.session.query(Study).filter_by(title=study.title).first()
        self.assertEqual(db_study.description, study.description)
        return db_study

    def construct_training(self, title="Best Training", description="A training to end all trainings",
                           outcomes_description="Increased intelligence and the ability to do magic tricks.",
                           image_url="assets/image.png", image_caption="One of the magic tricks you will learn"):

        training = Training(title=title, description=description, outcomes_description=outcomes_description, image_url=image_url,
                            image_caption=image_caption)
        training.organization_id = self.construct_organization().id
        db.session.add(training)
        db.session.commit()

        db_training = db.session.query(Training).filter_by(title=training.title).first()
        self.assertEqual(db_training.outcomes_description, training.outcomes_description)
        return db_training

    def construct_organization(self, name="Staunton Makerspace", description="A place full of surprise, delight, and amazing people. And tools. Lots of exciting tools."):

        organization = Organization(name=name, description=description)
        db.session.add(organization)
        db.session.commit()

        db_org = db.session.query(Organization).filter_by(name=organization.name).first()
        self.assertEqual(db_org.description, organization.description)
        return db_org

    def construct_category(self, name="Ultimakers", parent=None):

        category = Category(name=name)
        if parent is not None:
            category.parent = parent
        db.session.add(category)
        db.session.commit()

        db_category = db.session.query(Category).filter_by(name=category.name).first()
        self.assertIsNotNone(db_category.id)
        return db_category

    def construct_user(self, email="stan@staunton.com"):

        user = User(email=email, role=Role.user)
        db.session.add(user)
        db.session.commit()

        db_user = db.session.query(User).filter_by(email=user.email).first()
        self.assertEqual(db_user.email, user.email)
        return db_user

    def construct_admin_user(self, email="rmond@virginia.gov"):

        user = User(email=email, role=Role.admin)
        db.session.add(user)
        db.session.commit()

        db_user = db.session.query(User).filter_by(email=user.email).first()
        self.assertEqual(db_user.role, user.role)
        return db_user

    def construct_participant(self, user, relationship):

        participant = Participant(user=user, relationship=relationship)
        db.session.add(participant)
        db.session.commit()

        db_participant = db.session.query(Participant).filter_by(id=participant.id).first()
        self.assertEqual(db_participant.relationship, participant.relationship)
        return db_participant

    def construct_assistive_device(self, type='prosthetic', description='leg', timeframe='current',
                                   notes='I love my new leg!', supports_questionnaire=None):

        ad = AssistiveDevice(type=type, description=description, timeframe=timeframe, notes=notes)
        if supports_questionnaire is not None:
            ad.supports_questionnaire_id = supports_questionnaire.id

        db.session.add(ad)
        db.session.commit()

        db_ad = db.session.query(AssistiveDevice).filter_by(last_updated=ad.last_updated).first()
        self.assertEqual(db_ad.description, ad.description)
        return db_ad

    def construct_clinical_diagnoses_questionnaire(self, developmental='speechLanguage', mental_health='ocd',
                                                   medical='insomnia', genetic='corneliaDeLange', participant=None,
                                                   user=None):

        cdq = ClinicalDiagnosesQuestionnaire(developmental=developmental, mental_health=mental_health, medical=medical,
                                             genetic=genetic)
        if user is None:
            u = self.construct_user()
            cdq.user_id = u.id
        else:
            u = user
            cdq.user_id = u.id

        if participant is None:
            cdq.participant_id = self.construct_participant(user=u, relationship=Relationship.dependent).id
        else:
            cdq.participant_id = participant.id

        db.session.add(cdq)
        db.session.commit()

        db_cdq = db.session.query(ClinicalDiagnosesQuestionnaire).filter_by(user_id=cdq.user_id).first()
        self.assertEqual(db_cdq.participant_id, cdq.participant_id)
        return db_cdq

    def construct_contact_questionnaire(self, phone="123-456-7890", zip=55678, marketing_channel="Zine Ad",
                                        participant=None, user=None):

        cq = ContactQuestionnaire(phone=phone, zip=zip,
                                  marketing_channel=marketing_channel)
        if user is None:
            u = self.construct_user()
            cq.user_id = u.id
        else:
            u = user
            cq.user_id = u.id

        if participant is None:
            cq.participant_id = self.construct_participant(user=u, relationship=Relationship.dependent).id
        else:
            cq.participant_id = participant.id

        db.session.add(cq)
        db.session.commit()

        db_cq = db.session.query(ContactQuestionnaire).filter_by(zip=cq.zip).first()
        self.assertEqual(db_cq.phone, cq.phone)
        return db_cq

    def construct_current_behaviors_dependent_questionnaire(self, dependent_verbal_ability='fluent',
                                                            concerning_behaviors='hoarding',
                                                            has_academic_difficulties=True,
                                                            academic_difficulty_areas='math',
                                                            participant=None, user=None):

        cb = CurrentBehaviorsDependentQuestionnaire(dependent_verbal_ability=dependent_verbal_ability,
                                                    concerning_behaviors=concerning_behaviors,
                                                    has_academic_difficulties=has_academic_difficulties,
                                                    academic_difficulty_areas=academic_difficulty_areas)
        if user is None:
            u = self.construct_user()
            cb.user_id = u.id
        else:
            u = user
            cb.user_id = u.id

        if participant is None:
            p = self.construct_participant(user=u, relationship=Relationship.dependent)
            cb.participant_id = p.id
        else:
            p = participant
            cb.participant_id = p.id

        db.session.add(cb)
        db.session.commit()

        db_cbd = db.session.query(CurrentBehaviorsDependentQuestionnaire).filter_by(participant_id=cb.participant_id).first()
        self.assertEqual(db_cbd.concerning_behaviors, cb.concerning_behaviors)
        return db_cbd

    def construct_current_behaviors_self_questionnaire(self, self_verbal_ability='verbal',
                                                       has_academic_difficulties=True, academic_difficulty_areas='math',
                                                       participant=None, user=None):

        cb = CurrentBehaviorsSelfQuestionnaire(self_verbal_ability=self_verbal_ability,
                                               has_academic_difficulties=has_academic_difficulties,
                                               academic_difficulty_areas=academic_difficulty_areas)
        if user is None:
            u = self.construct_user()
            cb.user_id = u.id
        else:
            u = user
            cb.user_id = u.id

        if participant is None:
            p = self.construct_participant(user=u, relationship=Relationship.self_participant)
            cb.participant_id = p.id
        else:
            p = participant
            cb.participant_id = p.id

        db.session.add(cb)
        db.session.commit()

        db_cb = db.session.query(CurrentBehaviorsSelfQuestionnaire).filter_by(participant_id=cb.participant_id).first()
        self.assertEqual(db_cb.academic_difficulty_areas, cb.academic_difficulty_areas)
        return db_cb

    def construct_demographics_questionnaire(self, birth_sex="intersex", gender_identity="intersex",
                                             race_ethnicity="raceBlack", participant=None, user=None):

        dq = DemographicsQuestionnaire(birth_sex=birth_sex, gender_identity=gender_identity,
                                       race_ethnicity=race_ethnicity)
        if user is None:
            u = self.construct_user(email="user@study.com")
            dq.user_id = u.id
        else:
            u = user
            dq.user_id = u.id

        if participant is None:
            dq.participant_id = self.construct_participant(user=u, relationship=Relationship.self_participant).id
        else:
            dq.participant_id = participant.id

        db.session.add(dq)
        db.session.commit()

        db_dq = db.session.query(DemographicsQuestionnaire).filter_by(birth_sex=dq.birth_sex).first()
        self.assertEqual(db_dq.gender_identity, dq.gender_identity)
        return db_dq

    def construct_developmental_questionnaire(self, had_birth_complications=False, when_motor_milestones='delayed',
                                              when_language_milestones='early', when_toileting_milestones='notYet', participant=None, user=None):

        dq = DevelopmentalQuestionnaire(had_birth_complications=had_birth_complications,
                                        when_motor_milestones=when_motor_milestones,
                                        when_language_milestones=when_language_milestones,
                                        when_toileting_milestones=when_toileting_milestones)
        if user is None:
            u = self.construct_user(email="user@study.com")
            dq.user_id = u.id
        else:
            u = user
            dq.user_id = u.id

        if participant is None:
            dq.participant_id = self.construct_participant(user=u, relationship=Relationship.dependent).id
        else:
            dq.participant_id = participant.id

        db.session.add(dq)
        db.session.commit()

        db_dq = db.session.query(DevelopmentalQuestionnaire).filter_by(participant_id=dq.participant_id).first()
        self.assertEqual(db_dq.when_language_milestones, dq.when_language_milestones)
        return db_dq

    def construct_education_dependent_questionnaire(self, attends_school=True, school_name='Harvard', school_type='privateSchool',
                                                    dependent_placement='graduate', participant=None, user=None):

        eq = EducationDependentQuestionnaire(attends_school=attends_school, school_name=school_name, school_type=school_type,
                                             dependent_placement=dependent_placement)
        if user is None:
            u = self.construct_user(email="user@study.com")
            eq.user_id = u.id
        else:
            u = user
            eq.user_id = u.id

        if participant is None:
            p = self.construct_participant(user=u, relationship=Relationship.dependent)
            eq.participant_id = p.id
        else:
            p = participant
            eq.participant_id = p.id

        db.session.add(eq)
        db.session.commit()

        db_eq = db.session.query(EducationDependentQuestionnaire).filter_by(participant_id=eq.participant_id).first()
        self.assertEqual(db_eq.school_name, eq.school_name)
        return db_eq

    def construct_education_self_questionnaire(self, attends_school=True, school_name='Harvard', school_type='privateSchool',
                                               self_placement='graduate', participant=None, user=None):

        eq = EducationSelfQuestionnaire(attends_school=attends_school, school_name=school_name, school_type=school_type,
                                        self_placement=self_placement)

        if user is None:
            u = self.construct_user(email="user@study.com")
            eq.user_id = u.id
        else:
            u = user
            eq.user_id = u.id

        if participant is None:
            p = self.construct_participant(user=u, relationship=Relationship.self_participant)
            eq.participant_id = p.id
        else:
            p = participant
            eq.participant_id = p.id

        db.session.add(eq)
        db.session.commit()

        db_eq = db.session.query(EducationSelfQuestionnaire).filter_by(participant_id=eq.participant_id).first()
        self.assertEqual(db_eq.school_name, eq.school_name)
        return db_eq

    def construct_employment_questionnaire(self, is_currently_employed=True, employment_capacity='fullTime',
                                           has_employment_support=False, participant=None, user=None):

        eq = EmploymentQuestionnaire(is_currently_employed=is_currently_employed,
                                     employment_capacity=employment_capacity,
                                     has_employment_support=has_employment_support)
        if user is None:
            u = self.construct_user(email="user@study.com")
            eq.user_id = u.id
        else:
            u = user
            eq.user_id = u.id

        if participant is None:
            eq.participant_id = self.construct_participant(user=u, relationship=Relationship.self_participant).id
        else:
            eq.participant_id = participant.id

        db.session.add(eq)
        db.session.commit()

        db_eq = db.session.query(EmploymentQuestionnaire).filter_by(participant_id=eq.participant_id).first()
        self.assertEqual(db_eq.employment_capacity, eq.employment_capacity)
        return db_eq

    def construct_evaluation_history_dependent_questionnaire(self, self_identifies_autistic=True, has_autism_diagnosis=True,
                                                             years_old_at_first_diagnosis=7, who_diagnosed="pediatrician",
                                                             participant=None, user=None):

        ehq = EvaluationHistoryDependentQuestionnaire(self_identifies_autistic=self_identifies_autistic,
                                                      has_autism_diagnosis=has_autism_diagnosis,
                                                      years_old_at_first_diagnosis=years_old_at_first_diagnosis,
                                                      who_diagnosed=who_diagnosed)
        if user is None:
            u = self.construct_user(email="user@study.com")
            ehq.user_id = u.id
        else:
            u = user
            ehq.user_id = u.id

        if participant is None:
            p = self.construct_participant(user=u, relationship=Relationship.dependent)
            ehq.participant_id = p.id
        else:
            p = participant
            ehq.participant_id = p.id

        db.session.add(ehq)
        db.session.commit()

        db_ehq = db.session.query(EvaluationHistoryDependentQuestionnaire).filter_by(participant_id=ehq.participant_id).first()
        self.assertEqual(db_ehq.who_diagnosed, ehq.who_diagnosed)
        return db_ehq

    def construct_evaluation_history_self_questionnaire(self, self_identifies_autistic=True, has_autism_diagnosis=True,
                                                        years_old_at_first_diagnosis=7, who_diagnosed="pediatrician",
                                                        participant=None, user=None):

        ehq = EvaluationHistorySelfQuestionnaire(self_identifies_autistic=self_identifies_autistic,
                                                 has_autism_diagnosis=has_autism_diagnosis,
                                                 years_old_at_first_diagnosis=years_old_at_first_diagnosis,
                                                 who_diagnosed=who_diagnosed)
        if user is None:
            u = self.construct_user(email="user@study.com")
            ehq.user_id = u.id
        else:
            u = user
            ehq.user_id = u.id

        if participant is None:
            p = self.construct_participant(user=u, relationship=Relationship.self_participant)
            ehq.participant_id = p.id
        else:
            p = participant
            ehq.participant_id = p.id

        db.session.add(ehq)
        db.session.commit()

        db_ehq = db.session.query(EvaluationHistorySelfQuestionnaire).filter_by(participant_id=ehq.participant_id).first()
        self.assertEqual(db_ehq.who_diagnosed, ehq.who_diagnosed)
        return db_ehq

    def construct_home_dependent_questionnaire(self, dependent_living_situation='fullTimeGuardian', housemates=None,
                                               struggle_to_afford=False, participant=None, user=None):

        hq = HomeDependentQuestionnaire(dependent_living_situation=dependent_living_situation, struggle_to_afford=struggle_to_afford)

        if user is None:
            u = self.construct_user(email="user@study.com")
            hq.user_id = u.id
        else:
            u = user
            hq.user_id = u.id

        if participant is None:
            p = self.construct_participant(user=u, relationship=Relationship.dependent)
            hq.participant_id = p.id
        else:
            p = participant
            hq.participant_id = p.id

        db.session.add(hq)
        db.session.commit()

        if housemates is None:
            self.construct_housemate(home_dependent_questionnaire=hq)
        else:
            hq.housemates = housemates

        db_hq = db.session.query(HomeDependentQuestionnaire).filter_by(participant_id=hq.participant_id).first()
        self.assertEqual(db_hq.dependent_living_situation, hq.dependent_living_situation)
        return db_hq

    def construct_home_self_questionnaire(self,self_living_situation='alone', housemates=None, struggle_to_afford=False,
                                          participant=None, user=None):

        hq = HomeSelfQuestionnaire(self_living_situation=self_living_situation, struggle_to_afford=struggle_to_afford)

        if user is None:
            u = self.construct_user(email="user@study.com")
            hq.user_id = u.id
        else:
            u = user
            hq.user_id = u.id

        if participant is None:
            p = self.construct_participant(user=u, relationship=Relationship.self_participant)
            hq.participant_id = p.id
        else:
            p = participant
            hq.participant_id = p.id

        db.session.add(hq)
        db.session.commit()

        if housemates is None:
            self.construct_housemate(home_self_questionnaire=hq)
        else:
            hq.housemates = housemates

        db_hq = db.session.query(HomeSelfQuestionnaire).filter_by(participant_id=hq.participant_id).first()
        self.assertEqual(db_hq.self_living_situation, hq.self_living_situation)
        return db_hq

    def construct_housemate(self, name="Fred Fredly", relationship='bioSibling', age=23, has_autism=True,
                            home_dependent_questionnaire=None, home_self_questionnaire=None):

        h = Housemate(name=name, relationship=relationship, age=age, has_autism=has_autism)
        if home_dependent_questionnaire is not None:
            h.home_dependent_questionnaire_id = home_dependent_questionnaire.id
        if home_self_questionnaire is not None:
            h.home_self_questionnaire_id = home_self_questionnaire.id

        db.session.add(h)
        db.session.commit()

        db_h = db.session.query(Housemate).filter_by(last_updated=h.last_updated).first()
        self.assertEqual(db_h.relationship, h.relationship)
        return db_h

    def construct_identification_questionnaire(self, relationship_to_participant='adoptFather', first_name='Karl',
                                               is_first_name_preferred=False, nickname='Big K', birth_state='VA',
                                               is_english_primary=False, participant=None, user=None):

        iq = IdentificationQuestionnaire(relationship_to_participant=relationship_to_participant, first_name=first_name,
                                         is_first_name_preferred=is_first_name_preferred, nickname=nickname,
                                         birth_state=birth_state, is_english_primary=is_english_primary)
        if user is None:
            u = self.construct_user(email="user@study.com")
            iq.user_id = u.id
        else:
            u = user
            iq.user_id = u.id

        if participant is None:
            iq.participant_id = self.construct_participant(user=u, relationship=Relationship.dependent).id
        else:
            iq.participant_id = participant.id

        db.session.add(iq)
        db.session.commit()

        db_iq = db.session.query(IdentificationQuestionnaire).filter_by(participant_id=iq.participant_id).first()
        self.assertEqual(db_iq.nickname, iq.nickname)
        return db_iq

    def construct_medication(self, name='Magic Potion', dosage='3 times daily', time_frame='current',
                             notes='I feel better than ever!', supports_questionnaire=None):

        m = Medication(name=name, dosage=dosage, time_frame=time_frame, notes=notes)
        if supports_questionnaire is not None:
            m.supports_questionnaire_id = supports_questionnaire.id

        db.session.add(m)
        db.session.commit()

        db_m = db.session.query(Medication).filter_by(last_updated=m.last_updated).first()
        self.assertEqual(db_m.dosage, m.dosage)
        return db_m

    def construct_therapy(self, type='behavioral', description='Discrete Trial Training', timeframe='current',
                          notes='Small steps', supports_questionnaire=None):

        t = Therapy(type=type, description=description, timeframe=timeframe, notes=notes)
        if supports_questionnaire is not None:
            t.supports_questionnaire_id = supports_questionnaire.id

        db.session.add(t)
        db.session.commit()

        db_t = db.session.query(Therapy).filter_by(last_updated=t.last_updated).first()
        self.assertEqual(db_t.description, t.description)
        return db_t

    def construct_supports_questionnaire(self, medications=None, therapies=None, assistive_devices=None, participant=None, user=None):

        sq = SupportsQuestionnaire()
        if user is None:
            u = self.construct_user(email="user@supports.org")
            sq.user_id = u.id
        else:
            u = user
            sq.user_id = u.id

        if participant is None:
            sq.participant_id = self.construct_participant(user=u, relationship=Relationship.dependent).id
        else:
            sq.participant_id = participant.id

        db.session.add(sq)
        db.session.commit()

        if assistive_devices is None:
            self.construct_assistive_device(supports_questionnaire=sq)
        else:
            sq.assistive_devices = assistive_devices

        if medications is None:
            self.construct_medication(supports_questionnaire=sq)
        else:
            sq.medications = medications

        if therapies is None:
            self.construct_therapy(supports_questionnaire=sq)
        else:
            sq.therapies = therapies

        db_sq = db.session.query(SupportsQuestionnaire).filter_by(participant_id=sq.participant_id).first()
        self.assertEqual(db_sq.last_updated, sq.last_updated)
        return db_sq

    def test_resource_basics(self):
        self.construct_resource()
        r = db.session.query(StarResource).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/resource/%i' % r_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], r_id)
        self.assertEqual(response["title"], 'A+ Resource')
        self.assertEqual(response["description"], 'A delightful Resource destined to create rejoicing')

    def test_modify_resource_basics(self):
        self.construct_resource()
        r = db.session.query(StarResource).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/resource/%i' % r_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        response['website'] = 'http://sartography.com'
        response['county'] = 'Rockingbridge'
        response['image_caption'] = 'Daniel GG Dog Da Funk-a-funka'
        orig_date = response['last_updated']
        rv = self.app.put('/api/resource/%i' % r_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/resource/%i' % r_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['website'], 'http://sartography.com')
        self.assertEqual(response['county'], 'Rockingbridge')
        self.assertEqual(response['image_caption'], 'Daniel GG Dog Da Funk-a-funka')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_resource(self):
        r = self.construct_resource()
        r_id = r.id
        rv = self.app.get('api/resource/%i' % r_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/resource/%i' % r_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/resource/%i' % r_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_resource(self):
        resource = {'title':"Resource of Resources", 'description':"You need this resource in your life."}
        rv = self.app.post('api/resource', data=json.dumps(resource), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Resource of Resources')
        self.assertEqual(response['description'], 'You need this resource in your life.')
        self.assertIsNotNone(response['id'])

    def test_study_basics(self):
        self.construct_study()
        s = db.session.query(Study).first()
        self.assertIsNotNone(s)
        s_id = s.id
        rv = self.app.get('/api/study/%i' % s_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], s_id)
        self.assertEqual(response["title"], 'Fantastic Study')
        self.assertEqual(response["description"], 'A study that will go down in history')

    def test_modify_study_basics(self):
        self.construct_study()
        s = db.session.query(Study).first()
        self.assertIsNotNone(s)
        s_id = s.id
        rv = self.app.get('/api/study/%i' % s_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        response['outcomes_description'] = 'Better fluids for you and your car, Duh.'
        response['max_num_participants'] = '2'
        orig_date = response['last_updated']
        rv = self.app.put('/api/study/%i' % s_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/study/%i' % s_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['outcomes_description'], 'Better fluids for you and your car, Duh.')
        self.assertEqual(response['max_num_participants'], 2)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_study(self):
        s = self.construct_study()
        s_id = s.id
        rv = self.app.get('api/study/%i' % s_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/study/%i' % s_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/study/%i' % s_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_study(self):
        study = {'title':"Study of Studies", 'outcomes_description':"This study will change your life."}
        rv = self.app.post('api/study', data=json.dumps(study), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Study of Studies')
        self.assertEqual(response['outcomes_description'], 'This study will change your life.')
        self.assertIsNotNone(response['id'])

    def test_training_basics(self):
        self.construct_training()
        t = db.session.query(Training).first()
        self.assertIsNotNone(t)
        t_id = t.id
        rv = self.app.get('/api/training/%i' % t_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], t_id)
        self.assertEqual(response["title"], 'Best Training')
        self.assertEqual(response["description"], 'A training to end all trainings')

    def test_modify_training_basics(self):
        self.construct_training()
        t = db.session.query(Training).first()
        self.assertIsNotNone(t)
        t_id = t.id
        rv = self.app.get('/api/training/%i' % t_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        response['outcomes_description'] = 'Better fluids for you and your car, Duh.'
        response['image_caption'] = 'A nice cool glass of lemonade'
        orig_date = response['last_updated']
        rv = self.app.put('/api/training/%i' % t_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/training/%i' % t_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['outcomes_description'], 'Better fluids for you and your car, Duh.')
        self.assertEqual(response['image_caption'], 'A nice cool glass of lemonade')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_training(self):
        t = self.construct_training()
        t_id = t.id
        rv = self.app.get('api/training/%i' % t_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/training/%i' % t_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/training/%i' % t_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_training(self):
        training = {'title':"Training of Trainings", 'outcomes_description':"This training will change your life."}
        rv = self.app.post('api/training', data=json.dumps(training), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Training of Trainings')
        self.assertEqual(response['outcomes_description'], 'This training will change your life.')
        self.assertIsNotNone(response['id'])

    def test_organization_basics(self):
        self.construct_organization()
        o = db.session.query(Organization).first()
        self.assertIsNotNone(o)
        o_id = o.id
        rv = self.app.get('/api/organization/%i' % o_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], o_id)
        self.assertEqual(response["name"], 'Staunton Makerspace')
        self.assertEqual(response["description"], 'A place full of surprise, delight, and amazing people. And tools. Lots of exciting tools.')

    def test_modify_organization_basics(self):
        self.construct_organization()
        o = db.session.query(Organization).first()
        self.assertIsNotNone(o)
        o_id = o.id
        rv = self.app.get('/api/organization/%i' % o_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['name'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        orig_date = response['last_updated']
        rv = self.app.put('/api/organization/%i' % o_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/organization/%i' % o_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_organization(self):
        o = self.construct_organization()
        o_id = o.id
        rv = self.app.get('api/organization/%i' % o_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/organization/%i' % o_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/organization/%i' % o_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_organization(self):
        organization = {'name':"Organization of Champions", 'description':"All the best people, all the time."}
        rv = self.app.post('api/organization', data=json.dumps(organization), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'Organization of Champions')
        self.assertEqual(response['description'], 'All the best people, all the time.')
        self.assertIsNotNone(response['id'])

    def test_category_basics(self):
        self.construct_category()
        c = db.session.query(Category).first()
        self.assertIsNotNone(c)
        c_id = c.id
        c.parent = self.construct_category(name="3d Printers")
        rv = self.app.get('/api/category/%i' % c_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
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
        rv = self.app.put('/api/category/%i' % c_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/category/%i' % c_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'JellyBoxes')
        self.assertEqual(response['parent']['name'], 'Strange Kitchen Gadgets')

    def test_delete_category(self):
        c = self.construct_category()
        c_id = c.id
        rv = self.app.get('api/category/%i' % c_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/category/%i' % c_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/category/%i' % c_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_category(self):
        category = {'name': "My Favorite Things"}
        rv = self.app.post('api/category', data=json.dumps(category), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'My Favorite Things')
        self.assertIsNotNone(response['id'])

    def test_category_has_links(self):
        self.construct_category()
        rv = self.app.get(
            '/api/category/1',
            follow_redirects=True,
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["_links"]["self"], '/api/category/1')
        self.assertEqual(response["_links"]["collection"], '/api/category')

    def test_category_has_children(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent=c1)
        rv = self.app.get(
            '/api/category/1',
            follow_redirects=True,
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["children"][0]['id'], 2)
        self.assertEqual(response["children"][0]['name'], "I'm the kid")

    def test_category_has_parents_and_that_parent_has_no_children(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent=c1)
        c3 = self.construct_category(name="I'm the grand kid", parent=c2)
        rv = self.app.get(
            '/api/category/3',
            follow_redirects=True,
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["parent"]['id'], 2)
        self.assertNotIn("children", response["parent"])

    def test_category_depth_is_limited(self):
        c1 = self.construct_category()
        c2 = self.construct_category(
            name="I'm the kid", parent=c1)
        c3 = self.construct_category(
            name="I'm the grand kid",
            parent=c2)
        c4 = self.construct_category(
            name="I'm the great grand kid",
            parent=c3)

        rv = self.app.get(
            '/api/category',
            follow_redirects=True,
            content_type="application/json")

        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))

        self.assertEqual(1, len(response))
        self.assertEqual(1, len(response[0]["children"]))

    def test_get_resource_by_category(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c)
        db.session.add(cr)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/resource' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(r.id, response[0]["id"])
        self.assertEqual(r.description, response[0]["resource"]["description"])

    def test_get_resource_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c)
        cr2 = ResourceCategory(resource=r, category=c2)
        db.session.add_all([cr, cr2])
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/resource' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(r.id, response[0]["id"])
        self.assertEqual(2,
                         len(response[0]["resource"]["resource_categories"]))
        self.assertEqual(
            "c1", response[0]["resource"]["resource_categories"][0]["category"]
            ["name"])

    def test_category_resource_count(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c)
        db.session.add(cr)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["resource_count"])

    def test_get_category_by_resource(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c)
        db.session.add(cr)
        db.session.commit()
        rv = self.app.get(
            '/api/resource/%i/category' % r.id,
            content_type="application/json")
        self.assertSuccess(rv)
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
        self.assertSuccess(rv)
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
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        rc_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/resource/%i/category' % r.id,
            data=json.dumps(rc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_resource(self):
        self.test_add_category_to_resource()
        rv = self.app.delete('/api/resource_category/%i' % 1)
        self.assertSuccess(rv)
        rv = self.app.get(
            '/api/resource/%i/category' % 1, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_get_study_by_category(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        db.session.add(cs)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/study' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(s.id, response[0]["id"])
        self.assertEqual(s.description, response[0]["study"]["description"])

    def test_get_study_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        cs2 = StudyCategory(study=s, category=c2)
        db.session.add_all([cs, cs2])
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/study' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(s.id, response[0]["id"])
        self.assertEqual(2,
                         len(response[0]["study"]["study_categories"]))
        self.assertEqual(
            "c1", response[0]["study"]["study_categories"][0]["category"]
            ["name"])

    def test_category_study_count(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        db.session.add(cs)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["study_count"])

    def test_get_category_by_study(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        db.session.add(cs)
        db.session.commit()
        rv = self.app.get(
            '/api/study/%i/category' % s.id,
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_study(self):
        c = self.construct_category()
        s = self.construct_study()

        sc_data = {"study_id": s.id, "category_id": c.id}

        rv = self.app.post(
            '/api/study_category',
            data=json.dumps(sc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(s.id, response["study_id"])

    def test_set_all_categories_on_study(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        s = self.construct_study()

        sc_data = [
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
            '/api/study/%i/category' % s.id,
            data=json.dumps(sc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        sc_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/study/%i/category' % s.id,
            data=json.dumps(sc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_study(self):
        self.test_add_category_to_study()
        rv = self.app.delete('/api/study_category/%i' % 1)
        self.assertSuccess(rv)
        rv = self.app.get(
            '/api/study/%i/category' % 1, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_get_training_by_category(self):
        c = self.construct_category()
        t = self.construct_training()
        ct = TrainingCategory(training=t, category=c)
        db.session.add(ct)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/training' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(t.id, response[0]["id"])
        self.assertEqual(t.description, response[0]["training"]["description"])

    def test_get_training_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        t = self.construct_training()
        ct = TrainingCategory(training=t, category=c)
        ct2 = TrainingCategory(training=t, category=c2)
        db.session.add_all([ct, ct2])
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/training' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(t.id, response[0]["id"])
        self.assertEqual(2,
                         len(response[0]["training"]["training_categories"]))
        self.assertEqual(
            "c1", response[0]["training"]["training_categories"][0]["category"]
            ["name"])

    def test_category_training_count(self):
        c = self.construct_category()
        t = self.construct_training()
        ct = TrainingCategory(training=t, category=c)
        db.session.add(ct)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["training_count"])

    def test_get_category_by_training(self):
        c = self.construct_category()
        t = self.construct_training()
        ct = TrainingCategory(training=t, category=c)
        db.session.add(ct)
        db.session.commit()
        rv = self.app.get(
            '/api/training/%i/category' % t.id,
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_training(self):
        c = self.construct_category()
        t = self.construct_training()

        tc_data = {"training_id": t.id, "category_id": c.id}

        rv = self.app.post(
            '/api/training_category',
            data=json.dumps(tc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(t.id, response["training_id"])

    def test_set_all_categories_on_training(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        t = self.construct_training()

        tc_data = [
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
            '/api/training/%i/category' % t.id,
            data=json.dumps(tc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        tc_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/training/%i/category' % t.id,
            data=json.dumps(tc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_training(self):
        self.test_add_category_to_training()
        rv = self.app.delete('/api/training_category/%i' % 1)
        self.assertSuccess(rv)
        rv = self.app.get(
            '/api/training/%i/category' % 1, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_user_basics(self):
        self.construct_user()
        u = db.session.query(User).first()
        self.assertIsNotNone(u)
        u_id = u.id
        headers = self.logged_in_headers(u)
        rv = self.app.get('/api/user/%i' % u_id,
                          follow_redirects=True,
                          content_type="application/json", headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], u_id)
        self.assertEqual(response["email"], 'stan@staunton.com')

    def test_modify_user_basics(self):
        self.construct_user()
        u = db.session.query(User).first()
        headers = self.logged_in_headers(u)
        self.assertIsNotNone(u)
        rv = self.app.get('/api/user/%i' % u.id, content_type="application/json", headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        response['email'] = 'ed@edwardos.com'
        orig_date = response['last_updated']
        rv = self.app.put('/api/user/%i' % u.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=headers)
        self.assertSuccess(rv)
        rv = self.app.get('/api/user/%i' % u.id, content_type="application/json", headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['email'], 'ed@edwardos.com')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_user(self):
        u = self.construct_user()
        u_id = u.id

        rv = self.app.get('api/user/%i' % u_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.app.get('api/user/%i' % u_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)

        rv = self.app.delete('api/user/%i' % u_id, content_type="application/json", headers=None)
        self.assertEqual(401, rv.status_code)
        rv = self.app.delete('api/user/%i' % u_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)

        rv = self.app.get('api/user/%i' % u_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.app.get('api/user/%i' % u_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_user(self):
        user = {'email': "tara@spiders.org"}
        rv = self.app.post('api/user', data=json.dumps(user), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['email'], 'tara@spiders.org')
        self.assertIsNotNone(response['id'])

    def logged_in_headers(self, user=None):
        # If no user is provided, generate a dummy Admin user
        if not user:
            user = User(
                id=7,
                email="admin@admin.org",
                password="myPass457",
                email_verified=True,
                role=Role.admin)

        # Add user if it's not already in database
        existing_user = None
        if user.id:
            existing_user = User.query.filter_by(id=user.id).first()
        if not existing_user and user.email:
            existing_user = User.query.filter_by(email=user.email).first()

        if not existing_user:
            db.session.add(user)
            db.session.commit()

        data = {
            'email': user.email,
            'password': 'myPass457'
        }

        rv = self.app.post(
            '/api/login_password',
            data=json.dumps(data),
            content_type="application/json")

        db_user = User.query.filter_by(email=user.email).first()
        return dict(
            Authorization='Bearer ' + db_user.encode_auth_token().decode())

    def test_create_user_with_password(self, id=8, email="tyrion@got.com", role=Role.user, password="peterpass"):
        data = {
            "id": id,
            "email": email
        }
        rv = self.app.post(
            '/api/user',
            data=json.dumps(data),
            follow_redirects=True,
            headers=self.logged_in_headers(),
            content_type="application/json")
        self.assertSuccess(rv)
        user = User.query.filter_by(id=id).first()
        user.password = password
        user.role = role
        db.session.add(user)
        db.session.commit()

        rv = self.app.get(
            '/api/user/%i' % user.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(email, response["email"])
        self.assertEqual(role.name, response["role"])
        self.assertEqual(True, user.is_correct_password(password))

        return user

    def test_login_user(self):
        user = self.test_create_user_with_password()
        data = {"email": "tyrion@got.com", "password": "peterpass"}
        # Login shouldn't work with email not yet verified
        rv = self.app.post(
            '/api/login_password',
            data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(400, rv.status_code)

        user.email_verified = True
        rv = self.app.post(
            '/api/login_password',
            data=json.dumps(data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response["token"])

        return user

    def test_get_current_user(self):
        """ Test for the current user status """
        user = self.test_login_user()

        # Now get the user back.
        response = self.app.get(
            '/api/session',
            headers=dict(
                Authorization='Bearer ' + user.encode_auth_token().decode()))
        self.assertSuccess(response)
        return json.loads(response.data.decode())

    def decode(self, encoded_words):
        """
        Useful for checking the content of email messages
        (which we store in an array for testing)
        """
        encoded_word_regex = r'=\?{1}(.+)\?{1}([b|q])\?{1}(.+)\?{1}='
        charset, encoding, encoded_text = re.match(encoded_word_regex,
                                                   encoded_words).groups()
        if encoding is 'b':
            byte_string = base64.b64decode(encoded_text)
        elif encoding is 'q':
            byte_string = quopri.decodestring(encoded_text)
        text = byte_string.decode(charset)
        text = text.replace("_", " ")
        return text

    def test_register_sends_email(self):
        message_count = len(TEST_MESSAGES)
        self.test_create_user_with_password()
        self.assertGreater(len(TEST_MESSAGES), message_count)
        self.assertEqual("STAR Drive: Confirm Email",
                         self.decode(TEST_MESSAGES[-1]['subject']))

        logs = EmailLog.query.all()
        self.assertIsNotNone(logs[-1].tracking_code)

    def test_forgot_password_sends_email(self):
        user = self.test_create_user_with_password()
        message_count = len(TEST_MESSAGES)
        data = {"email": user.email}
        rv = self.app.post(
            '/api/forgot_password',
            data=json.dumps(data),
            content_type="application/json")
        self.assertSuccess(rv)
        self.assertGreater(len(TEST_MESSAGES), message_count)
        self.assertEqual("STAR Drive: Password Reset Email",
                         self.decode(TEST_MESSAGES[-1]['subject']))

        logs = EmailLog.query.all()
        self.assertIsNotNone(logs[-1].tracking_code)

    def test_participant_basics(self):
        self.construct_participant(user=self.construct_user(), relationship=Relationship.dependent)
        p = db.session.query(Participant).first()
        self.assertIsNotNone(p)
        p_id = p.id
        rv = self.app.get('/api/participant/%i' % p_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], p_id)
        self.assertEqual(response["relationship"], p.relationship.name)

    def test_modify_participant_you_do_not_own(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        good_headers = self.logged_in_headers(u)

        p = db.session.query(Participant).first()
        odd_user = User(
                email="frankie@badfella.fr",
                password="h@corleet",
                email_verified=True,
                role=Role.user)
        participant = {'first_name': "Lil' Johnny", 'last_name': "Tables"}
        rv = self.app.put('/api/participant/%i' % p.id, data=json.dumps(participant), content_type="application/json",
                          follow_redirects=True)
        self.assertEqual(401, rv.status_code, "you have to be logged in to edit participant.")
        rv = self.app.put('/api/participant/%i' % p.id, data=json.dumps(participant), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers(odd_user))
        self.assertEqual(400, rv.status_code, "you have to have a relationship with the user to do stuff.")
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual("unrelated_participant", response['code'])
        rv = self.app.put('/api/participant/%i' % p.id, data=json.dumps(participant), content_type="application/json",
                          follow_redirects=True, headers=good_headers)
        self.assertEqual(200, rv.status_code, "The owner can edit the user.")

    def test_modify_participant_you_do_own(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_guardian)
        headers = self.logged_in_headers(u)
        participant = {'id': 567}
        rv = self.app.put('/api/participant/%i' % p.id, data=json.dumps(participant), content_type="application/json",
                          follow_redirects=True, headers=headers)
        self.assertSuccess(rv)
        p = db.session.query(Participant).filter_by(id=p.id).first()
        self.assertEqual(567, p.id)

    def test_modify_participant_basics_admin(self):
        self.construct_participant(user=self.construct_user(), relationship=Relationship.dependent)
        p = db.session.query(Participant).first()
        self.assertIsNotNone(p)
        p_id = p.id
        rv = self.app.get('/api/participant/%i' % p_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        response['user_id'] = 234
        orig_date = response['last_updated']
        rv = self.app.put('/api/participant/%i' % p_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assertSuccess(rv)
        rv = self.app.get('/api/participant/%i' % p_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['user_id'], 234)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_participant(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.dependent)
        p_id = p.id
        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)

        rv = self.app.delete('api/participant/%i' % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.app.delete('api/participant/%i' % p_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)

        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_participant(self):
        p = {'id': 7, 'relationship': 'self_participant'}
        rv = self.app.post('/api/session/participant', data=json.dumps(p), content_type="application/json",
                           follow_redirects=True)
        self.assertEqual(401, rv.status_code, "you can't create a participant without an account.")

        rv = self.app.post(
            '/api/session/participant', data=json.dumps(p),
            content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)

        participant = db.session.query(Participant).filter_by(id=p['id']).first()

        self.assertIsNotNone(participant.id)
        self.assertIsNotNone(participant.user_id)

    def test_create_participant_to_have_bad_relationship(self):
        participant = {'id': 234, 'relationship': 'free_loader'}
        rv = self.app.post('/api/session/participant', data=json.dumps(participant),
                           content_type="application/json", follow_redirects=True, headers=self.logged_in_headers())
        self.assertEqual(400, rv.status_code, "you can't create a participant using an invalid relationship")
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["code"], "unknown_relationship")

    def test_get_participant_by_user(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        db.session.commit()
        rv = self.app.get(
            '/api/user/%i' % u.id,
            content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(u.id, response['id'])
        self.assertEqual(1, len(response['participants']))
        self.assertEqual(p.relationship.name, response['participants'][0]["relationship"])

    def test_clinical_diagnoses_questionnaire_basics(self):
        self.construct_clinical_diagnoses_questionnaire()
        cq = db.session.query(ClinicalDiagnosesQuestionnaire).first()
        self.assertIsNotNone(cq)
        cq_id = cq.id
        rv = self.app.get('/api/q/clinical_diagnoses_questionnaire/%i' % cq_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], cq_id)
        self.assertEqual(response["medical"], cq.medical)
        self.assertEqual(response["genetic"], cq.genetic)

    def test_modify_clinical_diagnoses_questionnaire_basics(self):
        self.construct_clinical_diagnoses_questionnaire()
        cq = db.session.query(ClinicalDiagnosesQuestionnaire).first()
        self.assertIsNotNone(cq)
        cq_id = cq.id
        rv = self.app.get('/api/q/clinical_diagnoses_questionnaire/%i' % cq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['developmental'] = 'intellectual'
        response['mental_health'] = 'depression'
        response['medical'] = 'gastrointestinal'
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/clinical_diagnoses_questionnaire/%i' % cq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/clinical_diagnoses_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['developmental'], 'intellectual')
        self.assertEqual(response['mental_health'], 'depression')
        self.assertEqual(response['medical'], 'gastrointestinal')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_clinical_diagnoses_questionnaire(self):
        cq = self.construct_clinical_diagnoses_questionnaire()
        cq_id = cq.id
        rv = self.app.get('api/q/clinical_diagnoses_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/clinical_diagnoses_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/clinical_diagnoses_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_clinical_diagnoses_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        clinical_diagnoses_questionnaire = {'medical': 'seizure', 'genetic': 'fragileX', 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/clinical_diagnoses_questionnaire', data=json.dumps(clinical_diagnoses_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['medical'], 'seizure')
        self.assertEqual(response['genetic'], 'fragileX')
        self.assertIsNotNone(response['id'])

    def test_contact_questionnaire_basics(self):
        self.construct_contact_questionnaire()
        cq = db.session.query(ContactQuestionnaire).first()
        self.assertIsNotNone(cq)
        cq_id = cq.id
        rv = self.app.get('/api/q/contact_questionnaire/%i' % cq_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], cq_id)
        self.assertEqual(response["phone"], cq.phone)
        self.assertEqual(response["marketing_channel"], cq.marketing_channel)

    def test_modify_contact_questionnaire_basics(self):
        self.construct_contact_questionnaire()
        cq = db.session.query(ContactQuestionnaire).first()
        self.assertIsNotNone(cq)
        cq_id = cq.id
        rv = self.app.get('/api/q/contact_questionnaire/%i' % cq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['phone'] = '123-456-7890'
        response['zip'] = 22345
        response['marketing_channel'] = 'flyer'
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/contact_questionnaire/%i' % cq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/contact_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['phone'], '123-456-7890')
        self.assertEqual(response['zip'], 22345)
        self.assertEqual(response['marketing_channel'], 'flyer')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_contact_questionnaire(self):
        cq = self.construct_contact_questionnaire()
        cq_id = cq.id
        rv = self.app.get('api/q/contact_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/contact_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/contact_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_contact_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        contact_questionnaire = {'phone': "123-456-7890", 'marketing_channel': "Subway sign", 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/contact_questionnaire', data=json.dumps(contact_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['phone'], '123-456-7890')
        self.assertEqual(response['marketing_channel'], 'Subway sign')
        self.assertIsNotNone(response['id'])

    def test_current_behaviors_dependent_questionnaire_basics(self):
        self.construct_current_behaviors_dependent_questionnaire()
        cbdq = db.session.query(CurrentBehaviorsDependentQuestionnaire).first()
        self.assertIsNotNone(cbdq)
        cbdq_id = cbdq.id
        rv = self.app.get('/api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], cbdq_id)
        self.assertEqual(response["concerning_behaviors"], cbdq.concerning_behaviors)
        self.assertEqual(response["has_academic_difficulties"], cbdq.has_academic_difficulties)

    def test_modify_current_behaviors_dependent_questionnaire_basics(self):
        self.construct_current_behaviors_dependent_questionnaire()
        cbdq = db.session.query(CurrentBehaviorsDependentQuestionnaire).first()
        self.assertIsNotNone(cbdq)
        cbdq_id = cbdq.id
        rv = self.app.get('/api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['dependent_verbal_ability'] = 'nonVerbal'
        response['concerning_behaviors'] = 'elopement'
        response['has_academic_difficulties'] = False
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['dependent_verbal_ability'], 'nonVerbal')
        self.assertEqual(response['concerning_behaviors'], 'elopement')
        self.assertEqual(response['has_academic_difficulties'], False)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_current_behaviors_dependent_questionnaire(self):
        cbdq = self.construct_current_behaviors_dependent_questionnaire()
        cbdq_id = cbdq.id
        rv = self.app.get('api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_current_behaviors_dependent_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.dependent)
        headers = self.logged_in_headers(u)

        current_behaviors_dependent_questionnaire = {'dependent_verbal_ability': 'verbal, AACsystem',
                                           'has_academic_difficulties': False, 'participant_id': p.id}
        rv = self.app.post('api/flow/dependent_intake/current_behaviors_dependent_questionnaire',
                           data=json.dumps(current_behaviors_dependent_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['dependent_verbal_ability'], 'verbal, AACsystem')
        self.assertEqual(response['has_academic_difficulties'], False)
        self.assertIsNotNone(response['id'])

    def test_current_behaviors_self_questionnaire_basics(self):
        self.construct_current_behaviors_self_questionnaire()
        cbsq = db.session.query(CurrentBehaviorsSelfQuestionnaire).first()
        self.assertIsNotNone(cbsq)
        cbsq_id = cbsq.id
        rv = self.app.get('/api/q/current_behaviors_self_questionnaire/%i' % cbsq_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], cbsq_id)
        self.assertEqual(response["has_academic_difficulties"], cbsq.has_academic_difficulties)

    def test_modify_current_behaviors_self_questionnaire_basics(self):
        self.construct_current_behaviors_self_questionnaire()
        cbsq = db.session.query(CurrentBehaviorsSelfQuestionnaire).first()
        self.assertIsNotNone(cbsq)
        cbsq_id = cbsq.id
        rv = self.app.get('/api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['self_verbal_ability'] = 'nonVerbal'
        response['academic_difficulty_areas'] = 'math'
        response['has_academic_difficulties'] = False
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_verbal_ability'], 'nonVerbal')
        self.assertEqual(response['academic_difficulty_areas'], 'math')
        self.assertEqual(response['has_academic_difficulties'], False)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_current_behaviors_self_questionnaire(self):
        cbsq = self.construct_current_behaviors_self_questionnaire()
        cbsq_id = cbsq.id
        rv = self.app.get('api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_current_behaviors_self_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        current_behaviors_self_questionnaire = {'self_verbal_ability': 'verbal, AACsystem',
                                           'has_academic_difficulties': False, 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/current_behaviors_self_questionnaire',
                           data=json.dumps(current_behaviors_self_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_verbal_ability'], 'verbal, AACsystem')
        self.assertEqual(response['has_academic_difficulties'], False)
        self.assertIsNotNone(response['id'])

    def test_demographics_questionnaire_basics(self):
        self.construct_demographics_questionnaire()
        dq = db.session.query(DemographicsQuestionnaire).first()
        self.assertIsNotNone(dq)
        dq_id = dq.id
        rv = self.app.get('/api/q/demographics_questionnaire/%i' % dq_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], dq_id)
        self.assertEqual(response["birth_sex"], dq.birth_sex)
        self.assertEqual(response["gender_identity"], dq.gender_identity)

    def test_modify_demographics_questionnaire_basics(self):
        self.construct_demographics_questionnaire()
        dq = db.session.query(DemographicsQuestionnaire).first()
        self.assertIsNotNone(dq)
        dq_id = dq.id
        rv = self.app.get('/api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['gender_identity'] = 'genderOther'
        response['race_ethnicity'] = 'raceOther'
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/demographics_questionnaire/%i' % dq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['gender_identity'], 'genderOther')
        self.assertEqual(response['race_ethnicity'], 'raceOther')
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_demographics_questionnaire(self):
        dq = self.construct_demographics_questionnaire()
        dq_id = dq.id
        rv = self.app.get('api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_demographics_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        demographics_questionnaire = {'birth_sex': "female", 'gender_identity': "genderOther", 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/demographics_questionnaire', data=json.dumps(demographics_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['birth_sex'], 'female')
        self.assertEqual(response['gender_identity'], 'genderOther')
        self.assertIsNotNone(response['id'])

    def test_developmental_questionnaire_basics(self):
        self.construct_developmental_questionnaire()
        dq = db.session.query(DevelopmentalQuestionnaire).first()
        self.assertIsNotNone(dq)
        dq_id = dq.id
        rv = self.app.get('/api/q/developmental_questionnaire/%i' % dq_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], dq_id)
        self.assertEqual(response["had_birth_complications"], dq.had_birth_complications)
        self.assertEqual(response["when_motor_milestones"], dq.when_motor_milestones)

    def test_modify_developmental_questionnaire_basics(self):
        self.construct_developmental_questionnaire()
        dq = db.session.query(DevelopmentalQuestionnaire).first()
        self.assertIsNotNone(dq)
        dq_id = dq.id
        rv = self.app.get('/api/q/developmental_questionnaire/%i' % dq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['when_motor_milestones'] = 'notYet'
        response['when_language_milestones'] = 'notYet'
        response['when_toileting_milestones'] = 'early'
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/developmental_questionnaire/%i' % dq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/developmental_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['when_motor_milestones'], 'notYet')
        self.assertEqual(response['when_language_milestones'], 'notYet')
        self.assertEqual(response['when_toileting_milestones'], 'early')
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_developmental_questionnaire(self):
        dq = self.construct_developmental_questionnaire()
        dq_id = dq.id
        rv = self.app.get('api/q/developmental_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/developmental_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/developmental_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_developmental_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.dependent)
        headers = self.logged_in_headers(u)

        developmental_questionnaire = {'had_birth_complications': True, 'birth_complications_description': 'C-Section',
                                       'participant_id': p.id}
        rv = self.app.post('api/flow/dependent_intake/developmental_questionnaire', data=json.dumps(developmental_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['had_birth_complications'], True)
        self.assertEqual(response['birth_complications_description'], 'C-Section')
        self.assertIsNotNone(response['id'])

    def test_education_dependent_questionnaire_basics(self):
        self.construct_education_dependent_questionnaire()
        eq = db.session.query(EducationDependentQuestionnaire).first()
        self.assertIsNotNone(eq)
        eq_id = eq.id
        rv = self.app.get('/api/q/education_dependent_questionnaire/%i' % eq_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], eq_id)
        self.assertEqual(response["school_name"], eq.school_name)
        self.assertEqual(response["school_type"], eq.school_type)

    def test_modify_education_dependent_questionnaire_basics(self):
        self.construct_education_dependent_questionnaire()
        eq = db.session.query(EducationDependentQuestionnaire).first()
        self.assertIsNotNone(eq)
        eq_id = eq.id
        rv = self.app.get('/api/q/education_dependent_questionnaire/%i' % eq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['school_name'] = 'Sesame School'
        response['school_type'] = 'public'
        response['dependent_placement'] = 'vocational'
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/education_dependent_questionnaire/%i' % eq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/education_dependent_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['school_name'], 'Sesame School')
        self.assertEqual(response['school_type'], 'public')
        self.assertEqual(response['dependent_placement'], 'vocational')
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_education_dependent_questionnaire(self):
        eq = self.construct_education_dependent_questionnaire()
        eq_id = eq.id
        rv = self.app.get('api/q/education_dependent_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/education_dependent_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/education_dependent_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_education_dependent_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        education_dependent_questionnaire = {'attends_school': True, 'school_name': 'Attreyu Academy', 'participant_id': p.id}
        rv = self.app.post('api/flow/dependent_intake/education_dependent_questionnaire', data=json.dumps(education_dependent_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['attends_school'], True)
        self.assertEqual(response['school_name'], 'Attreyu Academy')
        self.assertIsNotNone(response['id'])

    def test_education_self_questionnaire_basics(self):
        self.construct_education_self_questionnaire()
        eq = db.session.query(EducationSelfQuestionnaire).first()
        self.assertIsNotNone(eq)
        eq_id = eq.id
        rv = self.app.get('/api/q/education_self_questionnaire/%i' % eq_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], eq_id)
        self.assertEqual(response["school_name"], eq.school_name)
        self.assertEqual(response["school_type"], eq.school_type)

    def test_modify_education_self_questionnaire_basics(self):
        self.construct_education_self_questionnaire()
        eq = db.session.query(EducationSelfQuestionnaire).first()
        self.assertIsNotNone(eq)
        eq_id = eq.id
        rv = self.app.get('/api/q/education_self_questionnaire/%i' % eq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['school_name'] = 'Sesame School'
        response['school_type'] = 'public'
        response['self_placement'] = 'vocational'
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/education_self_questionnaire/%i' % eq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/education_self_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['school_name'], 'Sesame School')
        self.assertEqual(response['school_type'], 'public')
        self.assertEqual(response['self_placement'], 'vocational')
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_education_self_questionnaire(self):
        eq = self.construct_education_self_questionnaire()
        eq_id = eq.id
        rv = self.app.get('api/q/education_self_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/education_self_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/education_self_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_education_self_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        education_self_questionnaire = {'attends_school': True, 'school_name': 'Attreyu Academy', 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/education_self_questionnaire', data=json.dumps(education_self_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['attends_school'], True)
        self.assertEqual(response['school_name'], 'Attreyu Academy')
        self.assertIsNotNone(response['id'])

    def test_employment_questionnaire_basics(self):
        self.construct_employment_questionnaire()
        eq = db.session.query(EmploymentQuestionnaire).first()
        self.assertIsNotNone(eq)
        eq_id = eq.id
        rv = self.app.get('/api/q/employment_questionnaire/%i' % eq_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], eq_id)
        self.assertEqual(response["is_currently_employed"], eq.is_currently_employed)
        self.assertEqual(response["employment_capacity"], eq.employment_capacity)
        self.assertEqual(response["has_employment_support"], eq.has_employment_support)

    def test_modify_employment_questionnaire_basics(self):
        self.construct_employment_questionnaire()
        eq = db.session.query(EmploymentQuestionnaire).first()
        self.assertIsNotNone(eq)
        eq_id = eq.id
        rv = self.app.get('/api/q/employment_questionnaire/%i' % eq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['is_currently_employed'] = False
        response['employment_capacity'] = None
        response['has_employment_support'] = True
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/employment_questionnaire/%i' % eq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/employment_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['is_currently_employed'], False)
        self.assertEqual(response['employment_capacity'], None)
        self.assertEqual(response['has_employment_support'], True)
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_employment_questionnaire(self):
        eq = self.construct_employment_questionnaire()
        eq_id = eq.id
        rv = self.app.get('api/q/employment_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/employment_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/employment_questionnaire/%i' % eq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_employment_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        employment_questionnaire = {'is_currently_employed': True, 'employment_capacity': 'partTime', 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/employment_questionnaire', data=json.dumps(employment_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['is_currently_employed'], True)
        self.assertEqual(response['employment_capacity'], 'partTime')
        self.assertIsNotNone(response['id'])

    def test_evaluation_history_dependent_questionnaire_basics(self):
        self.construct_evaluation_history_dependent_questionnaire()
        ehq = db.session.query(EvaluationHistoryDependentQuestionnaire).first()
        self.assertIsNotNone(ehq)
        ehq_id = ehq.id
        rv = self.app.get('/api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], ehq_id)
        self.assertEqual(response["self_identifies_autistic"], ehq.self_identifies_autistic)
        self.assertEqual(response["years_old_at_first_diagnosis"], ehq.years_old_at_first_diagnosis)

    def test_modify_evaluation_history_dependent_questionnaire_basics(self):
        self.construct_evaluation_history_dependent_questionnaire()
        ehq = db.session.query(EvaluationHistoryDependentQuestionnaire).first()
        self.assertIsNotNone(ehq)
        ehq_id = ehq.id
        rv = self.app.get('/api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['self_identifies_autistic'] = False
        response['years_old_at_first_diagnosis'] = 12
        response['who_diagnosed'] = 'healthTeam'
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_identifies_autistic'], False)
        self.assertEqual(response['years_old_at_first_diagnosis'], 12)
        self.assertEqual(response['who_diagnosed'], 'healthTeam')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_evaluation_history_dependent_questionnaire(self):
        ehq = self.construct_evaluation_history_dependent_questionnaire()
        ehq_id = ehq.id
        rv = self.app.get('api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_evaluation_history_dependent_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_guardian)
        headers = self.logged_in_headers(u)

        evaluation_history_dependent_questionnaire = {'self_identifies_autistic': True, 'years_old_at_first_diagnosis': 5,
                                            'participant_id': p.id}
        rv = self.app.post('api/flow/dependent_intake/evaluation_history_dependent_questionnaire',
                           data=json.dumps(evaluation_history_dependent_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_identifies_autistic'], True)
        self.assertEqual(response['years_old_at_first_diagnosis'], 5)
        self.assertIsNotNone(response['id'])

    def test_evaluation_history_self_questionnaire_basics(self):
        self.construct_evaluation_history_self_questionnaire()
        ehq = db.session.query(EvaluationHistorySelfQuestionnaire).first()
        self.assertIsNotNone(ehq)
        ehq_id = ehq.id
        rv = self.app.get('/api/q/evaluation_history_self_questionnaire/%i' % ehq_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], ehq_id)
        self.assertEqual(response["self_identifies_autistic"], ehq.self_identifies_autistic)
        self.assertEqual(response["years_old_at_first_diagnosis"], ehq.years_old_at_first_diagnosis)

    def test_modify_evaluation_history_self_questionnaire_basics(self):
        self.construct_evaluation_history_self_questionnaire()
        ehq = db.session.query(EvaluationHistorySelfQuestionnaire).first()
        self.assertIsNotNone(ehq)
        ehq_id = ehq.id
        rv = self.app.get('/api/q/evaluation_history_self_questionnaire/%i' % ehq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['self_identifies_autistic'] = False
        response['years_old_at_first_diagnosis'] = 12
        response['who_diagnosed'] = 'healthTeam'
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/evaluation_history_self_questionnaire/%i' % ehq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/evaluation_history_self_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_identifies_autistic'], False)
        self.assertEqual(response['years_old_at_first_diagnosis'], 12)
        self.assertEqual(response['who_diagnosed'], 'healthTeam')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_evaluation_history_self_questionnaire(self):
        ehq = self.construct_evaluation_history_self_questionnaire()
        ehq_id = ehq.id
        rv = self.app.get('api/q/evaluation_history_self_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/evaluation_history_self_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/evaluation_history_self_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_evaluation_history_self_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_guardian)
        headers = self.logged_in_headers(u)

        evaluation_history_self_questionnaire = {'self_identifies_autistic': True, 'years_old_at_first_diagnosis': 5,
                                            'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/evaluation_history_self_questionnaire',
                           data=json.dumps(evaluation_history_self_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_identifies_autistic'], True)
        self.assertEqual(response['years_old_at_first_diagnosis'], 5)
        self.assertIsNotNone(response['id'])

    def test_home_dependent_questionnaire_basics(self):
        self.construct_home_dependent_questionnaire()
        hq = db.session.query(HomeDependentQuestionnaire).first()
        self.assertIsNotNone(hq)
        hq_id = hq.id
        rv = self.app.get('/api/q/home_dependent_questionnaire/%i' % hq_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], hq_id)
        self.assertEqual(response["participant_id"], hq.participant_id)
        self.assertEqual(response["user_id"], hq.user_id)
        self.assertEqual(response["dependent_living_situation"], hq.dependent_living_situation)
        self.assertEqual(response["struggle_to_afford"], hq.struggle_to_afford)
        self.assertEqual(len(response["housemates"]), len(hq.housemates))

    def test_modify_home_dependent_questionnaire_basics(self):
        self.construct_home_dependent_questionnaire()
        hq = db.session.query(HomeDependentQuestionnaire).first()
        self.assertIsNotNone(hq)
        hq_id = hq.id
        rv = self.app.get('/api/q/home_dependent_questionnaire/%i' % hq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['participant_id'] = self.construct_participant(user=self.construct_user(), relationship=Relationship.dependent).id
        response['dependent_living_situation'] = 'caregiver'
        response['struggle_to_afford'] = True
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/home_dependent_questionnaire/%i' % hq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        self.construct_housemate(name='Debbie Danger', home_dependent_questionnaire=hq)
        rv = self.app.get('/api/q/home_dependent_questionnaire/%i' % hq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['dependent_living_situation'], 'caregiver')
        self.assertEqual(response['struggle_to_afford'], True)
        self.assertEqual(len(response['housemates']), 2)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_home_dependent_questionnaire(self):
        hq = self.construct_home_dependent_questionnaire()
        hq_id = hq.id
        rv = self.app.get('api/q/home_dependent_questionnaire/%i' % hq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/home_dependent_questionnaire/%i' % hq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/home_dependent_questionnaire/%i' % hq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_home_dependent_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        home_dependent_questionnaire = {'dependent_living_situation': 'family', 'struggle_to_afford': False, 'participant_id': p.id}
        rv = self.app.post('api/flow/dependent_intake/home_dependent_questionnaire',
                           data=json.dumps(home_dependent_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['participant_id'], p.id)
        self.assertEqual(response['dependent_living_situation'], 'family')
        self.assertEqual(response['struggle_to_afford'], False)
        self.assertIsNotNone(response['id'])

    def test_home_self_questionnaire_basics(self):
        self.construct_home_self_questionnaire()
        hq = db.session.query(HomeSelfQuestionnaire).first()
        self.assertIsNotNone(hq)
        hq_id = hq.id
        rv = self.app.get('/api/q/home_self_questionnaire/%i' % hq_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], hq_id)
        self.assertEqual(response["participant_id"], hq.participant_id)
        self.assertEqual(response["user_id"], hq.user_id)
        self.assertEqual(response["self_living_situation"], hq.self_living_situation)
        self.assertEqual(response["struggle_to_afford"], hq.struggle_to_afford)
        self.assertEqual(len(response["housemates"]), len(hq.housemates))

    def test_modify_home_self_questionnaire_basics(self):
        self.construct_home_self_questionnaire()
        hq = db.session.query(HomeSelfQuestionnaire).first()
        self.assertIsNotNone(hq)
        hq_id = hq.id
        rv = self.app.get('/api/q/home_self_questionnaire/%i' % hq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['participant_id'] = self.construct_participant(user=self.construct_user(), relationship=Relationship.self_participant).id
        response['self_living_situation'] = 'caregiver'
        response['struggle_to_afford'] = True
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/home_self_questionnaire/%i' % hq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        self.construct_housemate(name='Debbie Danger', home_self_questionnaire=hq)
        rv = self.app.get('/api/q/home_self_questionnaire/%i' % hq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_living_situation'], 'caregiver')
        self.assertEqual(response['struggle_to_afford'], True)
        self.assertEqual(len(response['housemates']), 2)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_home_self_questionnaire(self):
        hq = self.construct_home_self_questionnaire()
        hq_id = hq.id
        rv = self.app.get('api/q/home_self_questionnaire/%i' % hq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/home_self_questionnaire/%i' % hq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/home_self_questionnaire/%i' % hq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_home_self_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        home_self_questionnaire = {'self_living_situation': 'family', 'struggle_to_afford': False, 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/home_self_questionnaire',
                           data=json.dumps(home_self_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['participant_id'], p.id)
        self.assertEqual(response['self_living_situation'], 'family')
        self.assertEqual(response['struggle_to_afford'], False)
        self.assertIsNotNone(response['id'])

    def test_identification_questionnaire_basics(self):
        self.construct_identification_questionnaire()
        iq = db.session.query(IdentificationQuestionnaire).first()
        self.assertIsNotNone(iq)
        iq_id = iq.id
        rv = self.app.get('/api/q/identification_questionnaire/%i' % iq_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], iq_id)
        self.assertEqual(response["first_name"], iq.first_name)
        self.assertEqual(response["nickname"], iq.nickname)
        self.assertEqual(response["birth_state"], iq.birth_state)

    def test_modify_identification_questionnaire_basics(self):
        self.construct_identification_questionnaire()
        iq = db.session.query(IdentificationQuestionnaire).first()
        self.assertIsNotNone(iq)
        iq_id = iq.id
        rv = self.app.get('/api/q/identification_questionnaire/%i' % iq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['first_name'] = 'Helga'
        response['birth_city'] = 'Staunton'
        response['is_first_name_preferred'] = True
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/identification_questionnaire/%i' % iq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/identification_questionnaire/%i' % iq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['first_name'], 'Helga')
        self.assertEqual(response['birth_city'], 'Staunton')
        self.assertEqual(response['is_first_name_preferred'], True)
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_identification_questionnaire(self):
        iq = self.construct_identification_questionnaire()
        iq_id = iq.id
        rv = self.app.get('api/q/identification_questionnaire/%i' % iq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/identification_questionnaire/%i' % iq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/identification_questionnaire/%i' % iq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_identification_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        identification_questionnaire = {'first_name': 'Eloise', 'middle_name': 'Elora', 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/identification_questionnaire', data=json.dumps(identification_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['first_name'], 'Eloise')
        self.assertEqual(response['middle_name'], 'Elora')
        self.assertIsNotNone(response['id'])

    def test_supports_questionnaire_basics(self):
        self.construct_supports_questionnaire()
        sq = db.session.query(SupportsQuestionnaire).first()
        self.assertIsNotNone(sq)
        sq_id = sq.id
        rv = self.app.get('/api/q/supports_questionnaire/%i' % sq_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], sq_id)
        self.assertEqual(response["participant_id"], sq.participant_id)
        self.assertEqual(response["user_id"], sq.user_id)
        self.assertEqual(len(response["assistive_devices"]), len(sq.assistive_devices))
        self.assertEqual(len(response["medications"]), len(sq.medications))
        self.assertEqual(len(response["therapies"]), len(sq.therapies))

    def test_modify_supports_questionnaire_basics(self):
        self.construct_supports_questionnaire()
        sq = db.session.query(SupportsQuestionnaire).first()
        self.assertIsNotNone(sq)
        sq_id = sq.id
        rv = self.app.get('/api/q/supports_questionnaire/%i' % sq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['participant_id'] = self.construct_participant(user=self.construct_user(), relationship=Relationship.self_participant).id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/supports_questionnaire/%i' % sq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        self.construct_medication(name='Iocane Powder', supports_questionnaire=sq)
        self.construct_therapy(type='socialSkills', supports_questionnaire=sq)
        self.construct_assistive_device(type='scooter', supports_questionnaire=sq)
        rv = self.app.get('/api/q/supports_questionnaire/%i' % sq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response['medications']), 2)
        self.assertEqual(len(response['therapies']), 2)
        self.assertEqual(len(response['assistive_devices']), 2)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_supports_questionnaire(self):
        sq = self.construct_supports_questionnaire()
        sq_id = sq.id
        rv = self.app.get('api/q/supports_questionnaire/%i' % sq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/supports_questionnaire/%i' % sq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/supports_questionnaire/%i' % sq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_supports_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        supports_questionnaire = {'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/supports_questionnaire',
                           data=json.dumps(supports_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['participant_id'], p.id)
        self.assertIsNotNone(response['id'])

    def test_questionnare_post_fails_if_flow_does_not_exist(self):
        evaluation_history_self_questionnaire = {'self_identifies_autistic': True, 'years_old_at_first_diagnosis': 5}
        rv = self.app.post('api/flow/noSuchFlow/evaluation_history_self_questionnaire',
                           data=json.dumps(evaluation_history_self_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code,
                          "This endpoint should require that the flow exists and that the question is in the flow.")
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response)
        self.assertEqual("Unknown path.", response["message"],
                          "There should be a clear error message explaining what went wrong.")

    def test_questionnare_post_fails_if_question_not_in_flow(self):
        evaluation_history_self_questionnaire = {'self_identifies_autistic': True, 'years_old_at_first_diagnosis': 5}
        rv = self.app.post('api/flow/self_intake/guardian_demographics_questionnaire',
                           data=json.dumps(evaluation_history_self_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=self.logged_in_headers())
        self.assertEqual(400, rv.status_code,
                          "This endpoint should require that the flow exists and that the question is in the flow.")
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response)
        self.assertEqual("not_in_the_flow", response["code"],
                          "There should be a clear error message explaining what went wrong.")

    def test_questionnare_post_fails_if_not_logged_in(self):
        cq = {'first_name': "Darah", 'marketing_channel': "Subway sign"}
        rv = self.app.post('api/flow/self_intake/contact_questionnaire', data=json.dumps(cq), content_type="application/json",
                           follow_redirects=True)
        self.assertEqual(401, rv.status_code)
        pass

    def test_questionnaire_post_fails_if_user_not_connected_to_participant(self):
        cq = {'first_name': "Darah", 'marketing_channel': "Subway sign"}
        rv = self.app.post('api/flow/self_intake/contact_questionnaire', data=json.dumps(cq), content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers())
        self.assertEqual(400, rv.status_code,
                          "This endpoint should require a participant id that is associated with current user.")
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response)
        self.assertEqual("Unable to save the provided object.", response["message"],
                          "There should be a clear error message explaining what went wrong.")

    def test_questionnionare_post_creates_log_record(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        cq = {'first_name': "Darah", 'marketing_channel': "Subway sign", 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/contact_questionnaire', data=json.dumps(cq), content_type="application/json",
                           follow_redirects=True, headers=headers)
        self.assertSuccess(rv)
        log = db.session.query(StepLog).all()
        self.assertIsNotNone(log)
        self.assertTrue(len(log) > 0)

    def test_flow_endpoint(self):
        # It should be possible to get a list of available flows
        rv = self.app.get('api/flow', content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(200, rv.status_code)
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)

    def test_intake_flows_endpoint(self):
        # Are the basics correct about the existing intake flows?
        rv = self.app.get('api/flow', content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(200, rv.status_code)
        response = json.loads(rv.get_data(as_text=True))
        for i in response:
            if i['name'] == 'self_intake':
                self.assertEqual(len(i['steps']), 10)
                self.assertEqual(i['steps'][8]['name'], 'employment_questionnaire')
            if i['name'] == 'dependent_intake':
                self.assertEqual(len(i['steps']), 9)
                self.assertEqual(i['steps'][5]['name'], 'developmental_questionnaire')
            if i['name'] == 'guardian_intake':
                self.assertEqual(len(i['steps']), 3)
                self.assertEqual(i['steps'][1]['name'], 'contact_questionnaire')

    def test_self_intake_flow_with_user(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)
        rv = self.app.get('api/flow/self_intake/%i' % p.id, content_type="application/json", headers=headers)
        self.assertEqual(200, rv.status_code)
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response)
        self.assertEqual('self_intake', response['name'])
        self.assertIsNotNone(response['steps'])
        self.assertTrue(len(response['steps']) > 0)
        self.assertEqual('identification_questionnaire', response['steps'][0]['name'])
        self.assertEqual(QuestionService.TYPE_IDENTIFYING, response['steps'][0]['type'])
        self.assertEqual(Step.STATUS_INCOMPLETE, response['steps'][0]['status'])

        cq = {
            'first_name': "Darah",
            'middle_name': "Soo",
            'last_name': "Ubway",
            'is_first_name_preferred': True,
            'birthdate': '02/02/2002',
            'birth_city': 'Staunton',
            'birth_state': 'VA',
            'is_english_primary': True,
            'participant_id': p.id
        }
        rv = self.app.post('api/flow/self_intake/identification_questionnaire', data=json.dumps(cq), content_type="application/json",
                           follow_redirects=True, headers=headers)

        rv = self.app.get('api/flow/self_intake/%i' % p.id, content_type="application/json", headers=headers)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual('identification_questionnaire', response['steps'][0]['name'])
        self.assertEqual(Step.STATUS_COMPLETE, response['steps'][0]['status'])
        self.assertIsNotNone(response['steps'][0]['date_completed'])
