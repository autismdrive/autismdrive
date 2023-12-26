import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError
from sqlalchemy import cast, Integer

from app.database import session
from app.elastic_index import elastic_index
from app.models import StudyUser
from app.models import Study, StudyInvestigator, StudyCategory, StudyUser
from app.rest_exception import RestException
from app.schemas import StudySchema


class StudyEndpoint(flask_restful.Resource):

    schema = StudySchema()

    def get(self, id):
        model = session.query(Study).filter_by(id=cast(id, Integer)).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        study = session.query(Study).filter_by(id=cast(id, Integer)).first()

        if study is not None:
            elastic_index.remove_document(study)

        session.query(StudyUser).filter_by(study_id=cast(id, Integer)).delete()
        session.query(StudyInvestigator).filter_by(study_id=cast(id, Integer)).delete()
        session.query(StudyCategory).filter_by(study_id=cast(id, Integer)).delete()
        session.query(Study).filter_by(id=cast(id, Integer)).delete()
        session.commit()
        return None

    def put(self, id):
        request_data = request.get_json()
        instance = session.query(Study).filter_by(id=cast(id, Integer)).first()
        try:
            updated = self.schema.load(request_data, instance=instance)
        except Exception as errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.utcnow()
        session.add(updated)
        session.commit()
        elastic_index.update_document(document=updated)
        return self.schema.dump(updated)


class StudyListEndpoint(flask_restful.Resource):

    studiesSchema = StudySchema(many=True)
    studySchema = StudySchema()

    def get(self):
        studies = session.query(Study).all()
        return self.studiesSchema.dump(studies)

    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.studySchema.load(request_data)
            session.add(load_result)
            session.commit()
            study_id = load_result.id
            session.close()

            db_study = session.query(Study).filter_by(id=cast(study_id, Integer)).first()
            elastic_index.add_document(document=db_study)
            return self.studySchema.dump(db_study)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)


class StudyByStatusListEndpoint(flask_restful.Resource):
    studiesSchema = StudySchema(many=True)

    def get(self, status):
        studies = session.query(Study).filter_by(status=status).order_by(Study.last_updated.desc())
        return self.studiesSchema.dump(studies)


class StudyByAgeEndpoint(flask_restful.Resource):
    studiesSchema = StudySchema(many=True)

    def get(self, status, age):
        # session.query(TestArr).filter(Any(2, TestArr.partners)).all()
        studies = (
            session.query(Study)
            .filter_by(status=status)
            .filter(Study.ages.any(age))
            .order_by(Study.last_updated.desc())
        )
        return self.studiesSchema.dump(studies)
