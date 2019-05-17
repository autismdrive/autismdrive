from tests.base_test import BaseTest
from app.model.flow import Step
from app.question_service import QuestionService
import json
import random
import string
import unittest
import openpyxl
import io
from app import db, app, elastic_index
from app.model.user import User, Role
from app.model.participant import Participant, Relationship
from app.model.questionnaires.assistive_device import AssistiveDevice
from app.model.questionnaires.alternative_augmentative import AlternativeAugmentative
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
from app.model.questionnaires.professional_profile_questionnaire import ProfessionalProfileQuestionnaire
from app.model.questionnaires.medication import Medication
from app.model.questionnaires.supports_questionnaire import SupportsQuestionnaire
from app.model.questionnaires.therapy import Therapy
from app.model.step_log import StepLog


class TestQuestionnaire(BaseTest, unittest.TestCase):

    def randomString(self):
        char_set = string.ascii_uppercase + string.digits
        return ''.join(random.sample(char_set * 6, 6))

    def test_base_endpoint(self):
        rv = self.app.get('/',
                          follow_redirects=True,
                          content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))

        endpoints = [
            ('api.categorybyresourceendpoint', '/api/resource/<resource_id>/category'),
            ('api.categorybystudyendpoint', '/api/study/<study_id>/category'),
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
            ('api.userendpoint', '/api/user/<id>'),
            ('api.userlistendpoint', '/api/user'),
            ('auth.forgot_password', '/api/forgot_password'),
            ('auth.login_password', '/api/login_password'),
            ('auth.reset_password', '/api/reset_password'),
        ]

        for endpoint in endpoints:
            self.assertEqual(response[endpoint[0]], endpoint[1])

    def get_field_from_response(self, response, name):
        for field in response['fields']:
            if field["name"] == name:
                return field

    def construct_admin_user(self, email="rmond@virginia.gov"):
        user = User(email=email, role=Role.admin)
        db.session.add(user)
        db.session.commit()

        db_user = db.session.query(User).filter_by(email=user.email).first()
        self.assertEqual(db_user.role, user.role)
        return db_user

    def construct_assistive_device(self, type_group='mobility', type='prosthetic', timeframe='current',
                                   notes='I love my new leg!', supports_questionnaire=None):
        ad = AssistiveDevice(type=type, timeframe=timeframe, notes=notes)
        if supports_questionnaire is not None:
            ad.supports_questionnaire_id = supports_questionnaire.id

        db.session.add(ad)
        db.session.commit()

        db_ad = db.session.query(AssistiveDevice).filter_by(last_updated=ad.last_updated).first()
        self.assertEqual(db_ad.notes, ad.notes)
        self.assertEqual(db_ad.type_group, ad.type_group)
        self.assertEqual(db_ad.type, ad.type)
        return db_ad

    def construct_alternative_augmentative(self, type='lowTechAAC', timeframe='current', notes='We use pen and paper', supports_questionnaire=None):

        aac = AlternativeAugmentative(type=type, timeframe=timeframe, notes=notes)
        if supports_questionnaire is not None:
            aac.supports_questionnaire_id = supports_questionnaire.id

        db.session.add(aac)
        db.session.commit()

        db_aac = db.session.query(AlternativeAugmentative).filter_by(last_updated=aac.last_updated).first()
        self.assertEqual(db_aac.notes, aac.notes)
        return db_aac

    def construct_clinical_diagnoses_questionnaire(self, developmental=['speechLanguage'], mental_health=['ocd'],
                                                   medical=['insomnia'], genetic=['corneliaDeLange'], participant=None,
                                                   user=None):

        cdq = ClinicalDiagnosesQuestionnaire(developmental=developmental, mental_health=mental_health, medical=medical,
                                             genetic=genetic)
        if user is None:
            u = self.construct_user(email='clinic@questionnaire.com')
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
            u = self.construct_user(email='contact@questionnaire.com')
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
                                                            concerning_behaviors=['hoarding'],
                                                            has_academic_difficulties=True,
                                                            academic_difficulty_areas=['math', 'writing'],
                                                            participant=None, user=None):

        cb = CurrentBehaviorsDependentQuestionnaire(dependent_verbal_ability=dependent_verbal_ability,
                                                    concerning_behaviors=concerning_behaviors,
                                                    has_academic_difficulties=has_academic_difficulties,
                                                    academic_difficulty_areas=academic_difficulty_areas)
        if user is None:
            u = self.construct_user(email='cbd@questionnaire.com')
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

        db_cbd = db.session.query(CurrentBehaviorsDependentQuestionnaire).filter_by(
            participant_id=cb.participant_id).first()
        self.assertEqual(db_cbd.concerning_behaviors, cb.concerning_behaviors)
        return db_cbd

    def construct_current_behaviors_self_questionnaire(self, self_verbal_ability='verbal',
                                                       has_academic_difficulties=True, academic_difficulty_areas='math',
                                                       participant=None, user=None):

        cb = CurrentBehaviorsSelfQuestionnaire(self_verbal_ability=self_verbal_ability,
                                               has_academic_difficulties=has_academic_difficulties,
                                               academic_difficulty_areas=academic_difficulty_areas)
        if user is None:
            u = self.construct_user(email='cbs@questionnaire.com')
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
            u = self.construct_user(email='demograph@questionnaire.com')
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
                                              when_language_milestones='early', when_toileting_milestones='notYet',
                                              participant=None, user=None):

        dq = DevelopmentalQuestionnaire(had_birth_complications=had_birth_complications,
                                        when_motor_milestones=when_motor_milestones,
                                        when_language_milestones=when_language_milestones,
                                        when_toileting_milestones=when_toileting_milestones)
        if user is None:
            u = self.construct_user(email='develop@questionnaire.com')
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

    def construct_education_dependent_questionnaire(self, attends_school=True, school_name='Harvard',
                                                    school_type='privateSchool',
                                                    dependent_placement='graduate', participant=None, user=None):

        eq = EducationDependentQuestionnaire(attends_school=attends_school, school_name=school_name,
                                             school_type=school_type,
                                             dependent_placement=dependent_placement)
        if user is None:
            u = self.construct_user(email='edudep@questionnaire.com')
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

    def construct_education_self_questionnaire(self, attends_school=True, school_name='Harvard',
                                               school_type='privateSchool',
                                               self_placement='graduate', participant=None, user=None):

        eq = EducationSelfQuestionnaire(attends_school=attends_school, school_name=school_name, school_type=school_type,
                                        self_placement=self_placement)

        if user is None:
            u = self.construct_user(email='eduself@questionnaire.com')
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
            u = self.construct_user(email='employ@questionnaire.com')
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

    def construct_evaluation_history_dependent_questionnaire(self, self_identifies_autistic=True,
                                                             has_autism_diagnosis=True,
                                                             years_old_at_first_diagnosis=7,
                                                             who_diagnosed="pediatrician",
                                                             participant=None, user=None):

        ehq = EvaluationHistoryDependentQuestionnaire(self_identifies_autistic=self_identifies_autistic,
                                                      has_autism_diagnosis=has_autism_diagnosis,
                                                      years_old_at_first_diagnosis=years_old_at_first_diagnosis,
                                                      who_diagnosed=who_diagnosed)
        if user is None:
            u = self.construct_user(email='evaldep@questionnaire.com')
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

        db_ehq = db.session.query(EvaluationHistoryDependentQuestionnaire).filter_by(
            participant_id=ehq.participant_id).first()
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
            u = self.construct_user(email='evalself@questionnaire.com')
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

        db_ehq = db.session.query(EvaluationHistorySelfQuestionnaire).filter_by(
            participant_id=ehq.participant_id).first()
        self.assertEqual(db_ehq.who_diagnosed, ehq.who_diagnosed)
        return db_ehq

    def construct_home_dependent_questionnaire(self, dependent_living_situation='fullTimeGuardian', housemates=None,
                                               struggle_to_afford=False, participant=None, user=None):

        hq = HomeDependentQuestionnaire(dependent_living_situation=dependent_living_situation,
                                        struggle_to_afford=struggle_to_afford)

        if user is None:
            u = self.construct_user(email='homedep@questionnaire.com')
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

    def construct_home_self_questionnaire(self, self_living_situation='alone', housemates=None,
                                          struggle_to_afford=False,
                                          participant=None, user=None):

        hq = HomeSelfQuestionnaire(self_living_situation=self_living_situation, struggle_to_afford=struggle_to_afford)

        if user is None:
            u = self.construct_user(email='homeself@questionnaire.com')
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
            u = self.construct_user(email='ident@questionnaire.com')
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

    def construct_professional_questionnaire(self, purpose="profResearch",
                                             professional_identity=["artTher", "profOther"],
                                             professional_identity_other="Astronaut",
                                             learning_interests=["insuranceCov", "learnOther"],
                                             learning_interests_other="Data plotting using dried fruit",
                                             currently_work_with_autistic=True, previous_work_with_autistic=False,
                                             length_work_with_autistic='3 minutes', participant=None, user=None):

        pq = ProfessionalProfileQuestionnaire(purpose=purpose, professional_identity=professional_identity,
                                              professional_identity_other=professional_identity_other,
                                              learning_interests=learning_interests,
                                              learning_interests_other=learning_interests_other,
                                              currently_work_with_autistic=currently_work_with_autistic,
                                              previous_work_with_autistic=previous_work_with_autistic,
                                              length_work_with_autistic=length_work_with_autistic)
        if user is None:
            u = self.construct_user(email='prof@questionnaire.com')
            pq.user_id = u.id
        else:
            u = user
            pq.user_id = u.id

        if participant is None:
            pq.participant_id = self.construct_participant(user=u, relationship=Relationship.dependent).id
        else:
            pq.participant_id = participant.id

        db.session.add(pq)
        db.session.commit()

        db_pq = db.session.query(ProfessionalProfileQuestionnaire).filter_by(participant_id=pq.participant_id).first()
        self.assertEqual(db_pq.learning_interests, pq.learning_interests)
        return db_pq

    def construct_medication(self, symptom='symptomInsomnia', name='Magic Potion', notes='I feel better than ever!', supports_questionnaire=None):

        m = Medication(symptom=symptom, name=name, notes=notes)
        if supports_questionnaire is not None:
            m.supports_questionnaire_id = supports_questionnaire.id

        db.session.add(m)
        db.session.commit()

        db_m = db.session.query(Medication).filter_by(last_updated=m.last_updated).first()
        self.assertEqual(db_m.notes, m.notes)
        return db_m

    def construct_therapy(self, type='behavioral', timeframe='current', notes='Small steps',
                          supports_questionnaire=None):

        t = Therapy(type=type, timeframe=timeframe, notes=notes)
        if supports_questionnaire is not None:
            t.supports_questionnaire_id = supports_questionnaire.id

        db.session.add(t)
        db.session.commit()

        db_t = db.session.query(Therapy).filter_by(last_updated=t.last_updated).first()
        self.assertEqual(db_t.notes, t.notes)
        return db_t

    def construct_supports_questionnaire(self, medications=None, therapies=None, assistive_devices=None,
                                         alternative_augmentative=None, participant=None, user=None):

        sq = SupportsQuestionnaire()
        if user is None:
            u = self.construct_user(email='support@questionnaire.com')
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

        if alternative_augmentative is None:
            self.construct_alternative_augmentative(supports_questionnaire=sq)
        else:
            sq.alternative_augmentative = alternative_augmentative

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

    def construct_all_questionnaires(self):
        user = self.construct_user()
        participant = self.construct_participant(user=user, relationship=Relationship.dependent)
        self.construct_clinical_diagnoses_questionnaire(user=user, participant=participant)
        self.construct_contact_questionnaire(user=user, participant=participant)
        self.construct_current_behaviors_dependent_questionnaire(user=user, participant=participant)
        self.construct_current_behaviors_self_questionnaire(user=user, participant=participant)
        self.construct_demographics_questionnaire(user=user, participant=participant)
        self.construct_developmental_questionnaire(user=user, participant=participant)
        self.construct_education_dependent_questionnaire(user=user, participant=participant)
        self.construct_education_self_questionnaire(user=user, participant=participant)
        self.construct_employment_questionnaire(user=user, participant=participant)
        self.construct_evaluation_history_dependent_questionnaire(user=user, participant=participant)
        self.construct_evaluation_history_self_questionnaire(user=user, participant=participant)
        self.construct_home_dependent_questionnaire(user=user, participant=participant)
        self.construct_home_self_questionnaire(user=user, participant=participant)
        self.construct_identification_questionnaire(user=user, participant=participant)
        self.construct_professional_questionnaire(user=user, participant=participant)
        self.construct_supports_questionnaire(user=user, participant=participant)

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

    def test_search_basics(self):
        elastic_index.clear()
        rainbow_query = {'words': 'rainbows', 'filters': []}
        world_query = {'words': 'world', 'filters': []}
        search_results = self.search(rainbow_query)
        self.assertEqual(0, len(search_results["hits"]))
        search_results = self.search(world_query)
        self.assertEqual(0, len(search_results["hits"]))

        # test that elastic resource is created with post
        resource = {'title': "space unicorn", 'description': "delivering rainbows"}
        rv = self.app.post('api/resource', data=json.dumps(resource), content_type="application/json",
                           follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))

        search_results = self.search(rainbow_query)
        self.assertEqual(1, len(search_results["hits"]))
        self.assertEqual(search_results['hits'][0]['id'], response['id'])
        self.assertEqual(search_results['hits'][0]['title'], response['title'])
        self.assertEqual(search_results['hits'][0]['type'], "resource")
        self.assertEqual(search_results['hits'][0]['highlights'], "delivering <em>rainbows</em>")
        self.assertIsNotNone(search_results['hits'][0]['last_updated'])
        search_results = self.search(world_query)
        self.assertEqual(0, len(search_results["hits"]))

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
        study = {'title': "space platypus", 'description': "delivering umbrellas"}
        rv = self.app.post('api/study', data=json.dumps(study), content_type="application/json",
                           follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))

        search_results = self.search(umbrella_query)
        self.assertEqual(1, len(search_results["hits"]))
        self.assertEqual(search_results['hits'][0]['id'], response['id'])
        search_results = self.search(universe_query)
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
        world_query = {'words': 'world', 'filters': []}
        resource = self.construct_resource(
            title='space unicorn', description="delivering rainbows")
        search_results = self.search(rainbow_query)
        self.assertEqual(1, len(search_results["hits"]))
        elastic_index.remove_document(resource, 'Resource')
        search_results = self.search(world_query)
        self.assertEqual(0, len(search_results["hits"]))

    def test_user_basics(self):
        self.construct_user()
        u = db.session.query(User).first()
        self.assertIsNotNone(u)
        u_id = u.id
        headers = self.logged_in_headers(u)
        rv = self.app.get('/api/user/%i' % u_id,
                          follow_redirects=True,
                          content_type="application/json", headers=headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], u_id)
        self.assertEqual(response["email"], 'stan@staunton.com')

    def test_modify_user_basics(self):
        self.construct_user()
        u = db.session.query(User).first()
        admin_headers = self.logged_in_headers()
        user_headers = self.logged_in_headers(u)
        self.assertIsNotNone(u)

        # A user should be able to access and modify their user record, with the exception of making themselves Admin
        rv = self.app.get('/api/user/%i' % u.id, content_type="application/json", headers=user_headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        response['email'] = 'ed@edwardos.com'
        orig_date = response['last_updated']
        rv = self.app.put('/api/user/%i' % u.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=user_headers)
        self.assert_success(rv)

        # Only Admin users can make other admin users
        response['role'] = 'admin'
        rv = self.app.put('/api/user/%i' % u.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=admin_headers)
        self.assert_success(rv)

        rv = self.app.get('/api/user/%i' % u.id, content_type="application/json", headers=user_headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['email'], 'ed@edwardos.com')
        self.assertEqual(response['role'], 'admin')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_user(self):
        u = self.construct_user()
        u_id = u.id

        rv = self.app.get('api/user/%i' % u_id, content_type="application/json")

    def test_questionnare_post_fails_if_not_logged_in(self):
        cq = {'first_name': "Darah", 'marketing_channel': "Subway sign"}
        rv = self.app.post('api/flow/self_intake/contact_questionnaire', data=json.dumps(cq),
                           content_type="application/json",
                           follow_redirects=True)
        self.assertEqual(401, rv.status_code)
        pass

    def test_questionnaire_post_fails_if_user_not_connected_to_participant(self):
        cq = {'first_name': "Darah", 'marketing_channel': "Subway sign"}
        rv = self.app.post('api/flow/self_intake/contact_questionnaire', data=json.dumps(cq),
                           content_type="application/json",
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
        rv = self.app.post('api/flow/self_intake/contact_questionnaire', data=json.dumps(cq),
                           content_type="application/json",
                           follow_redirects=True, headers=headers)
        self.assert_success(rv)
        log = db.session.query(StepLog).all()
        self.assertIsNotNone(log)
        self.assertTrue(len(log) > 0)

    def test_clinical_diagnoses_questionnaire_basics(self):
        self.construct_clinical_diagnoses_questionnaire()
        cq = db.session.query(ClinicalDiagnosesQuestionnaire).first()
        self.assertIsNotNone(cq)
        cq_id = cq.id
        rv = self.app.get('/api/q/clinical_diagnoses_questionnaire/%i' % cq_id,
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], cq_id)
        self.assertEqual(response["medical"], cq.medical)
        self.assertEqual(response["genetic"], cq.genetic)

    def test_modify_clinical_diagnoses_questionnaire_basics(self):
        self.construct_clinical_diagnoses_questionnaire()
        cq = db.session.query(ClinicalDiagnosesQuestionnaire).first()
        self.assertIsNotNone(cq)
        cq_id = cq.id
        rv = self.app.get('/api/q/clinical_diagnoses_questionnaire/%i' % cq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['developmental'] = ['intellectual']
        response['mental_health'] = ['depression']
        response['medical'] = ['gastrointestinal']
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/clinical_diagnoses_questionnaire/%i' % cq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/clinical_diagnoses_questionnaire/%i' % cq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['developmental'], ['intellectual'])
        self.assertEqual(response['mental_health'], ['depression'])
        self.assertEqual(response['medical'], ['gastrointestinal'])
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_clinical_diagnoses_questionnaire(self):
        cq = self.construct_clinical_diagnoses_questionnaire()
        cq_id = cq.id
        rv = self.app.get('api/q/clinical_diagnoses_questionnaire/%i' % cq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/clinical_diagnoses_questionnaire/%i' % cq_id, content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/clinical_diagnoses_questionnaire/%i' % cq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_clinical_diagnoses_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        clinical_diagnoses_questionnaire = {'medical': ['seizure'], 'genetic': ['fragileX'], 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/clinical_diagnoses_questionnaire',
                           data=json.dumps(clinical_diagnoses_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['medical'], ['seizure'])
        self.assertEqual(response['genetic'], ['fragileX'])
        self.assertIsNotNone(response['id'])

    def test_contact_questionnaire_basics(self):
        self.construct_contact_questionnaire()
        cq = db.session.query(ContactQuestionnaire).first()
        self.assertIsNotNone(cq)
        cq_id = cq.id
        rv = self.app.get('/api/q/contact_questionnaire/%i' % cq_id,
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], cq_id)
        self.assertEqual(response["phone"], cq.phone)
        self.assertEqual(response["marketing_channel"], cq.marketing_channel)

    def test_modify_contact_questionnaire_basics(self):
        self.construct_contact_questionnaire()
        cq = db.session.query(ContactQuestionnaire).first()
        self.assertIsNotNone(cq)
        cq_id = cq.id
        rv = self.app.get('/api/q/contact_questionnaire/%i' % cq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['phone'] = '123-456-7890'
        response['zip'] = 22345
        response['marketing_channel'] = 'flyer'
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/contact_questionnaire/%i' % cq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/contact_questionnaire/%i' % cq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['phone'], '123-456-7890')
        self.assertEqual(response['zip'], 22345)
        self.assertEqual(response['marketing_channel'], 'flyer')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_contact_questionnaire(self):
        cq = self.construct_contact_questionnaire()
        cq_id = cq.id
        rv = self.app.get('api/q/contact_questionnaire/%i' % cq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/contact_questionnaire/%i' % cq_id, content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/contact_questionnaire/%i' % cq_id, content_type="application/json",
                          headers=self.logged_in_headers())
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
        self.assert_success(rv)
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
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], cbdq_id)
        self.assertEqual(response["concerning_behaviors"], cbdq.concerning_behaviors)
        self.assertEqual(response["has_academic_difficulties"], cbdq.has_academic_difficulties)

    def test_modify_current_behaviors_dependent_questionnaire_basics(self):
        self.construct_current_behaviors_dependent_questionnaire()
        cbdq = db.session.query(CurrentBehaviorsDependentQuestionnaire).first()
        self.assertIsNotNone(cbdq)
        cbdq_id = cbdq.id
        rv = self.app.get('/api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['dependent_verbal_ability'] = 'nonVerbal'
        response['concerning_behaviors'] = ['elopement']
        response['has_academic_difficulties'] = False
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['dependent_verbal_ability'], 'nonVerbal')
        self.assertEqual(response['concerning_behaviors'], ['elopement'])
        self.assertEqual(response['has_academic_difficulties'], False)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_current_behaviors_dependent_questionnaire(self):
        cbdq = self.construct_current_behaviors_dependent_questionnaire()
        cbdq_id = cbdq.id
        rv = self.app.get('api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id,
                             content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/current_behaviors_dependent_questionnaire/%i' % cbdq_id,
                          content_type="application/json", headers=self.logged_in_headers())
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
        self.assert_success(rv)
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
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], cbsq_id)
        self.assertEqual(response["has_academic_difficulties"], cbsq.has_academic_difficulties)

    def test_modify_current_behaviors_self_questionnaire_basics(self):
        self.construct_current_behaviors_self_questionnaire()
        cbsq = db.session.query(CurrentBehaviorsSelfQuestionnaire).first()
        self.assertIsNotNone(cbsq)
        cbsq_id = cbsq.id
        rv = self.app.get('/api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, content_type="application/json", headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['self_verbal_ability'] = ['nonVerbal']
        response['academic_difficulty_areas'] = ['math']
        response['has_academic_difficulties'] = False
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_verbal_ability'], ['nonVerbal'])
        self.assertEqual(response['academic_difficulty_areas'], ['math'])
        self.assertEqual(response['has_academic_difficulties'], False)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_current_behaviors_self_questionnaire(self):
        cbsq = self.construct_current_behaviors_self_questionnaire()
        cbsq_id = cbsq.id
        rv = self.app.get('api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/current_behaviors_self_questionnaire/%i' % cbsq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_current_behaviors_self_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        current_behaviors_self_questionnaire = {'self_verbal_ability': ['verbal', 'AACsystem'],
                                                'has_academic_difficulties': False, 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/current_behaviors_self_questionnaire',
                           data=json.dumps(current_behaviors_self_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_verbal_ability'], ['verbal', 'AACsystem'])
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
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], dq_id)
        self.assertEqual(response["birth_sex"], dq.birth_sex)
        self.assertEqual(response["gender_identity"], dq.gender_identity)

    def test_modify_demographics_questionnaire_basics(self):
        self.construct_demographics_questionnaire()
        dq = db.session.query(DemographicsQuestionnaire).first()
        self.assertIsNotNone(dq)
        dq_id = dq.id
        rv = self.app.get('/api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json", headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['gender_identity'] = 'genderOther'
        response['race_ethnicity'] = ['raceOther']
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/demographics_questionnaire/%i' % dq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['gender_identity'], 'genderOther')
        self.assertEqual(response['race_ethnicity'], ['raceOther'])
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_demographics_questionnaire(self):
        dq = self.construct_demographics_questionnaire()
        dq_id = dq.id
        rv = self.app.get('api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_demographics_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        demographics_questionnaire = {'birth_sex': "female", 'gender_identity': "genderOther", 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/demographics_questionnaire',
                           data=json.dumps(demographics_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assert_success(rv)
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
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], dq_id)
        self.assertEqual(response["had_birth_complications"], dq.had_birth_complications)
        self.assertEqual(response["when_motor_milestones"], dq.when_motor_milestones)

    def test_modify_developmental_questionnaire_basics(self):
        self.construct_developmental_questionnaire()
        dq = db.session.query(DevelopmentalQuestionnaire).first()
        self.assertIsNotNone(dq)
        dq_id = dq.id
        rv = self.app.get('/api/q/developmental_questionnaire/%i' % dq_id, content_type="application/json", headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['when_motor_milestones'] = 'notYet'
        response['when_language_milestones'] = 'notYet'
        response['when_toileting_milestones'] = 'early'
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/developmental_questionnaire/%i' % dq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/developmental_questionnaire/%i' % dq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['when_motor_milestones'], 'notYet')
        self.assertEqual(response['when_language_milestones'], 'notYet')
        self.assertEqual(response['when_toileting_milestones'], 'early')
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_developmental_questionnaire(self):
        dq = self.construct_developmental_questionnaire()
        dq_id = dq.id
        rv = self.app.get('api/q/developmental_questionnaire/%i' % dq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/developmental_questionnaire/%i' % dq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/developmental_questionnaire/%i' % dq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_developmental_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.dependent)
        headers = self.logged_in_headers(u)

        developmental_questionnaire = {'had_birth_complications': True, 'birth_complications_description': 'C-Section',
                                       'participant_id': p.id}
        rv = self.app.post('api/flow/dependent_intake/developmental_questionnaire',
                           data=json.dumps(developmental_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assert_success(rv)
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
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], eq_id)
        self.assertEqual(response["school_name"], eq.school_name)
        self.assertEqual(response["school_type"], eq.school_type)

    def test_modify_education_dependent_questionnaire_basics(self):
        self.construct_education_dependent_questionnaire()
        eq = db.session.query(EducationDependentQuestionnaire).first()
        self.assertIsNotNone(eq)
        eq_id = eq.id
        rv = self.app.get('/api/q/education_dependent_questionnaire/%i' % eq_id, content_type="application/json", headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['school_name'] = 'Sesame School'
        response['school_type'] = 'public'
        response['dependent_placement'] = 'vocational'
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/education_dependent_questionnaire/%i' % eq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/education_dependent_questionnaire/%i' % eq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['school_name'], 'Sesame School')
        self.assertEqual(response['school_type'], 'public')
        self.assertEqual(response['dependent_placement'], 'vocational')
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_education_dependent_questionnaire(self):
        eq = self.construct_education_dependent_questionnaire()
        eq_id = eq.id
        rv = self.app.get('api/q/education_dependent_questionnaire/%i' % eq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/education_dependent_questionnaire/%i' % eq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/education_dependent_questionnaire/%i' % eq_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_education_dependent_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        education_dependent_questionnaire = {'attends_school': True, 'school_name': 'Attreyu Academy',
                                             'participant_id': p.id}
        rv = self.app.post('api/flow/dependent_intake/education_dependent_questionnaire',
                           data=json.dumps(education_dependent_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assert_success(rv)
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
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], eq_id)
        self.assertEqual(response["school_name"], eq.school_name)
        self.assertEqual(response["school_type"], eq.school_type)

    def test_modify_education_self_questionnaire_basics(self):
        self.construct_education_self_questionnaire()
        eq = db.session.query(EducationSelfQuestionnaire).first()
        self.assertIsNotNone(eq)
        eq_id = eq.id
        rv = self.app.get('/api/q/education_self_questionnaire/%i' % eq_id, content_type="application/json", headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['school_name'] = 'Sesame School'
        response['school_type'] = 'public'
        response['self_placement'] = 'vocational'
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/education_self_questionnaire/%i' % eq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/education_self_questionnaire/%i' % eq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['school_name'], 'Sesame School')
        self.assertEqual(response['school_type'], 'public')
        self.assertEqual(response['self_placement'], 'vocational')
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_education_self_questionnaire(self):
        eq = self.construct_education_self_questionnaire()
        eq_id = eq.id
        rv = self.app.get('api/q/education_self_questionnaire/%i' % eq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/education_self_questionnaire/%i' % eq_id, content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/education_self_questionnaire/%i' % eq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_education_self_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        education_self_questionnaire = {'attends_school': True, 'school_name': 'Attreyu Academy',
                                        'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/education_self_questionnaire',
                           data=json.dumps(education_self_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assert_success(rv)
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
        self.assert_success(rv)
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
        rv = self.app.get('/api/q/employment_questionnaire/%i' % eq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['is_currently_employed'] = False
        response['employment_capacity'] = None
        response['has_employment_support'] = 'yes'
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/employment_questionnaire/%i' % eq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/employment_questionnaire/%i' % eq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['is_currently_employed'], False)
        self.assertEqual(response['employment_capacity'], None)
        self.assertEqual(response['has_employment_support'], 'yes')
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_employment_questionnaire(self):
        eq = self.construct_employment_questionnaire()
        eq_id = eq.id
        rv = self.app.get('api/q/employment_questionnaire/%i' % eq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/employment_questionnaire/%i' % eq_id, content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/employment_questionnaire/%i' % eq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_employment_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        employment_questionnaire = {'is_currently_employed': True, 'employment_capacity': 'partTime',
                                    'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/employment_questionnaire', data=json.dumps(employment_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assert_success(rv)
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
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], ehq_id)
        self.assertEqual(response["self_identifies_autistic"], ehq.self_identifies_autistic)
        self.assertEqual(response["years_old_at_first_diagnosis"], ehq.years_old_at_first_diagnosis)

    def test_modify_evaluation_history_dependent_questionnaire_basics(self):
        self.construct_evaluation_history_dependent_questionnaire()
        ehq = db.session.query(EvaluationHistoryDependentQuestionnaire).first()
        self.assertIsNotNone(ehq)
        ehq_id = ehq.id
        rv = self.app.get('/api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['self_identifies_autistic'] = False
        response['years_old_at_first_diagnosis'] = 12
        response['who_diagnosed'] = 'healthTeam'
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_identifies_autistic'], False)
        self.assertEqual(response['years_old_at_first_diagnosis'], 12)
        self.assertEqual(response['who_diagnosed'], 'healthTeam')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_evaluation_history_dependent_questionnaire(self):
        ehq = self.construct_evaluation_history_dependent_questionnaire()
        ehq_id = ehq.id
        rv = self.app.get('api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id,
                             content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/evaluation_history_dependent_questionnaire/%i' % ehq_id,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_evaluation_history_dependent_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_guardian)
        headers = self.logged_in_headers(u)

        evaluation_history_dependent_questionnaire = {'self_identifies_autistic': True,
                                                      'years_old_at_first_diagnosis': 5,
                                                      'participant_id': p.id}
        rv = self.app.post('api/flow/dependent_intake/evaluation_history_dependent_questionnaire',
                           data=json.dumps(evaluation_history_dependent_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assert_success(rv)
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
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], ehq_id)
        self.assertEqual(response["self_identifies_autistic"], ehq.self_identifies_autistic)
        self.assertEqual(response["years_old_at_first_diagnosis"], ehq.years_old_at_first_diagnosis)

    def test_modify_evaluation_history_self_questionnaire_basics(self):
        self.construct_evaluation_history_self_questionnaire()
        ehq = db.session.query(EvaluationHistorySelfQuestionnaire).first()
        self.assertIsNotNone(ehq)
        ehq_id = ehq.id
        rv = self.app.get('/api/q/evaluation_history_self_questionnaire/%i' % ehq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['self_identifies_autistic'] = False
        response['years_old_at_first_diagnosis'] = 12
        response['who_diagnosed'] = 'healthTeam'
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/evaluation_history_self_questionnaire/%i' % ehq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/evaluation_history_self_questionnaire/%i' % ehq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_identifies_autistic'], False)
        self.assertEqual(response['years_old_at_first_diagnosis'], 12)
        self.assertEqual(response['who_diagnosed'], 'healthTeam')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_evaluation_history_self_questionnaire(self):
        ehq = self.construct_evaluation_history_self_questionnaire()
        ehq_id = ehq.id
        rv = self.app.get('api/q/evaluation_history_self_questionnaire/%i' % ehq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/evaluation_history_self_questionnaire/%i' % ehq_id, content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/evaluation_history_self_questionnaire/%i' % ehq_id, content_type="application/json",
                          headers=self.logged_in_headers())
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
        self.assert_success(rv)
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
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
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
        rv = self.app.get('/api/q/home_dependent_questionnaire/%i' % hq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['participant_id'] = self.construct_participant(user=self.construct_user(),
                                                                relationship=Relationship.dependent).id
        response['dependent_living_situation'] = ['caregiver']
        response['struggle_to_afford'] = True
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/home_dependent_questionnaire/%i' % hq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        self.construct_housemate(name='Debbie Danger', home_dependent_questionnaire=hq)
        rv = self.app.get('/api/q/home_dependent_questionnaire/%i' % hq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['dependent_living_situation'], ['caregiver'])
        self.assertEqual(response['struggle_to_afford'], True)
        self.assertEqual(len(response['housemates']), 2)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_home_dependent_questionnaire(self):
        hq = self.construct_home_dependent_questionnaire()
        hq_id = hq.id
        rv = self.app.get('api/q/home_dependent_questionnaire/%i' % hq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/home_dependent_questionnaire/%i' % hq_id, content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/home_dependent_questionnaire/%i' % hq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_home_dependent_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        home_dependent_questionnaire = {'dependent_living_situation': ['family'], 'struggle_to_afford': False,
                                        'participant_id': p.id}
        rv = self.app.post('api/flow/dependent_intake/home_dependent_questionnaire',
                           data=json.dumps(home_dependent_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['participant_id'], p.id)
        self.assertEqual(response['dependent_living_situation'], ['family'])
        self.assertEqual(response['struggle_to_afford'], False)
        self.assertIsNotNone(response['id'])

    def test_home_self_questionnaire_basics(self):
        self.construct_home_self_questionnaire()
        hq = db.session.query(HomeSelfQuestionnaire).first()
        self.assertIsNotNone(hq)
        hq_id = hq.id
        rv = self.app.get('/api/q/home_self_questionnaire/%i' % hq_id,
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
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
        rv = self.app.get('/api/q/home_self_questionnaire/%i' % hq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['participant_id'] = self.construct_participant(user=self.construct_user(),
                                                                relationship=Relationship.self_participant).id
        response['self_living_situation'] = ['caregiver']
        response['struggle_to_afford'] = True
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/home_self_questionnaire/%i' % hq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        self.construct_housemate(name='Debbie Danger', home_self_questionnaire=hq)
        rv = self.app.get('/api/q/home_self_questionnaire/%i' % hq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_living_situation'], ['caregiver'])
        self.assertEqual(response['struggle_to_afford'], True)
        self.assertEqual(len(response['housemates']), 2)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_home_self_questionnaire(self):
        hq = self.construct_home_self_questionnaire()
        hq_id = hq.id
        rv = self.app.get('api/q/home_self_questionnaire/%i' % hq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/home_self_questionnaire/%i' % hq_id, content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/home_self_questionnaire/%i' % hq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_home_self_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        home_self_questionnaire = {'self_living_situation': ['family'], 'struggle_to_afford': False,
                                   'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/home_self_questionnaire',
                           data=json.dumps(home_self_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['participant_id'], p.id)
        self.assertEqual(response['self_living_situation'], ['family'])
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
        self.assert_success(rv)
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
        rv = self.app.get('/api/q/identification_questionnaire/%i' % iq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['first_name'] = 'Helga'
        response['birth_city'] = 'Staunton'
        response['is_first_name_preferred'] = True
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/identification_questionnaire/%i' % iq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/q/identification_questionnaire/%i' % iq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['first_name'], 'Helga')
        self.assertEqual(response['birth_city'], 'Staunton')
        self.assertEqual(response['is_first_name_preferred'], True)
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_identification_questionnaire(self):
        iq = self.construct_identification_questionnaire()
        iq_id = iq.id
        rv = self.app.get('api/q/identification_questionnaire/%i' % iq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/identification_questionnaire/%i' % iq_id, content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/identification_questionnaire/%i' % iq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_identification_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        headers = self.logged_in_headers(u)

        identification_questionnaire = {'first_name': 'Eloise', 'middle_name': 'Elora', 'participant_id': p.id}
        rv = self.app.post('api/flow/self_intake/identification_questionnaire',
                           data=json.dumps(identification_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assert_success(rv)
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
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
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
        rv = self.app.get('/api/q/supports_questionnaire/%i' % sq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        response['participant_id'] = self.construct_participant(user=self.construct_user(),
                                                                relationship=Relationship.self_participant).id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/supports_questionnaire/%i' % sq_id, data=json.dumps(response),
                          content_type="application/json",
                          follow_redirects=True,
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        self.construct_medication(name='Iocane Powder', supports_questionnaire=sq)
        self.construct_therapy(type='socialSkills', supports_questionnaire=sq)
        self.construct_alternative_augmentative(type='highTechAAC', supports_questionnaire=sq)
        self.construct_assistive_device(type_group='hearing', type='hearingAid', notes='Your ears you keep and I\'ll tell you why.', supports_questionnaire=sq)
        rv = self.app.get('/api/q/supports_questionnaire/%i' % sq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response['medications']), 2)
        self.assertEqual(len(response['therapies']), 2)
        self.assertEqual(len(response['alternative_augmentative']), 2)
        self.assertEqual(len(response['assistive_devices']), 2)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_supports_questionnaire(self):
        sq = self.construct_supports_questionnaire()
        sq_id = sq.id
        rv = self.app.get('api/q/supports_questionnaire/%i' % sq_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/q/supports_questionnaire/%i' % sq_id, content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/q/supports_questionnaire/%i' % sq_id, content_type="application/json",
                          headers=self.logged_in_headers())
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
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['participant_id'], p.id)
        self.assertIsNotNone(response['id'])

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
                self.assertEqual(i['steps'][8]['label'], 'Employment')
            if i['name'] == 'dependent_intake':
                self.assertEqual(len(i['steps']), 9)
                self.assertEqual(i['steps'][5]['name'], 'developmental_questionnaire')
                self.assertEqual(i['steps'][5]['label'], 'Birth and Developmental History')
            if i['name'] == 'guardian_intake':
                self.assertEqual(len(i['steps']), 3)
                self.assertEqual(i['steps'][1]['name'], 'contact_questionnaire')
                self.assertEqual(i['steps'][1]['label'], 'Contact Information')

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
        rv = self.app.post('api/flow/self_intake/identification_questionnaire', data=json.dumps(cq),
                           content_type="application/json",
                           follow_redirects=True, headers=headers)

        rv = self.app.get('api/flow/self_intake/%i' % p.id, content_type="application/json", headers=headers)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual('identification_questionnaire', response['steps'][0]['name'])
        self.assertEqual(Step.STATUS_COMPLETE, response['steps'][0]['status'])
        self.assertIsNotNone(response['steps'][0]['date_completed'])

    def test_questionnaire_meta_is_relation_specific(self):
        self.construct_identification_questionnaire()
        rv = self.app.get('/api/flow/self_intake/identification_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        intro = self.get_field_from_response(response, "intro")
        self.assertIsNotNone(intro["template_options"]["description"])
        self.assertEqual(intro["template_options"]["description"],
                         "Please answer the following questions about yourself (* indicates required response):")

        birth_city = self.get_field_from_response(response, "birth_city")
        self.assertIsNotNone(birth_city)
        self.assertIsNotNone(birth_city["template_options"])
        self.assertIsNotNone(birth_city["template_options"]["label"])
        self.assertEqual(birth_city["template_options"]["label"],
                         "Your city/municipality of birth")

        rv = self.app.get('/api/flow/dependent_intake/identification_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        birth_city = self.get_field_from_response(response, "birth_city")
        self.assertIsNotNone(birth_city["template_options"]["label"])
        self.assertEqual(birth_city["template_options"]["label"],
                         "Your child's city/municipality of birth")

    def test_questionnaire_meta_has_relation_required_fields(self):
        self.construct_identification_questionnaire()
        rv = self.app.get('/api/flow/dependent_intake/identification_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        relationship = self.get_field_from_response(response, "relationship")
        self.assertIsNotNone(relationship)

        # Convert Participant to a dependant
        rv = self.app.get('/api/flow/self_intake/identification_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        relationship = self.get_field_from_response(response, "relationship")
        self.assertIsNone(relationship)

    def test_meta_contains_table_details(self):
        self.construct_identification_questionnaire()
        rv = self.app.get('/api/flow/dependent_intake/identification_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual("identifying", response["table"]["question_type"])
        self.assertEqual("Identification", response["table"]["label"])

    def test_meta_field_groups_contain_their_fields(self):
        self.construct_home_self_questionnaire()
        rv = self.app.get('/api/flow/self_intake/home_self_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self_living = self.get_field_from_response(response, "self_living")
        self.assertEqual("self_living_situation", self_living["fieldGroup"][0]["name"])

    def test_support_meta_contain_their_fields(self):
        self.construct_supports_questionnaire()
        rv = self.app.get('/api/flow/self_intake/supports_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        assistive_devices = self.get_field_from_response(response, "assistive_devices")
        self.assertIsNotNone(assistive_devices["fieldArray"]["fieldGroup"][0])
        self.assertEqual("type", assistive_devices["fieldArray"]["fieldGroup"][0]["name"])

    def test_evaluation_history_dependent_meta_contain_their_fields(self):
        self.construct_evaluation_history_dependent_questionnaire()
        rv = self.app.get('/api/flow/dependent_intake/evaluation_history_dependent_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response["fields"]), 10)

    def test_evaluation_history_self_meta_contain_their_fields(self):
        self.construct_evaluation_history_self_questionnaire()
        rv = self.app.get('/api/flow/self_intake/evaluation_history_self_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response["fields"]), 10)

    def test_education_dependent_meta_contain_their_fields(self):
        self.construct_education_dependent_questionnaire()
        rv = self.app.get('/api/flow/dependent_intake/education_dependent_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response["fields"]), 5)

    def test_education_self_meta_contain_their_fields(self):
        self.construct_education_self_questionnaire()
        rv = self.app.get('/api/flow/self_intake/education_self_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(response["fields"]), 5)

    def test_meta_fields_are_ordered(self):
        self.construct_education_self_questionnaire()
        rv = self.app.get('/api/flow/self_intake/education_self_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["fields"][0]["display_order"])
        self.assertEqual(2, response["fields"][1]["display_order"])
        self.assertEqual(3, response["fields"][2]["display_order"])

        self.assertEqual(6.1, response['fields'][4]["fieldGroup"][0]["display_order"])
        self.assertEqual(6.2, response['fields'][4]["fieldGroup"][1]["display_order"])

    def test_questionnaire_names_list_basics(self):
        rv = self.app.get('/api/q',
                          follow_redirects=True,
                          content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual("assistive_device", response[1])
        self.assertEqual("education_dependent_questionnaire", response[8])
        self.assertEqual("home_self_questionnaire", response[14])
        self.assertEqual("therapy", response[20])
        self.assertEqual(21, len(response))

    def test_questionnaire_list_meta_basics(self):
        self.construct_education_self_questionnaire()
        rv = self.app.get('/api/q/education_self_questionnaire/meta',
                          follow_redirects=True,
                          content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(list(filter(lambda field: field['name'] == 'id', response["fields"]))))
        self.assertEqual(1, len(list(filter(lambda field: field['name'] == 'user_id', response["fields"]))))
        self.assertEqual(1, len(list(filter(lambda field: field['name'] == 'school_type', response["fields"]))))
        self.assertEqual(1, len(list(filter(lambda field: field['name'] == 'school_services_other', response["fields"]))))
        self.assertEqual(13, len(response["fields"]))

    def test_questionnaire_list_basics(self):
        q = self.construct_current_behaviors_dependent_questionnaire()
        rv = self.app.get('/api/q/current_behaviors_dependent_questionnaire',
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(["math", "writing"], response[0]["academic_difficulty_areas"])
        self.assertEqual("fluent", response[0]["dependent_verbal_ability"])
        self.assertEqual(q.id, response[0]["id"])

    def test_non_admin_cannot_view_questionnaire_list(self):
        user = self.construct_user(email='regularUser@user.com')
        admin = self.construct_admin_user(email='adminUser@user.com')
        self.construct_contact_questionnaire()
        rv = self.app.get('/api/q/contact_questionnaire', content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.app.get('/api/q/contact_questionnaire', content_type="application/json", headers=self.logged_in_headers(user=user))
        self.assertEqual(403, rv.status_code)
        rv = self.app.get('/api/q/contact_questionnaire', content_type="application/json", headers=self.logged_in_headers(user=admin))
        self.assert_success(rv)

    def test_export_single_questionnaire(self):
        self.construct_current_behaviors_dependent_questionnaire()
        rv = self.app.get('/api/q/current_behaviors_dependent_questionnaire/export',
                          follow_redirects=True,
                          content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        wb = openpyxl.load_workbook(io.BytesIO(rv.data))
        ws = wb.get_active_sheet()
        self.assertEqual(ws, wb.active)
        self.assertEqual('id', ws['A1'].value)
        self.assertEqual('last_updated', ws['B1'].value)
        self.assertEqual('participant_id', ws['C1'].value)
        self.assertEqual('user_id', ws['D1'].value)
        self.assertEqual('dependent_verbal_ability', ws['E1'].value)
        self.assertEqual('concerning_behaviors', ws['F1'].value)
        self.assertEqual('hoarding, ', ws['F2'].value)
        self.assertEqual('concerning_behaviors_other', ws['G1'].value)
        self.assertEqual('has_academic_difficulties', ws['H1'].value)
        self.assertEqual('academic_difficulty_areas', ws['I1'].value)
        self.assertEqual('math, writing, ', ws['I2'].value)
        self.assertEqual('academic_difficulty_other', ws['J1'].value)
        self.assertEqual(10, ws.max_column)
        self.assertEqual(2, ws.max_row)

    def test_export_all_questionnaires(self):
        self.construct_all_questionnaires()
        rv = self.app.get('/api/q/all/export', follow_redirects=True,
                          content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        wb = openpyxl.load_workbook(io.BytesIO(rv.data))
        ws = wb.get_active_sheet()
        self.assertEqual(ws, wb.active)
        self.assertEqual(2, ws.max_row)
        self.assertEqual(21, len(wb.worksheets))
        self.assertEqual('alternative_augmentative', wb.worksheets[0].title)
        self.assertEqual('assistive_device', wb.worksheets[1].title)
        self.assertEqual('clinical_diagnoses_questionnai', wb.worksheets[2].title)
        self.assertEqual('contact_questionnaire', wb.worksheets[3].title)
        self.assertEqual('current_behaviors_dependent_qu', wb.worksheets[4].title)
        self.assertEqual('current_behaviors_self_questio', wb.worksheets[5].title)
        self.assertEqual('demographics_questionnaire', wb.worksheets[6].title)
        self.assertEqual('developmental_questionnaire', wb.worksheets[7].title)
        self.assertEqual('education_dependent_questionna', wb.worksheets[8].title)
        self.assertEqual('education_self_questionnaire', wb.worksheets[9].title)
        self.assertEqual('employment_questionnaire', wb.worksheets[10].title)
        self.assertEqual('evaluation_history_dependent_q', wb.worksheets[11].title)
        self.assertEqual('evaluation_history_self_questi', wb.worksheets[12].title)
        self.assertEqual('home_dependent_questionnaire', wb.worksheets[13].title)
        self.assertEqual('home_self_questionnaire', wb.worksheets[14].title)
        self.assertEqual('housemate', wb.worksheets[15].title)
        self.assertEqual('identification_questionnaire', wb.worksheets[16].title)
        self.assertEqual('medication', wb.worksheets[17].title)
        self.assertEqual('professional_profile_questionn', wb.worksheets[18].title)
        self.assertEqual('supports_questionnaire', wb.worksheets[19].title)
        self.assertEqual('therapy', wb.worksheets[20].title)
