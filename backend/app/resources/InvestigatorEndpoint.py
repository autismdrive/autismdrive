import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError

from app import RestException, db
from app.model.investigator import Investigator
from app.model.study_investigator import StudyInvestigator
from app.schema.schema import InvestigatorSchema


class InvestigatorEndpoint(flask_restful.Resource):

    schema = InvestigatorSchema()

    def get(self, id):
        model = db.session.query(Investigator).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        db.session.query(StudyInvestigator).filter_by(investigator_id=id).delete()
        db.session.query(Investigator).filter_by(id=id).delete()
        db.session.commit()
        return None

    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Investigator).filter_by(id=id).first()

        try:
            updated = self.schema.load(request_data, instance=instance)
        except Exception as errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)

        updated.last_updated = datetime.datetime.utcnow()
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)


class InvestigatorListEndpoint(flask_restful.Resource):

    investigatorsSchema = InvestigatorSchema(many=True)
    investigatorSchema = InvestigatorSchema()

    def get(self):
        investigators = db.session.query(Investigator).order_by(Investigator.name).all()
        return self.investigatorsSchema.dump(investigators)

    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.investigatorSchema.load(request_data)
            model = db.session.query(Investigator).filter_by(name=load_result.name).first()
            if model:
                return self.investigatorSchema.dump(model)
            else:
                db.session.add(load_result)
                db.session.commit()
            return self.investigatorSchema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)
