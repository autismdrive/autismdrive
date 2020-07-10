import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError

from app import RestException, db, elastic_index
from app.model.study import Study
from app.model.study_category import StudyCategory
from app.model.study_investigator import StudyInvestigator
from app.model.study_user import StudyUser
from app.schema.schema import StudySchema


class StudyEndpoint(flask_restful.Resource):

    schema = StudySchema()

    def get(self, id):
        model = db.session.query(Study).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        study = db.session.query(Study).filter_by(id=id).first()

        if study is not None:
            elastic_index.remove_document(study, 'Study')

        db.session.query(StudyUser).filter_by(study_id=id).delete()
        db.session.query(StudyInvestigator).filter_by(study_id=id).delete()
        db.session.query(StudyCategory).filter_by(study_id=id).delete()
        db.session.query(Study).filter_by(id=id).delete()
        db.session.commit()
        return None

    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Study).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        elastic_index.update_document(updated, 'Study')
        return self.schema.dump(updated)


class StudyListEndpoint(flask_restful.Resource):

    studiesSchema = StudySchema(many=True)
    studySchema = StudySchema()

    def get(self):
        studies = db.session.query(Study).all()
        return self.studiesSchema.dump(studies)

    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.studySchema.load(request_data).data
            db.session.add(load_result)
            db.session.commit()
            elastic_index.add_document(load_result, 'Study')
            return self.studySchema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)


class StudyByStatusListEndpoint(flask_restful.Resource):
    studiesSchema = StudySchema(many=True)

    def get(self, status):
        studies = db.session.query(Study).filter_by(status=status).order_by(Study.last_updated.desc())
        return self.studiesSchema.dump(studies)
