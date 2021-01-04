import json
import random
import string
import unittest
from datetime import datetime

from dateutil import parser
import openpyxl
import io

from data_loader import DataLoader
from tests.base_test import BaseTest
from app import db, app, elastic_index
from app.export_service import ExportService
from app.model.flow import Step
from app.model.participant import Participant, Relationship
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
from app.model.questionnaires.registration_questionnaire import RegistrationQuestionnaire
from app.model.chain_step import ChainStep
from app.model.questionnaires.chain_questionnaire import ChainQuestionnaire
from app.model.questionnaires.chain_session import ChainSession
from app.model.questionnaires.chain_session_step import ChainSessionStep
from app.model.questionnaires.supports_questionnaire import SupportsQuestionnaire
from app.model.questionnaires.therapy import Therapy
from app.model.resource_category import ResourceCategory
from app.model.step_log import StepLog
from app.model.user import User, Role


class BaseTestQuestionnaire(BaseTest):
    """Tools for building questionnaires of all types and descriptions."""

    def randomString(self):
        char_set = string.ascii_uppercase + string.digits
        return ''.join(random.sample(char_set * 6, 6))

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

        db_ad = db.session.query(AssistiveDevice).filter_by(id=ad.id).first()
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

    def construct_registration_questionnaire(self, first_name='Nora', last_name='Bora', email='nora@bora.com',
                                             zip_code=24401, relationship_to_autism=None, marketing_channel=None,
                                             user=None, event=None):

        rq = RegistrationQuestionnaire(first_name=first_name, last_name=last_name, email=email, zip_code=zip_code,
                                       relationship_to_autism=relationship_to_autism,
                                       marketing_channel=marketing_channel)

        if marketing_channel is None:
            rq.marketing_channel = ['drive', 'facebook']
        if relationship_to_autism is None:
            rq.relationship_to_autism = ['self', 'professional']

        if user is None:
            u = self.construct_user(email='nora@bora.com')
            rq.user_id = u.id
        else:
            u = user
            rq.user_id = u.id

        if event is None:
            rq.event_id = self.construct_event(title='Webinar: You have to be here (virtually)').id
        else:
            rq.event_id = event.id

        db.session.add(rq)
        db.session.commit()

        db_rq = db.session.query(RegistrationQuestionnaire).filter_by(user_id=rq.user_id).first()
        self.assertEqual(db_rq.email, rq.email)
        return db_rq

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

    def construct_chain_session_questionnaire(self, participant=None, user=None):
        self.construct_chain_steps()

        bq = ChainQuestionnaire()
        if user is None:
            u = self.construct_user(email='edudep@questionnaire.com', role=Role.researcher)
            bq.user_id = u.id
        else:
            u = user
            bq.user_id = u.id

        if participant is None:
            p = self.construct_participant(user=u, relationship=Relationship.dependent)
            bq.participant_id = p.id
        else:
            p = participant
            bq.participant_id = p.id


        session_1_step_1 = ChainSessionStep(
            date=parser.parse("2020-12-14T17:46:14.030Z"),
            chain_step_id=0,
            status="focus",
            completed=False,
            was_prompted=True,
            prompt_level="partial_physical",
            had_challenging_behavior=True,
            challenging_behavior_severity="moderate"
        )
        session_1 = ChainSession()
        session_1.step_attempts = [session_1_step_1]
        bq.sessions = [session_1]

        db.session.add(bq)
        db.session.commit()

        db_bq = db.session.query(ChainQuestionnaire).filter_by(participant_id=bq.participant_id).first()
        self.assertEqual(db_bq.participant_id, bq.participant_id)
        self.assertEqual(db_bq.user_id, bq.user_id)
        self.assertEqual(db_bq.sessions, bq.sessions)
        return db_bq

    def construct_all_questionnaires(self, user=None):
        if user is None:
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
        self.construct_registration_questionnaire(user=user)
        self.construct_chain_session_questionnaire(user=user, participant=participant)

