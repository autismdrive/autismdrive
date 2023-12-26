import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError
from sqlalchemy import cast, Integer

from app.database import session
from app.models import Investigator, StudyInvestigator
from app.rest_exception import RestException
from app.schemas import InvestigatorSchema


class InvestigatorEndpoint(flask_restful.Resource):

    schema = InvestigatorSchema()

    def get(self, id):
        model = session.query(Investigator).filter_by(id=cast(id, Integer)).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        session.query(StudyInvestigator).filter_by(investigator_id=cast(id, Integer)).delete()
        session.query(Investigator).filter_by(id=cast(id, Integer)).delete()
        session.commit()
        return None

    def put(self, id):
        request_data = request.get_json()
        instance = session.query(Investigator).filter_by(id=cast(id, Integer)).first()

        try:
            updated = self.schema.load(request_data, instance=instance)
        except Exception as errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)

        updated.last_updated = datetime.datetime.utcnow()
        session.add(updated)
        session.commit()
        return self.schema.dump(updated)


class InvestigatorListEndpoint(flask_restful.Resource):

    investigatorsSchema = InvestigatorSchema(many=True)
    investigatorSchema = InvestigatorSchema()

    def get(self):
        investigators = session.query(Investigator).order_by(Investigator.name).all()
        return self.investigatorsSchema.dump(investigators)

    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.investigatorSchema.load(request_data)
            model = session.query(Investigator).filter_by(name=load_result.name).first()
            if model:
                return self.investigatorSchema.dump(model)
            else:
                session.add(load_result)
                session.commit()
            return self.investigatorSchema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT, details=err.messages)
