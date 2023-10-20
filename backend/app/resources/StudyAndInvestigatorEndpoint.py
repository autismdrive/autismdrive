import flask_restful
from flask import request

from app.database import session
from app.models import Investigator, Study, StudyInvestigator
from app.models import StudyInvestigator
from app.rest_exception import RestException
from app.schemas import StudyInvestigatorSchema, InvestigatorStudiesSchema, StudyInvestigatorsSchema


class StudyByInvestigatorEndpoint(flask_restful.Resource):

    schema = InvestigatorStudiesSchema()

    def get(self, investigator_id):
        study_investigators = (
            session.query(StudyInvestigator)
            .join(StudyInvestigator.study)
            .filter(StudyInvestigator.investigator_id == investigator_id)
            .order_by(Study.title)
            .all()
        )
        return self.schema.dump(study_investigators, many=True)


class InvestigatorByStudyEndpoint(flask_restful.Resource):

    schema = StudyInvestigatorsSchema()

    def get(self, study_id):
        study_investigators = (
            session.query(StudyInvestigator)
            .join(StudyInvestigator.investigator)
            .filter(StudyInvestigator.study_id == study_id)
            .order_by(Investigator.name)
            .all()
        )
        return self.schema.dump(study_investigators, many=True)

    def post(self, study_id):
        request_data = request.get_json()

        for item in request_data:
            item["study_id"] = study_id

        study_investigators = self.schema.load(request_data, many=True)
        session.query(StudyInvestigator).filter_by(study_id=study_id).delete()
        for c in study_investigators:
            session.add(StudyInvestigator(study_id=study_id, investigator_id=c.investigator_id))
        session.commit()
        return self.get(study_id)


class StudyInvestigatorEndpoint(flask_restful.Resource):
    schema = StudyInvestigatorSchema()

    def get(self, id):
        model = session.query(StudyInvestigator).filter_by(id=id).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        session.query(StudyInvestigator).filter_by(id=id).delete()
        session.commit()
        return None


class StudyInvestigatorListEndpoint(flask_restful.Resource):
    schema = StudyInvestigatorSchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data)
        session.query(StudyInvestigator).filter_by(
            study_id=load_result.study_id, investigator_id=load_result.investigator_id
        ).delete()
        session.add(load_result)
        session.commit()
        return self.schema.dump(load_result)
