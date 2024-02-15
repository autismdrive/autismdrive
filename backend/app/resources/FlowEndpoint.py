import copy
import datetime

import flask_restful
from flask import request, g
from marshmallow import ValidationError
from sqlalchemy import cast, Integer, select
from sqlalchemy.orm import joinedload

from app.auth import auth
from app.database import session, get_class
from app.export_service import ExportService
from app.models import Flows, Participant, StepLog
from app.rest_exception import RestException
from app.schemas import FlowSchema
from app.utils import pascal_case_it


class FlowEndpoint(flask_restful.Resource):
    schema = FlowSchema()

    @auth.login_required
    def get(self, name, participant_id):
        p_id_int = int(participant_id)
        flow = copy.deepcopy(Flows.get_flow_by_name(name))
        participant = session.query(Participant).filter_by(id=p_id_int).first()
        if participant is None:
            raise RestException(RestException.NOT_FOUND)
        if g.user.related_to_participant(p_id_int) and not g.user.role == "Admin":
            raise RestException(RestException.UNRELATED_PARTICIPANT)
        step_logs = (
            session.execute(select(StepLog).filter_by(participant_id=p_id_int, flow=name)).unique().scalars().all()
        )
        session.close()

        for log in step_logs:
            flow.steps = flow.update_step_progress(log)
        return self.schema.dump(flow)


class FlowListEndpoint(flask_restful.Resource):
    flows_schema = FlowSchema(many=True)

    def get(self):
        return self.flows_schema.dump(Flows.get_all_flows())


class FlowQuestionnaireMetaEndpoint(flask_restful.Resource):
    def get(self, flow_name: str, questionnaire_name: str):
        questionnaire_name = pascal_case_it(questionnaire_name)
        flow = Flows.get_flow_by_name(flow_name)
        if flow is None:
            raise RestException(RestException.NOT_FOUND)
        class_ref = get_class(questionnaire_name)
        questionnaire = class_ref()
        return ExportService.get_meta(questionnaire, flow.relationship)

    #        return schema.dump(questionnaire)


class FlowQuestionnaireEndpoint(flask_restful.Resource):
    @auth.login_required
    def post(self, flow_name: str, questionnaire_name: str):
        flow = Flows.get_flow_by_name(flow_name)
        if flow is None:
            raise RestException(RestException.NOT_FOUND)
        if not flow.has_step(questionnaire_name):
            raise RestException(RestException.NOT_IN_THE_FLOW)
        request_data = request.get_json()
        request_data["user_id"] = g.user.id
        if "_links" in request_data:
            request_data.pop("_links")

        class_name = pascal_case_it(questionnaire_name)
        model_class = get_class(class_name)
        schema = ExportService.get_schema(class_name)

        try:
            new_quest: model_class = schema.load(request_data, session=session)
        except ValidationError as e:
            raise RestException(RestException.INVALID_OBJECT, details=e.messages)

        if hasattr(new_quest, "participant_id"):
            if new_quest.participant_id is None:
                raise RestException(RestException.INVALID_OBJECT, details="You must supply a participant id.")
            if not g.user.related_to_participant(new_quest.participant_id):
                raise RestException(RestException.UNRELATED_PARTICIPANT)
        else:
            raise RestException(RestException.INVALID_OBJECT, details="You must supply a participant id.")

        session.add(new_quest)
        session.commit()
        new_q_id = new_quest.id
        session.close()

        select_statement = select(model_class)

        # Create joinedload for all relationships
        for relationship in model_class.__mapper__.relationships:
            select_statement = select_statement.options(joinedload(getattr(model_class, relationship.key)))

        db_new_q = session.execute(select_statement.filter_by(id=new_q_id)).unique().scalar()
        session.close()

        self.log_progress(flow, questionnaire_name, db_new_q)
        return schema.dump(db_new_q)

    def log_progress(self, flow, questionnaire_name, questionnaire):
        log = StepLog(
            questionnaire_name=questionnaire_name,
            questionnaire_id=questionnaire.id,
            flow=flow.name,
            participant_id=questionnaire.participant_id,
            user_id=g.user.id,
            date_completed=datetime.datetime.utcnow(),
            time_on_task_ms=questionnaire.time_on_task_ms,
        )
        session.add(log)
        session.commit()
        session.close()
