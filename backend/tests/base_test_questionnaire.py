import random
import string

from dateutil import parser
from sqlalchemy import cast, Integer

from app.models import Participant
from tests.base_test import BaseTest


class BaseTestQuestionnaire(BaseTest):
    """Tools for building questionnaires of all types and descriptions."""

    def randomString(self):
        char_set = string.ascii_uppercase + string.digits
        return "".join(random.sample(char_set * 6, 6))

    def get_field_from_response(self, response, name):
        for field in response["fields"]:
            if field["name"] == name:
                return field

    def construct_admin_user(self, email="rmond@virginia.gov"):
        from app.models import User
        from app.enums import Role

        user = User(email=email, role=Role.admin)
        self.session.add(user)
        self.session.commit()

        db_user = self.session.query(User).filter_by(email=user.email).first()
        self.assertEqual(db_user.role, user.role)
        return db_user

    def construct_assistive_device(
        self,
        type_group="mobility",
        type="prosthetic",
        timeframe="current",
        notes="I love my new leg!",
        supports_questionnaire=None,
    ):
        from app.models import AssistiveDevice

        ad = AssistiveDevice(type=type, timeframe=timeframe, notes=notes)
        if supports_questionnaire is not None:
            ad.supports_questionnaire_id = supports_questionnaire.id

        self.session.add(ad)
        self.session.commit()

        db_ad = self.session.query(AssistiveDevice).filter_by(id=ad.id).first()
        self.assertEqual(db_ad.notes, ad.notes)
        self.assertEqual(db_ad.type_group, ad.type_group)
        self.assertEqual(db_ad.type, ad.type)
        return db_ad

    def construct_alternative_augmentative(
        self, type="lowTechAAC", timeframe="current", notes="We use pen and paper", supports_questionnaire=None
    ):

        from app.models import AlternativeAugmentative

        aac = AlternativeAugmentative(type=type, timeframe=timeframe, notes=notes)
        if supports_questionnaire is not None:
            aac.supports_questionnaire_id = supports_questionnaire.id

        self.session.add(aac)
        self.session.commit()

        db_aac = self.session.query(AlternativeAugmentative).filter_by(last_updated=aac.last_updated).first()
        self.assertEqual(db_aac.notes, aac.notes)
        return db_aac

    def construct_clinical_diagnoses_questionnaire(
        self,
        developmental=None,
        mental_health=None,
        medical=None,
        genetic=None,
        participant=None,
        user=None,
    ):
        developmental = ["speechLanguage"] if developmental is None else developmental
        mental_health = ["ocd"] if mental_health is None else mental_health
        medical = ["insomnia"] if medical is None else medical
        genetic = ["corneliaDeLange"] if genetic is None else genetic

        from app.models import ClinicalDiagnosesQuestionnaire

        cdq = ClinicalDiagnosesQuestionnaire(
            developmental=developmental, mental_health=mental_health, medical=medical, genetic=genetic
        )
        if user is None:
            u = self.construct_user(email="clinic@questionnaire.com")
            cdq.user_id = u.id
        else:
            u = user
            cdq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            cdq.participant_id = self.construct_participant(user_id=u.id, relationship=Relationship.dependent).id
        else:
            cdq.participant_id = participant.id

        self.session.add(cdq)
        self.session.commit()

        db_cdq = (
            self.session.query(ClinicalDiagnosesQuestionnaire).filter_by(user_id=cast(cdq.user_id, Integer)).first()
        )
        self.assertEqual(db_cdq.participant_id, cdq.participant_id)
        return db_cdq

    def construct_contact_questionnaire(
        self, phone="123-456-7890", zip=55678, marketing_channel="Zine Ad", participant=None, user=None
    ):

        from app.models import ContactQuestionnaire

        cq = ContactQuestionnaire(phone=phone, zip=zip, marketing_channel=marketing_channel)
        if user is None:
            u = self.construct_user(email="contact@questionnaire.com")
            cq.user_id = u.id
        else:
            u = user
            cq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            cq.participant_id = self.construct_participant(user_id=u.id, relationship=Relationship.dependent).id
        else:
            cq.participant_id = participant.id

        self.session.add(cq)
        self.session.commit()

        db_cq = self.session.query(ContactQuestionnaire).filter_by(zip=cq.zip).first()
        self.assertEqual(db_cq.phone, cq.phone)
        return db_cq

    def construct_current_behaviors_dependent_questionnaire(
        self,
        dependent_verbal_ability="fluent",
        concerning_behaviors=None,
        has_academic_difficulties=True,
        academic_difficulty_areas=None,
        participant=None,
        user=None,
    ):
        concerning_behaviors = ["hoarding"] if concerning_behaviors is None else concerning_behaviors
        academic_difficulty_areas = (
            ["math", "writing"] if academic_difficulty_areas is None else academic_difficulty_areas
        )

        from app.models import CurrentBehaviorsDependentQuestionnaire

        cb = CurrentBehaviorsDependentQuestionnaire(
            dependent_verbal_ability=dependent_verbal_ability,
            concerning_behaviors=concerning_behaviors,
            has_academic_difficulties=has_academic_difficulties,
            academic_difficulty_areas=academic_difficulty_areas,
        )
        if user is None:
            u = self.construct_user(email="cbd@questionnaire.com")
            cb.user_id = u.id
        else:
            u = user
            cb.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            p = self.construct_participant(user_id=u.id, relationship=Relationship.dependent)
            cb.participant_id = p.id
        else:
            p = participant
            cb.participant_id = p.id

        self.session.add(cb)
        self.session.commit()

        db_cbd = (
            self.session.query(CurrentBehaviorsDependentQuestionnaire)
            .filter_by(participant_id=cast(cb.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_cbd.concerning_behaviors, cb.concerning_behaviors)
        return db_cbd

    def construct_current_behaviors_self_questionnaire(
        self,
        self_verbal_ability="verbal",
        has_academic_difficulties=True,
        academic_difficulty_areas="math",
        participant=None,
        user=None,
    ):

        from app.models import CurrentBehaviorsSelfQuestionnaire

        cb = CurrentBehaviorsSelfQuestionnaire(
            self_verbal_ability=self_verbal_ability,
            has_academic_difficulties=has_academic_difficulties,
            academic_difficulty_areas=academic_difficulty_areas,
        )
        if user is None:
            u = self.construct_user(email="cbs@questionnaire.com")
            cb.user_id = u.id
        else:
            u = user
            cb.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            p = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant)
            cb.participant_id = p.id
        else:
            p = participant
            cb.participant_id = p.id

        self.session.add(cb)
        self.session.commit()

        db_cb = (
            self.session.query(CurrentBehaviorsSelfQuestionnaire)
            .filter_by(participant_id=cast(cb.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_cb.academic_difficulty_areas, cb.academic_difficulty_areas)
        return db_cb

    def construct_demographics_questionnaire(
        self, birth_sex="intersex", gender_identity="intersex", race_ethnicity="raceBlack", participant=None, user=None
    ):

        from app.models import DemographicsQuestionnaire

        dq = DemographicsQuestionnaire(
            birth_sex=birth_sex, gender_identity=gender_identity, race_ethnicity=race_ethnicity
        )
        if user is None:
            u = self.construct_user(email="demograph@questionnaire.com")
            dq.user_id = u.id
        else:
            u = user
            dq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            dq.participant_id = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant).id
        else:
            dq.participant_id = participant.id

        self.session.add(dq)
        self.session.commit()

        db_dq = self.session.query(DemographicsQuestionnaire).filter_by(birth_sex=dq.birth_sex).first()
        self.assertEqual(db_dq.gender_identity, dq.gender_identity)
        return db_dq

    def construct_developmental_questionnaire(
        self,
        had_birth_complications=False,
        when_motor_milestones="delayed",
        when_language_milestones="early",
        when_toileting_milestones="notYet",
        participant=None,
        user=None,
    ):

        from app.models import DevelopmentalQuestionnaire

        dq = DevelopmentalQuestionnaire(
            had_birth_complications=had_birth_complications,
            when_motor_milestones=when_motor_milestones,
            when_language_milestones=when_language_milestones,
            when_toileting_milestones=when_toileting_milestones,
        )
        if user is None:
            u = self.construct_user(email="develop@questionnaire.com")
            dq.user_id = u.id
        else:
            u = user
            dq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            dq.participant_id = self.construct_participant(user_id=u.id, relationship=Relationship.dependent).id
        else:
            dq.participant_id = participant.id

        self.session.add(dq)
        self.session.commit()

        db_dq = (
            self.session.query(DevelopmentalQuestionnaire)
            .filter_by(participant_id=cast(dq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_dq.when_language_milestones, dq.when_language_milestones)
        return db_dq

    def construct_education_dependent_questionnaire(
        self,
        attends_school=True,
        school_name="Harvard",
        school_type="privateSchool",
        dependent_placement="graduate",
        participant=None,
        user=None,
    ):

        from app.models import EducationDependentQuestionnaire

        eq = EducationDependentQuestionnaire(
            attends_school=attends_school,
            school_name=school_name,
            school_type=school_type,
            dependent_placement=dependent_placement,
        )
        if user is None:
            u = self.construct_user(email="edudep@questionnaire.com")
            eq.user_id = u.id
        else:
            u = user
            eq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            p = self.construct_participant(user_id=u.id, relationship=Relationship.dependent)
            eq.participant_id = p.id
        else:
            p = participant
            eq.participant_id = p.id

        self.session.add(eq)
        self.session.commit()

        db_eq = (
            self.session.query(EducationDependentQuestionnaire)
            .filter_by(participant_id=cast(eq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_eq.school_name, eq.school_name)
        return db_eq

    def construct_education_self_questionnaire(
        self,
        attends_school=True,
        school_name="Harvard",
        school_type="privateSchool",
        self_placement="graduate",
        participant=None,
        user=None,
    ):

        from app.models import EducationSelfQuestionnaire

        eq = EducationSelfQuestionnaire(
            attends_school=attends_school,
            school_name=school_name,
            school_type=school_type,
            self_placement=self_placement,
        )

        if user is None:
            u = self.construct_user(email="eduself@questionnaire.com")
            eq.user_id = u.id
        else:
            u = user
            eq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            p = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant)
            eq.participant_id = p.id
        else:
            p = participant
            eq.participant_id = p.id

        self.session.add(eq)
        self.session.commit()

        db_eq = (
            self.session.query(EducationSelfQuestionnaire)
            .filter_by(participant_id=cast(eq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_eq.school_name, eq.school_name)
        return db_eq

    def construct_employment_questionnaire(
        self,
        is_currently_employed=True,
        employment_capacity="fullTime",
        has_employment_support=False,
        participant=None,
        user=None,
    ):

        from app.models import EmploymentQuestionnaire

        eq = EmploymentQuestionnaire(
            is_currently_employed=is_currently_employed,
            employment_capacity=employment_capacity,
            has_employment_support=has_employment_support,
        )
        if user is None:
            u = self.construct_user(email="employ@questionnaire.com")
            eq.user_id = u.id
        else:
            u = user
            eq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            eq.participant_id = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant).id
        else:
            eq.participant_id = participant.id

        self.session.add(eq)
        self.session.commit()

        db_eq = (
            self.session.query(EmploymentQuestionnaire)
            .filter_by(participant_id=cast(eq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_eq.employment_capacity, eq.employment_capacity)
        return db_eq

    def construct_evaluation_history_dependent_questionnaire(
        self,
        self_identifies_autistic=True,
        has_autism_diagnosis=True,
        years_old_at_first_diagnosis=7,
        who_diagnosed="pediatrician",
        participant=None,
        user=None,
    ):

        from app.models import (
            EvaluationHistoryDependentQuestionnaire,
        )

        ehq = EvaluationHistoryDependentQuestionnaire(
            self_identifies_autistic=self_identifies_autistic,
            has_autism_diagnosis=has_autism_diagnosis,
            years_old_at_first_diagnosis=years_old_at_first_diagnosis,
            who_diagnosed=who_diagnosed,
        )
        if user is None:
            u = self.construct_user(email="evaldep@questionnaire.com")
            ehq.user_id = u.id
        else:
            u = user
            ehq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            p = self.construct_participant(user_id=u.id, relationship=Relationship.dependent)
            ehq.participant_id = p.id
        else:
            p = participant
            ehq.participant_id = p.id

        self.session.add(ehq)
        self.session.commit()

        db_ehq = (
            self.session.query(EvaluationHistoryDependentQuestionnaire)
            .filter_by(participant_id=cast(ehq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_ehq.who_diagnosed, ehq.who_diagnosed)
        return db_ehq

    def construct_evaluation_history_self_questionnaire(
        self,
        self_identifies_autistic=True,
        has_autism_diagnosis=True,
        years_old_at_first_diagnosis=7,
        who_diagnosed="pediatrician",
        participant=None,
        user=None,
    ):

        from app.models import EvaluationHistorySelfQuestionnaire

        ehq = EvaluationHistorySelfQuestionnaire(
            self_identifies_autistic=self_identifies_autistic,
            has_autism_diagnosis=has_autism_diagnosis,
            years_old_at_first_diagnosis=years_old_at_first_diagnosis,
            who_diagnosed=who_diagnosed,
        )
        if user is None:
            u = self.construct_user(email="evalself@questionnaire.com")
            ehq.user_id = u.id
        else:
            u = user
            ehq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            p = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant)
            ehq.participant_id = p.id
        else:
            p = participant
            ehq.participant_id = p.id

        self.session.add(ehq)
        self.session.commit()

        db_ehq = (
            self.session.query(EvaluationHistorySelfQuestionnaire)
            .filter_by(participant_id=cast(ehq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_ehq.who_diagnosed, ehq.who_diagnosed)
        return db_ehq

    def construct_home_dependent_questionnaire(
        self,
        dependent_living_situation="fullTimeGuardian",
        housemates=None,
        struggle_to_afford=False,
        participant=None,
        user=None,
    ):

        from app.models import HomeDependentQuestionnaire

        hq = HomeDependentQuestionnaire(
            dependent_living_situation=[dependent_living_situation], struggle_to_afford=struggle_to_afford
        )

        if user is None:
            u = self.construct_user(email="homedep@questionnaire.com")
            hq.user_id = u.id
        else:
            u = user
            hq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            p = self.construct_participant(user_id=u.id, relationship=Relationship.dependent)
            hq.participant_id = p.id
        else:
            p = participant
            hq.participant_id = p.id

        self.session.add(hq)
        self.session.commit()

        if housemates is None:
            self.construct_housemate(home_dependent_questionnaire=hq)
        else:
            hq.housemates = housemates

        db_hq = (
            self.session.query(HomeDependentQuestionnaire)
            .filter_by(participant_id=cast(hq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_hq.dependent_living_situation, hq.dependent_living_situation)
        return db_hq

    def construct_home_self_questionnaire(
        self, self_living_situation="alone", housemates=None, struggle_to_afford=False, participant=None, user=None
    ):

        from app.models import HomeSelfQuestionnaire

        hq = HomeSelfQuestionnaire(self_living_situation=[self_living_situation], struggle_to_afford=struggle_to_afford)

        if user is None:
            u = self.construct_user(email="homeself@questionnaire.com")
            hq.user_id = u.id
        else:
            u = user
            hq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            p = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant)
            hq.participant_id = p.id
        else:
            p = participant
            hq.participant_id = p.id

        self.session.add(hq)
        self.session.commit()

        if housemates is None:
            self.construct_housemate(home_self_questionnaire=hq)
        else:
            hq.housemates = housemates

        db_hq = (
            self.session.query(HomeSelfQuestionnaire).filter_by(participant_id=cast(hq.participant_id, Integer)).first()
        )
        self.assertEqual(db_hq.self_living_situation, hq.self_living_situation)
        return db_hq

    def construct_housemate(
        self,
        name="Fred Fredly",
        relationship="bioSibling",
        age=23,
        has_autism=True,
        home_dependent_questionnaire=None,
        home_self_questionnaire=None,
    ):

        from app.models import Housemate

        h_dict = {"name": name, "relationship": relationship, "age": age, "has_autism": has_autism}
        if home_dependent_questionnaire is not None:
            h_dict["home_dependent_questionnaire_id"] = home_dependent_questionnaire.id
        if home_self_questionnaire is not None:
            h_dict["home_self_questionnaire_id"] = home_self_questionnaire.id
        h = Housemate(**h_dict)

        self.session.add(h)
        self.session.commit()
        h_id = h.id
        expected_rel = h.relationship
        self.session.close()

        db_h = self.session.query(Housemate).filter_by(id=h_id).first()
        self.assertEqual(db_h.relationship, expected_rel)
        return db_h

    def construct_identification_questionnaire(
        self,
        relationship_to_participant="adoptFather",
        first_name="Karl",
        is_first_name_preferred=False,
        nickname="Big K",
        birth_state="VA",
        is_english_primary=False,
        participant=None,
        user=None,
    ):

        from app.models import IdentificationQuestionnaire

        iq = IdentificationQuestionnaire(
            relationship_to_participant=relationship_to_participant,
            first_name=first_name,
            is_first_name_preferred=is_first_name_preferred,
            nickname=nickname,
            birth_state=birth_state,
            is_english_primary=is_english_primary,
        )
        if user is None:
            u = self.construct_user(email="ident@questionnaire.com")
            iq.user_id = u.id
        else:
            u = user
            iq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            iq.participant_id = self.construct_participant(user_id=u.id, relationship=Relationship.dependent).id
        else:
            iq.participant_id = participant.id

        self.session.add(iq)
        self.session.commit()

        db_iq = (
            self.session.query(IdentificationQuestionnaire)
            .filter_by(participant_id=cast(iq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_iq.nickname, iq.nickname)
        return db_iq

    def construct_professional_questionnaire(
        self,
        purpose="profResearch",
        professional_identity=None,
        professional_identity_other="Astronaut",
        learning_interests=None,
        learning_interests_other="Data plotting using dried fruit",
        currently_work_with_autistic=True,
        previous_work_with_autistic=False,
        length_work_with_autistic="3 minutes",
        participant=None,
        user=None,
    ):
        professional_identity = ["artTher", "profOther"] if professional_identity is None else professional_identity
        learning_interests = ["insuranceCov", "learnOther"] if learning_interests is None else learning_interests
        from app.models import ProfessionalProfileQuestionnaire

        pq = ProfessionalProfileQuestionnaire(
            purpose=purpose,
            professional_identity=professional_identity,
            professional_identity_other=professional_identity_other,
            learning_interests=learning_interests,
            learning_interests_other=learning_interests_other,
            currently_work_with_autistic=currently_work_with_autistic,
            previous_work_with_autistic=previous_work_with_autistic,
            length_work_with_autistic=length_work_with_autistic,
        )
        if user is None:
            u = self.construct_user(email="prof@questionnaire.com")
            pq.user_id = u.id
        else:
            u = user
            pq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            pq.participant_id = self.construct_participant(user_id=u.id, relationship=Relationship.dependent).id
        else:
            pq.participant_id = participant.id

        self.session.add(pq)
        self.session.commit()

        db_pq = (
            self.session.query(ProfessionalProfileQuestionnaire)
            .filter_by(participant_id=cast(pq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_pq.learning_interests, pq.learning_interests)
        return db_pq

    def construct_registration_questionnaire(
        self,
        first_name="Nora",
        last_name="Bora",
        email="nora@bora.com",
        zip_code=24401,
        relationship_to_autism=None,
        marketing_channel=None,
        user=None,
        event=None,
    ):

        from app.models import RegistrationQuestionnaire

        u = user if user else self.construct_user(email="nora@bora.com")
        e = event if event else self.construct_event(title="Webinar: You have to be here (virtually)")

        p = self.session.query(Participant).filter_by(user_id=cast(u.id, Integer)).first()

        rq = RegistrationQuestionnaire(
            first_name=first_name,
            last_name=last_name,
            email=email,
            zip_code=zip_code,
            relationship_to_autism=relationship_to_autism if relationship_to_autism else ["self", "professional"],
            marketing_channel=marketing_channel if marketing_channel else ["drive", "facebook"],
            user_id=u.id,
            event_id=e.id,
            participant_id=p.id,
        )

        self.session.add(rq)
        self.session.commit()

        db_rq = self.session.query(RegistrationQuestionnaire).filter_by(user_id=cast(rq.user_id, Integer)).first()
        self.assertEqual(db_rq.email, rq.email)
        return db_rq

    def construct_medication(
        self,
        symptom="symptomInsomnia",
        name="Magic Potion",
        notes="I feel better than ever!",
        supports_questionnaire=None,
    ):

        from app.models import Medication

        m = Medication(symptom=symptom, name=name, notes=notes)
        if supports_questionnaire is not None:
            m.supports_questionnaire_id = supports_questionnaire.id

        self.session.add(m)
        self.session.commit()

        db_m = self.session.query(Medication).filter_by(last_updated=m.last_updated).first()
        self.assertEqual(db_m.notes, m.notes)
        return db_m

    def construct_therapy(
        self, type="behavioral", timeframe="current", notes="Small steps", supports_questionnaire=None
    ):

        from app.models import Therapy

        t = Therapy(type=type, timeframe=timeframe, notes=notes)
        if supports_questionnaire is not None:
            t.supports_questionnaire_id = supports_questionnaire.id

        self.session.add(t)
        self.session.commit()

        db_t = self.session.query(Therapy).filter_by(last_updated=t.last_updated).first()
        self.assertEqual(db_t.notes, t.notes)
        return db_t

    def construct_supports_questionnaire(
        self,
        medications=None,
        therapies=None,
        assistive_devices=None,
        alternative_augmentative=None,
        participant=None,
        user=None,
    ):

        from app.models import SupportsQuestionnaire

        sq = SupportsQuestionnaire()
        if user is None:
            u = self.construct_user(email="support@questionnaire.com")
            sq.user_id = u.id
        else:
            u = user
            sq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            sq.participant_id = self.construct_participant(user_id=u.id, relationship=Relationship.dependent).id
        else:
            sq.participant_id = participant.id

        self.session.add(sq)
        self.session.commit()

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

        db_sq = (
            self.session.query(SupportsQuestionnaire).filter_by(participant_id=cast(sq.participant_id, Integer)).first()
        )
        self.assertEqual(db_sq.last_updated, sq.last_updated)
        return db_sq

    def construct_chain_session_questionnaire(self, participant=None, user=None):
        self.construct_chain_steps()

        from app.models import ChainQuestionnaire

        bq = ChainQuestionnaire()
        if user is None:
            from app.enums import Role

            u = self.construct_user(email="edudep@questionnaire.com", role=Role.researcher)
            bq.user_id = u.id
        else:
            u = user
            bq.user_id = u.id

        if participant is None:
            from app.enums import Relationship

            p = self.construct_participant(user_id=u.id, relationship=Relationship.dependent)
            bq.participant_id = p.id
        else:
            p = participant
            bq.participant_id = p.id

        session_date = parser.parse("2020-12-14T17:46:14.030Z")
        from app.models import ChainSessionStep

        session_1_step_1 = ChainSessionStep(
            date=session_date,
            chain_step_id=0,
            status="focus",
            completed=False,
            was_prompted=True,
            prompt_level="partial_physical",
            had_challenging_behavior=True,
            reason_step_incomplete="challenging_behavior",
            num_stars=0,
        )
        from app.models import ChainSession

        session_1 = ChainSession(date=session_date)
        session_1.step_attempts = [session_1_step_1]
        bq.sessions = [session_1]

        self.session.add(bq)
        self.session.commit()

        db_bq = (
            self.session.query(ChainQuestionnaire).filter_by(participant_id=cast(bq.participant_id, Integer)).first()
        )
        self.assertEqual(db_bq.participant_id, bq.participant_id)
        self.assertEqual(db_bq.user_id, bq.user_id)
        self.assertEqual(db_bq.sessions, bq.sessions)
        self.assertEqual(db_bq.sessions[0].date, session_date)
        self.assertEqual(db_bq.sessions[0].step_attempts[0].date, session_date)
        self.assertEqual(db_bq.sessions[0].step_attempts[0].num_stars, 0)
        return db_bq

    def construct_all_questionnaires(self, user=None) -> dict[str, object]:
        if user is None:
            user = self.construct_user()
        from app.enums import Relationship

        participant = self.construct_participant(user_id=user.id, relationship=Relationship.dependent)
        self.construct_usermeta(user=user)
        return {
            "clinical_diagnoses": self.construct_clinical_diagnoses_questionnaire(user=user, participant=participant),
            "contact": self.construct_contact_questionnaire(user=user, participant=participant),
            "current_behaviors_dependent": self.construct_current_behaviors_dependent_questionnaire(
                user=user, participant=participant
            ),
            "current_behaviors_self": self.construct_current_behaviors_self_questionnaire(
                user=user, participant=participant
            ),
            "demographics": self.construct_demographics_questionnaire(user=user, participant=participant),
            "developmental": self.construct_developmental_questionnaire(user=user, participant=participant),
            "education_dependent": self.construct_education_dependent_questionnaire(user=user, participant=participant),
            "education_self": self.construct_education_self_questionnaire(user=user, participant=participant),
            "employment": self.construct_employment_questionnaire(user=user, participant=participant),
            "evaluation_history_dependent": self.construct_evaluation_history_dependent_questionnaire(
                user=user, participant=participant
            ),
            "evaluation_history_self": self.construct_evaluation_history_self_questionnaire(
                user=user, participant=participant
            ),
            "home_dependent": self.construct_home_dependent_questionnaire(user=user, participant=participant),
            "home_self": self.construct_home_self_questionnaire(user=user, participant=participant),
            "identification": self.construct_identification_questionnaire(user=user, participant=participant),
            "professional": self.construct_professional_questionnaire(user=user, participant=participant),
            "supports": self.construct_supports_questionnaire(user=user, participant=participant),
            "registration": self.construct_registration_questionnaire(user=user),
            "chain_session": self.construct_chain_session_questionnaire(user=user, participant=participant),
        }
