import datetime

import flask_restful
from flask import request, g

from app import RestException, db, auth
from app.model.flow import Flow, FlowSchema
from app.model.progress_log import ProgressLog
from app.question_service import QuestionService


class Flows:
    @staticmethod
    def get_intake_flow():
        flow = Flow(name="intake")
        flow.add_step('contact_questionnaire')
        flow.add_step('demographics_questionnaire')
        flow.add_step('evaluation_history_questionnaire')
        flow.add_step('home_questionnaire')
        flow.add_step('identification_questionnaire')
        return flow

    @staticmethod
    def get_all_flows():
        return [Flows.get_intake_flow()];

    @staticmethod
    def get_flow_by_name(name):
        if name == 'intake':
            return Flows.get_intake_flow()


class FlowEndpoint(flask_restful.Resource):
    schema = FlowSchema()

    @auth.login_required
    def get(self, name):
        return self.schema.dump(Flows.get_flow_by_name(name))


class FlowListEndpoint(flask_restful.Resource):
    flows_schema = FlowSchema(many=True)

    def get(self):
        return self.flows_schema.dump(Flows.get_all_flows()).data


class FlowQuestionnaireEndpoint(flask_restful.Resource):

    @auth.login_required
    def post(self, flow, questionnaire_name):
        flow = Flows.get_flow_by_name(flow)
        if flow is None:
            raise RestException(RestException.NOT_FOUND)
        if not flow.has_step(questionnaire_name):
            raise RestException(RestException.NOT_IN_THE_FLOW)
        request_data = request.get_json()
        schema = QuestionService.get_schema(questionnaire_name)
        new_quest, errors = schema.load(request_data, session=db.session)

        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        if new_quest.participant_id is None: raise RestException(RestException.INVALID_OBJECT, details=
                                                                 "You must supply a participant id.")
        if not g.user.related_to_participant(new_quest.participant_id):
            raise RestException(RestException.UNRELATED_PARTICIPANT)
        db.session.add(new_quest)
        db.session.commit()
        self.log_progress(flow, questionnaire_name, new_quest);
        return schema.dump(new_quest)

    def log_progress(self, flow, questionnaire_name, questionnaire):
        log = ProgressLog(questionnaire_name=questionnaire_name,
                          questionnaire_id=questionnaire.id,
                          flow=flow.name,
                          participant_id=questionnaire.participant_id,
                          user_id=g.user.id,
                          date_completed=datetime.datetime.now(),
                          time_on_task_ms=questionnaire.time_on_task_ms)
        db.session.add(log)
        db.session.commit()
