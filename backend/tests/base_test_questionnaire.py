import random
import string

from dateutil import parser
from sqlalchemy import cast, Integer, select

from tests.base_test import BaseTest
from app.enums import Relationship, Role
from app.models import (
    AlternativeAugmentative,
    AssistiveDevice,
    ChainQuestionnaire,
    ChainSession,
    ChainSessionStep,
    ClinicalDiagnosesQuestionnaire,
    ContactQuestionnaire,
    CurrentBehaviorsDependentQuestionnaire,
    CurrentBehaviorsSelfQuestionnaire,
    DemographicsQuestionnaire,
    DevelopmentalQuestionnaire,
    EducationDependentQuestionnaire,
    EducationSelfQuestionnaire,
    EmploymentQuestionnaire,
    EvaluationHistoryDependentQuestionnaire,
    EvaluationHistorySelfQuestionnaire,
    HomeDependentQuestionnaire,
    HomeSelfQuestionnaire,
    Housemate,
    IdentificationQuestionnaire,
    Medication,
    Participant,
    ProfessionalProfileQuestionnaire,
    RegistrationQuestionnaire,
    SupportsQuestionnaire,
    Therapy,
    User,
)
from app.resources.ParticipantEndpoint import get_participant_by_id
from app.resources.UserEndpoint import get_user_by_id
from fixtures.fixure_utils import fake


