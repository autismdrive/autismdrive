import datetime

import flask_restful
from flask import request, g

from app import RestException, db, auth
from app.model.flow import Flow
from app.model.participant import Participant, Relationship
from app.model.step_log import StepLog
from app.resources.schema import FlowSchema
from app.export_service import ExportService


class Flows:
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
    def get_all_flows():
        flows = [
            Flows.get_self_intake_flow(),
            Flows.get_dependent_intake_flow(),
            Flows.get_guardian_intake_flow(),
            Flows.get_professional_intake_flow()
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


class FlowEndpoint(flask_restful.Resource):
    schema = FlowSchema()

    @auth.login_required
    def get(self, name, participant_id):
        flow = Flows.get_flow_by_name(name)
        participant = db.session.query(Participant).filter_by(id=participant_id).first()
        if participant is None: raise RestException(RestException.NOT_FOUND)
        if g.user.related_to_participant(participant_id) and not g.user.role == 'Admin':
            raise RestException(RestException.UNRELATED_PARTICIPANT)
        step_logs = db.session.query(StepLog).filter_by(participant_id=participant_id, flow=name)
        for log in step_logs:
            flow.update_step_progress(log)
        return self.schema.dump(flow)


class FlowListEndpoint(flask_restful.Resource):
    flows_schema = FlowSchema(many=True)

    def get(self):
        return self.flows_schema.dump(Flows.get_all_flows()).data


class FlowQuestionnaireMetaEndpoint(flask_restful.Resource):

    def get(self, flow, questionnaire_name):
        questionnaire_name = ExportService.camel_case_it(questionnaire_name)
        flow = Flows.get_flow_by_name(flow)
        if flow is None:
            raise RestException(RestException.NOT_FOUND)
        class_ref = ExportService.get_class(questionnaire_name)
        questionnaire = db.session.query(class_ref).first()
        return ExportService.get_meta(questionnaire, flow.relationship)
    #        return schema.dump(questionnaire)


class FlowQuestionnaireEndpoint(flask_restful.Resource):

    @auth.login_required
    def post(self, flow, questionnaire_name):
        flow = Flows.get_flow_by_name(flow)
        if flow is None:
            raise RestException(RestException.NOT_FOUND)
        if not flow.has_step(questionnaire_name):
            raise RestException(RestException.NOT_IN_THE_FLOW)
        request_data = request.get_json()
        request_data["user_id"] = g.user.id
        schema = ExportService.get_schema(ExportService.camel_case_it(questionnaire_name))
        new_quest, errors = schema.load(request_data, session=db.session)

        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        if new_quest.participant_id is None: raise RestException(RestException.INVALID_OBJECT, details=
                                                                 "You must supply a participant id.")
        if not g.user.related_to_participant(new_quest.participant_id):
            raise RestException(RestException.UNRELATED_PARTICIPANT)
        db.session.add(new_quest)
        db.session.commit()
        self.log_progress(flow, questionnaire_name, new_quest)
        return schema.dump(new_quest)

    def log_progress(self, flow, questionnaire_name, questionnaire):
        log = StepLog(questionnaire_name=questionnaire_name,
                      questionnaire_id=questionnaire.id,
                      flow=flow.name,
                      participant_id=questionnaire.participant_id,
                      user_id=g.user.id,
                      date_completed=datetime.datetime.now(),
                      time_on_task_ms=questionnaire.time_on_task_ms)
        db.session.add(log)
        db.session.commit()
