import flask_restful
from flask import request
from marshmallow import ValidationError

from app import RestException, db
from app.model.study import Study
from app.resources.schema import StudySchema


class StudyEndpoint(flask_restful.Resource):

    schema = StudySchema()

    def get(self, id):
        model = db.session.query(Study).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        db.session.query(Study).filter_by(id=id).delete()
        db.session.commit()
        return None

    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Study).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        db.session.add(updated)
        db.session.commit()
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
            return self.studySchema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)
