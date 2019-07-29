import flask_restful
from flask import request

from app import db, RestException
from app.model.investigator import Investigator
from app.model.study import Study
from app.model.study_investigator import StudyInvestigator
from app.schema.schema import StudyInvestigatorSchema, InvestigatorStudiesSchema, StudyInvestigatorsSchema


class StudyByInvestigatorEndpoint(flask_restful.Resource):

    schema = InvestigatorStudiesSchema()

    def get(self, investigator_id):
        study_investigators = db.session.query(StudyInvestigator)\
            .join(StudyInvestigator.study)\
            .filter(StudyInvestigator.investigator_id == investigator_id)\
            .order_by(Study.title)\
            .all()
        return self.schema.dump(study_investigators, many=True)


class InvestigatorByStudyEndpoint(flask_restful.Resource):

    schema = StudyInvestigatorsSchema()

    def get(self, study_id):
        study_investigators = db.session.query(StudyInvestigator).\
            join(StudyInvestigator.investigator).\
            filter(StudyInvestigator.study_id == study_id).\
            order_by(Investigator.name).\
            all()
        return self.schema.dump(study_investigators,many=True)

    def post(self, study_id):
        request_data = request.get_json()
        study_investigators = self.schema.load(request_data, many=True).data
        db.session.query(StudyInvestigator).filter_by(study_id=study_id).delete()
        for c in study_investigators:
            db.session.add(StudyInvestigator(study_id=study_id,
                           investigator_id=c.investigator_id))
        db.session.commit()
        return self.get(study_id)


class StudyInvestigatorEndpoint(flask_restful.Resource):
    schema = StudyInvestigatorSchema()

    def get(self, id):
        model = db.session.query(StudyInvestigator).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        db.session.query(StudyInvestigator).filter_by(id=id).delete()
        db.session.commit()
        return None


class StudyInvestigatorListEndpoint(flask_restful.Resource):
    schema = StudyInvestigatorSchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data).data
        db.session.query(StudyInvestigator).filter_by(study_id=load_result.study_id,
                                                     investigator_id=load_result.investigator_id).delete()
        db.session.add(load_result)
        db.session.commit()
        return self.schema.dump(load_result)