class BaseTestQuestionnaire(BaseTest):
    """Tools for building questionnaires of all types and descriptions."""

    def randomString(self):
        char_set = string.ascii_uppercase + string.digits
        return "".join(random.sample(char_set * 6, 6))

    def construct_user_and_participant(
        self,
        user_id: int = None,
        participant_id: int = None,
        relationship: Relationship = Relationship.dependent,
        user_role: Role = Role.user,
    ) -> tuple[User, Participant]:
        """
        Constructs a user and a participant or retrieves an existing user and participant for the given ID(s).
        Returns a tuple of the User and Participant
        """

        if user_id is None:
            u = self.construct_user(email=fake.email(), role=user_role)
        else:
            u = get_user_by_id(user_id, with_joins=True)
        assert u is not None
        u_id = u.id

        if participant_id is None:
            p = self.construct_participant(user_id=u_id, relationship=relationship)
        else:
            p = get_participant_by_id(participant_id, with_joins=True)
        assert p is not None

        return u, p

    def construct_assistive_device(
        self,
        type_group="mobility",
        device_type="prosthetic",
        timeframe="current",
        notes="I love my new leg!",
        supports_questionnaire_id: int = None,
    ):
        ad = AssistiveDevice(type_group=type_group, type=device_type, timeframe=timeframe, notes=notes)
        if supports_questionnaire_id is not None:
            ad.supports_questionnaire_id = supports_questionnaire_id

        self.session.add(ad)
        self.session.commit()
        ad_id = ad.id
        assert ad_id is not None

        db_ad = self.session.query(AssistiveDevice).filter_by(id=ad_id).first()
        self.assertEqual(db_ad.notes, notes)
        self.assertEqual(db_ad.type_group, type_group)
        self.assertEqual(db_ad.type, device_type)
        return db_ad

    def construct_alternative_augmentative(
        self, aac_type="lowTechAAC", timeframe="current", notes="We use pen and paper", supports_questionnaire_id=None
    ):
        aac = AlternativeAugmentative(type=aac_type, timeframe=timeframe, notes=notes)
        if supports_questionnaire_id is not None:
            aac.supports_questionnaire_id = supports_questionnaire_id

        self.session.add(aac)
        self.session.commit()

        db_aac = self.session.query(AlternativeAugmentative).filter_by(last_updated=aac.last_updated).first()
        self.assertEqual(db_aac.notes, notes)
        self.assertEqual(db_aac.type, aac_type)
        return db_aac

    def construct_clinical_diagnoses_questionnaire(
        self,
        developmental=None,
        mental_health=None,
        medical=None,
        genetic=None,
        participant_id: int = None,
        user_id: int = None,
    ):
        developmental = ["speechLanguage"] if developmental is None else developmental
        mental_health = ["ocd"] if mental_health is None else mental_health
        medical = ["insomnia"] if medical is None else medical
        genetic = ["corneliaDeLange"] if genetic is None else genetic

        u, p = self.construct_user_and_participant(user_id, participant_id)
        u_id = u.id
        p_id = p.id

        cdq = ClinicalDiagnosesQuestionnaire(
            developmental=developmental,
            mental_health=mental_health,
            medical=medical,
            genetic=genetic,
            user_id=u_id,
            participant_id=p_id,
        )
        self.session.add(cdq)
        self.session.commit()

        db_cdq = (
            self.session.execute(
                select(ClinicalDiagnosesQuestionnaire).filter_by(user_id=u_id).filter_by(participant_id=p_id)
            )
            .unique()
            .scalar_one_or_none()
        )

        self.assertEqual(db_cdq.user_id, u_id)
        self.assertEqual(db_cdq.participant_id, p_id)
        self.assertEqual(db_cdq.developmental, developmental)
        self.assertEqual(db_cdq.mental_health, mental_health)
        self.assertEqual(db_cdq.medical, medical)
        self.assertEqual(db_cdq.genetic, genetic)
        return db_cdq

    def construct_contact_questionnaire(
        self,
        phone="123-456-7890",
        zip_code=55678,
        marketing_channel="Zine Ad",
        participant_id: int = None,
        user_id: int = None,
    ):

        u, p = self.construct_user_and_participant(user_id, participant_id)
        u_id = u.id
        p_id = p.id

        cq = ContactQuestionnaire(
            phone=phone, zip=zip_code, marketing_channel=marketing_channel, user_id=u_id, participant_id=p_id
        )

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
        participant_id: int = None,
        user_id: int = None,
    ) -> CurrentBehaviorsDependentQuestionnaire:
        concerning_behaviors = ["hoarding"] if concerning_behaviors is None else concerning_behaviors
        academic_difficulty_areas = (
            ["math", "writing"] if academic_difficulty_areas is None else academic_difficulty_areas
        )

        u, p = self.construct_user_and_participant(user_id, participant_id)
        u_id = u.id
        p_id = p.id

        cbd = CurrentBehaviorsDependentQuestionnaire(
            dependent_verbal_ability=dependent_verbal_ability,
            concerning_behaviors=concerning_behaviors,
            has_academic_difficulties=has_academic_difficulties,
            academic_difficulty_areas=academic_difficulty_areas,
            user_id=u_id,
            participant_id=p_id,
        )

        self.session.add(cbd)
        self.session.commit()

        db_cbd = (
            self.session.execute(select(CurrentBehaviorsDependentQuestionnaire).filter_by(participant_id=p_id))
            .unique()
            .scalar_one_or_none()
        )
        assert db_cbd is not None
        self.assertEqual(db_cbd.dependent_verbal_ability, dependent_verbal_ability)
        self.assertEqual(db_cbd.concerning_behaviors, concerning_behaviors)
        self.assertEqual(db_cbd.has_academic_difficulties, has_academic_difficulties)
        self.assertEqual(db_cbd.academic_difficulty_areas, academic_difficulty_areas)

        return db_cbd

    def construct_current_behaviors_self_questionnaire(
        self,
        self_verbal_ability="verbal",
        has_academic_difficulties=True,
        academic_difficulty_areas="math",
        participant_id: int = None,
        user_id: int = None,
    ) -> CurrentBehaviorsSelfQuestionnaire:

        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.self_participant)
        u_id = u.id
        p_id = p.id
        cb = CurrentBehaviorsSelfQuestionnaire(
            self_verbal_ability=self_verbal_ability,
            has_academic_difficulties=has_academic_difficulties,
            academic_difficulty_areas=academic_difficulty_areas,
            user_id=u_id,
            participant_id=p_id,
        )

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
        self,
        birth_sex="intersex",
        gender_identity="intersex",
        race_ethnicity="raceBlack",
        participant_id: int = None,
        user_id: int = None,
    ):

        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.self_participant)
        u_id = u.id
        p_id = p.id
        dq = DemographicsQuestionnaire(
            birth_sex=birth_sex,
            gender_identity=gender_identity,
            race_ethnicity=race_ethnicity,
            user_id=u_id,
            participant_id=p_id,
        )

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
        participant_id: int = None,
        user_id: int = None,
    ):

        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.dependent)
        u_id = u.id
        p_id = p.id
        dq = DevelopmentalQuestionnaire(
            had_birth_complications=had_birth_complications,
            when_motor_milestones=when_motor_milestones,
            when_language_milestones=when_language_milestones,
            when_toileting_milestones=when_toileting_milestones,
            user_id=u_id,
            participant_id=p_id,
        )

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
        participant_id: int = None,
        user_id: int = None,
    ):

        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.dependent)
        u_id = u.id
        p_id = p.id
        eq = EducationDependentQuestionnaire(
            attends_school=attends_school,
            school_name=school_name,
            school_type=school_type,
            dependent_placement=dependent_placement,
            user_id=u_id,
            participant_id=p_id,
        )

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
        participant_id: int = None,
        user_id: int = None,
    ):

        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.self_participant)
        u_id = u.id
        p_id = p.id
        eq = EducationSelfQuestionnaire(
            attends_school=attends_school,
            school_name=school_name,
            school_type=school_type,
            self_placement=self_placement,
            user_id=u_id,
            participant_id=p_id,
        )

        self.session.add(eq)
        self.session.commit()

        db_eq = (
            self.session.query(EducationSelfQuestionnaire)
            .filter_by(participant_id=cast(eq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_eq.attends_school, attends_school)
        self.assertEqual(db_eq.school_name, school_name)
        self.assertEqual(db_eq.school_type, school_type)
        self.assertEqual(db_eq.self_placement, self_placement)
        return db_eq

    def construct_employment_questionnaire(
        self,
        is_currently_employed=True,
        employment_capacity="fullTime",
        has_employment_support=False,
        participant_id: int = None,
        user_id: int = None,
    ):

        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.self_participant)
        u_id = u.id
        p_id = p.id
        eq = EmploymentQuestionnaire(
            is_currently_employed=is_currently_employed,
            employment_capacity=employment_capacity,
            has_employment_support=has_employment_support,
            user_id=u_id,
            participant_id=p_id,
        )

        self.session.add(eq)
        self.session.commit()

        db_eq = (
            self.session.query(EmploymentQuestionnaire)
            .filter_by(participant_id=cast(eq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_eq.employment_capacity, employment_capacity)
        return db_eq

    def construct_evaluation_history_dependent_questionnaire(
        self,
        self_identifies_autistic=True,
        has_autism_diagnosis=True,
        years_old_at_first_diagnosis=7,
        who_diagnosed="pediatrician",
        participant_id: int = None,
        user_id: int = None,
    ):
        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.dependent)
        u_id = u.id
        p_id = p.id
        ehq = EvaluationHistoryDependentQuestionnaire(
            self_identifies_autistic=self_identifies_autistic,
            has_autism_diagnosis=has_autism_diagnosis,
            years_old_at_first_diagnosis=years_old_at_first_diagnosis,
            who_diagnosed=who_diagnosed,
            user_id=u_id,
            participant_id=p_id,
        )

        self.session.add(ehq)
        self.session.commit()

        db_ehq = (
            self.session.query(EvaluationHistoryDependentQuestionnaire)
            .filter_by(participant_id=cast(ehq.participant_id, Integer))
            .first()
        )
        self.assertEqual(db_ehq.who_diagnosed, who_diagnosed)
        return db_ehq

    def construct_evaluation_history_self_questionnaire(
        self,
        self_identifies_autistic=True,
        has_autism_diagnosis=True,
        years_old_at_first_diagnosis=7,
        who_diagnosed="pediatrician",
        participant_id: int = None,
        user_id: int = None,
    ):
        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.self_participant)
        u_id = u.id
        p_id = p.id
        ehq = EvaluationHistorySelfQuestionnaire(
            self_identifies_autistic=self_identifies_autistic,
            has_autism_diagnosis=has_autism_diagnosis,
            years_old_at_first_diagnosis=years_old_at_first_diagnosis,
            who_diagnosed=who_diagnosed,
            user_id=u_id,
            participant_id=p_id,
        )

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
        participant_id: int = None,
        user_id: int = None,
    ):

        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.dependent)
        u_id = u.id
        p_id = p.id
        hq = HomeDependentQuestionnaire(
            dependent_living_situation=[dependent_living_situation],
            struggle_to_afford=struggle_to_afford,
            user_id=u_id,
            participant_id=p_id,
        )

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
        self,
        self_living_situation="alone",
        housemates=None,
        struggle_to_afford=False,
        participant_id: int = None,
        user_id: int = None,
    ):
        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.self_participant)
        u_id = u.id
        p_id = p.id
        hq = HomeSelfQuestionnaire(
            self_living_situation=[self_living_situation],
            struggle_to_afford=struggle_to_afford,
            user_id=u_id,
            participant_id=p_id,
        )

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
        participant_id: int = None,
        user_id: int = None,
    ):
        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.dependent)
        u_id = u.id
        p_id = p.id

        iq = IdentificationQuestionnaire(
            relationship_to_participant=relationship_to_participant,
            first_name=first_name,
            is_first_name_preferred=is_first_name_preferred,
            nickname=nickname,
            birth_state=birth_state,
            is_english_primary=is_english_primary,
            user_id=u_id,
            participant_id=p_id,
        )

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
        participant_id: int = None,
        user_id: int = None,
    ):
        professional_identity = ["artTher", "profOther"] if professional_identity is None else professional_identity
        learning_interests = ["insuranceCov", "learnOther"] if learning_interests is None else learning_interests

        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.dependent)
        u_id = u.id
        p_id = p.id
        pq = ProfessionalProfileQuestionnaire(
            purpose=purpose,
            professional_identity=professional_identity,
            professional_identity_other=professional_identity_other,
            learning_interests=learning_interests,
            learning_interests_other=learning_interests_other,
            currently_work_with_autistic=currently_work_with_autistic,
            previous_work_with_autistic=previous_work_with_autistic,
            length_work_with_autistic=length_work_with_autistic,
            user_id=u_id,
            participant_id=p_id,
        )

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
        user_id: int = None,
        participant_id: int = None,
        event=None,
    ):

        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.self_participant)
        u_id = u.id
        p_id = p.id
        e = event if event else self.construct_event(title="Webinar: You have to be here (virtually)")
        e_id = e.id

        rq = RegistrationQuestionnaire(
            first_name=first_name,
            last_name=last_name,
            email=email,
            zip_code=zip_code,
            relationship_to_autism=relationship_to_autism if relationship_to_autism else ["self", "professional"],
            marketing_channel=marketing_channel if marketing_channel else ["drive", "facebook"],
            user_id=u_id,
            event_id=e_id,
            participant_id=p_id,
        )

        self.session.add(rq)
        self.session.commit()

        db_rq = self.session.query(RegistrationQuestionnaire).filter_by(user_id=u_id).first()
        self.assertEqual(db_rq.email, rq.email)
        return db_rq

    def construct_medication(
        self,
        symptom="symptomInsomnia",
        name="Magic Potion",
        notes="I feel better than ever!",
        supports_questionnaire_id=None,
    ):

        m = Medication(symptom=symptom, name=name, notes=notes)
        if supports_questionnaire_id is not None:
            m.supports_questionnaire_id = supports_questionnaire_id

        self.session.add(m)
        self.session.commit()
        new_med_id = m.id
        new_med_name = m.name
        new_med_symptom = m.symptom
        new_med_notes = m.notes
        self.session.close()

        db_m = self.session.execute(select(Medication).filter_by(id=new_med_id)).unique().scalar_one()
        self.assertEqual(db_m.name, new_med_name)
        self.assertEqual(db_m.symptom, new_med_symptom)
        self.assertEqual(db_m.notes, new_med_notes)
        self.session.close()
        return db_m

    def construct_therapy(
        self, therapy_type="behavioral", timeframe="current", notes="Small steps", supports_questionnaire_id=None
    ):

        t = Therapy(type=therapy_type, timeframe=timeframe, notes=notes)
        if supports_questionnaire_id is not None:
            t.supports_questionnaire_id = supports_questionnaire_id

        self.session.add(t)
        self.session.commit()

        db_t = self.session.query(Therapy).filter_by(last_updated=t.last_updated).first()
        self.assertEqual(db_t.notes, notes)
        self.assertEqual(db_t.type, therapy_type)
        return db_t

    def construct_supports_questionnaire(
        self,
        medications=None,
        therapies=None,
        assistive_devices=None,
        alternative_augmentative=None,
        participant_id: int = None,
        user_id: int = None,
    ):
        u, p = self.construct_user_and_participant(user_id, participant_id, relationship=Relationship.dependent)
        u_id = u.id
        p_id = p.id
        sq = SupportsQuestionnaire(
            user_id=u_id,
            participant_id=p_id,
        )
        self.session.add(sq)
        self.session.commit()

        sq_id = sq.id

        if assistive_devices is None:
            self.construct_assistive_device(supports_questionnaire_id=sq_id)
        else:
            sq.assistive_devices = assistive_devices

        if alternative_augmentative is None:
            self.construct_alternative_augmentative(supports_questionnaire_id=sq_id)
        else:
            sq.alternative_augmentative = alternative_augmentative

        if medications is None:
            self.construct_medication(supports_questionnaire_id=sq_id)
        else:
            sq.medications = medications

        if therapies is None:
            self.construct_therapy(supports_questionnaire_id=sq_id)
        else:
            sq.therapies = therapies

        self.session.add(sq)
        self.session.commit()

        db_sq = self.session.query(SupportsQuestionnaire).filter_by(participant_id=p_id).first()
        self.assertEqual(db_sq.last_updated, sq.last_updated)
        return db_sq

    def construct_chain_session_questionnaire(self, participant_id: int = None, user_id: int = None):
        self.construct_chain_steps()

        u, p = self.construct_user_and_participant(
            user_id, participant_id, relationship=Relationship.dependent, user_role=Role.researcher
        )
        u_id = u.id
        p_id = p.id
        bq = ChainQuestionnaire(user_id=u_id, participant_id=p_id)

        session_date = parser.parse("2020-12-14T17:46:14.030Z")

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

        session_1 = ChainSession(date=session_date)
        session_1.step_attempts = [session_1_step_1]
        bq.sessions = [session_1]

        self.session.add(bq)
        self.session.commit()

        db_bq = self.session.query(ChainQuestionnaire).filter_by(participant_id=p_id).first()
        self.assertEqual(db_bq.participant_id, bq.participant_id)
        self.assertEqual(db_bq.user_id, bq.user_id)
        self.assertEqual(db_bq.sessions, bq.sessions)
        self.assertEqual(db_bq.sessions[0].date, session_date)
        self.assertEqual(db_bq.sessions[0].step_attempts[0].date, session_date)
        self.assertEqual(db_bq.sessions[0].step_attempts[0].num_stars, 0)
        return db_bq

    def construct_all_questionnaires(self, user_id: int = None) -> dict[str, object]:
        u, p = self.construct_user_and_participant(
            user_id=user_id, participant_id=None, relationship=Relationship.dependent
        )
        u_id = u.id
        p_id = p.id

        self.construct_user_meta(user_id=u_id)

        return {
            "clinical_diagnoses": self.construct_clinical_diagnoses_questionnaire(user_id=u_id, participant_id=p_id),
            "contact": self.construct_contact_questionnaire(user_id=u_id, participant_id=p_id),
            "current_behaviors_dependent": self.construct_current_behaviors_dependent_questionnaire(
                user_id=u_id, participant_id=p_id
            ),
            "current_behaviors_self": self.construct_current_behaviors_self_questionnaire(
                user_id=u_id, participant_id=p_id
            ),
            "demographics": self.construct_demographics_questionnaire(user_id=u_id, participant_id=p_id),
            "developmental": self.construct_developmental_questionnaire(user_id=u_id, participant_id=p_id),
            "education_dependent": self.construct_education_dependent_questionnaire(user_id=u_id, participant_id=p_id),
            "education_self": self.construct_education_self_questionnaire(user_id=u_id, participant_id=p_id),
            "employment": self.construct_employment_questionnaire(user_id=u_id, participant_id=p_id),
            "evaluation_history_dependent": self.construct_evaluation_history_dependent_questionnaire(
                user_id=u_id, participant_id=p_id
            ),
            "evaluation_history_self": self.construct_evaluation_history_self_questionnaire(
                user_id=u_id, participant_id=p_id
            ),
            "home_dependent": self.construct_home_dependent_questionnaire(user_id=u_id, participant_id=p_id),
            "home_self": self.construct_home_self_questionnaire(user_id=u_id, participant_id=p_id),
            "identification": self.construct_identification_questionnaire(user_id=u_id, participant_id=p_id),
            "professional": self.construct_professional_questionnaire(user_id=u_id, participant_id=p_id),
            "supports": self.construct_supports_questionnaire(user_id=u_id, participant_id=p_id),
            "registration": self.construct_registration_questionnaire(user_id=u_id),
            "chain_session": self.construct_chain_session_questionnaire(user_id=u_id, participant_id=p_id),
        }
