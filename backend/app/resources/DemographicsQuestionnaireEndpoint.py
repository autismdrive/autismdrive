import flask_restful
import datetime
from flask import request
from sqlalchemy.exc import IntegrityError

from app import db, RestException
from app.model.demographics_questionnaire import DemographicsQuestionnaire
from app.resources.schema import DemographicsQuestionnaireSchema


class DemographicsQuestionnaireEndpoint(flask_restful.Resource):
    schema = DemographicsQuestionnaireSchema()

    def get(self, id):
        demographics_questionnaire = db.session.query(DemographicsQuestionnaire).filter(DemographicsQuestionnaire.id == id).first()
        if demographics_questionnaire is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(demographics_questionnaire)

    def delete(self, id):
        try:
            db.session.query(DemographicsQuestionnaire).filter(DemographicsQuestionnaire.id == id).delete()
            db.session.commit()
        except IntegrityError as error:
            raise RestException(RestException.CAN_NOT_DELETE)
        return

    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(DemographicsQuestionnaire).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)


class DemographicsQuestionnaireListEndpoint(flask_restful.Resource):
    demographics_questionnaire_schema = DemographicsQuestionnaireSchema()
    demographics_questionnaires_schema = DemographicsQuestionnaireSchema(many=True)

    def get(self):
        demographics_questionnaires = db.session.query(DemographicsQuestionnaire).all()
        return self.demographics_questionnaires_schema.dump(demographics_questionnaires)

    def post(self):
        request_data = request.get_json()
        new_quest, errors = self.demographics_questionnaire_schema.load(request_data)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        db.session.add(new_quest)
        db.session.commit()
        return self.demographics_questionnaire_schema.dump(new_quest)
