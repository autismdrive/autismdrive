from app.model.flow import Flow
from app.model.participant_relationship import Relationship


class Flows:

# WIP Method
    @staticmethod
    def parse_form():
        return ""

    @staticmethod
    def get_self_intake_flow():
        flow = Flow(name="self_intake")
        flow.relationship = Relationship.self_participant
        flow.add_step('identification_questionnaire')
        flow.add_step('contact_questionnaire')
        flow.add_step('demographics_questionnaire')
        flow.add_step('home_self_questionnaire')
        flow.add_step('evaluation_history_self_questionnaire')
        flow.add_step('clinical_diagnoses_questionnaire')
        flow.add_step('current_behaviors_self_questionnaire')
        flow.add_step('education_self_questionnaire')
        flow.add_step('employment_questionnaire')
        flow.add_step('supports_questionnaire')
        return flow

    @staticmethod
    def get_dependent_intake_flow():
        flow = Flow(name="dependent_intake")
        flow.relationship = Relationship.dependent
        flow.add_step('identification_questionnaire')
        flow.add_step('demographics_questionnaire')
        flow.add_step('home_dependent_questionnaire')
        flow.add_step('evaluation_history_dependent_questionnaire')
        flow.add_step('clinical_diagnoses_questionnaire')
        flow.add_step('developmental_questionnaire')
        flow.add_step('current_behaviors_dependent_questionnaire')
        flow.add_step('education_dependent_questionnaire')
        flow.add_step('supports_questionnaire')
        return flow

    @staticmethod
    def get_guardian_intake_flow():
        flow = Flow(name="guardian_intake")
        flow.relationship = Relationship.self_guardian
        flow.add_step('identification_questionnaire')
        flow.add_step('contact_questionnaire')
        flow.add_step('demographics_questionnaire')
        return flow

    @staticmethod
    def get_professional_intake_flow():
        flow = Flow(name="professional_intake")
        flow.relationship = Relationship.self_professional
        flow.add_step('identification_questionnaire')
        flow.add_step('contact_questionnaire')
        flow.add_step('demographics_questionnaire')
        flow.add_step('professional_profile_questionnaire')
        return flow

    @staticmethod
    def get_interested_intake_flow():
        flow = Flow(name="interested_intake")
        flow.relationship = Relationship.self_interested
        flow.add_step('identification_questionnaire')
        flow.add_step('contact_questionnaire')
        return flow

    @staticmethod
    def get_registration_flow():
        flow = Flow(name="registration")
        flow.add_step('registration_questionnaire')
        return flow

    # SkillStar Flows
    @staticmethod
    def get_skillstar_flow():
        flow = Flow(name="skillstar")
        flow.relationship = Relationship.self_professional
        flow.add_step('chain_questionnaire')
        return flow

    @staticmethod
    def get_skillstar_flows():
        flows = [
            Flows.get_skillstar_flow(),
        ]
        return flows

    @staticmethod
    def get_all_flows():
        flows = [
            Flows.get_self_intake_flow(),
            Flows.get_dependent_intake_flow(),
            Flows.get_guardian_intake_flow(),
            Flows.get_professional_intake_flow(),
            Flows.get_interested_intake_flow(),
            Flows.get_registration_flow(),
            Flows.get_skillstar_flow(),
        ]
        return flows

    @staticmethod
    def get_flow_by_name(name):
        if name == 'self_intake':
            return Flows.get_self_intake_flow()
        if name == 'dependent_intake':
            return Flows.get_dependent_intake_flow()
        if name == 'guardian_intake':
            return Flows.get_guardian_intake_flow()
        if name == 'professional_intake':
            return Flows.get_professional_intake_flow()
        if name == 'interested_intake':
            return Flows.get_interested_intake_flow()
        if name == 'registration':
            return Flows.get_registration_flow()
        if name == 'skillstar':
            return Flows.get_skillstar_flow()

    @staticmethod
    def get_flow_by_relationship(name):
        if name == Relationship.self_participant:
            return Flows.get_self_intake_flow()
        if name == Relationship.dependent:
            return Flows.get_dependent_intake_flow()
        if name == Relationship.self_guardian:
            return Flows.get_guardian_intake_flow()
        if name == Relationship.self_professional:
            return Flows.get_professional_intake_flow()
        if name == Relationship.self_interested:
            return Flows.get_interested_intake_flow()

