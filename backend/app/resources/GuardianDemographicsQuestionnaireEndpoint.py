import flask_restful
import datetime
from flask import request
from sqlalchemy.exc import IntegrityError

from app import db, RestException
from app.model.guardian_demographics_questionnaire import GuardianDemographicsQuestionnaire
from app.resources.schema import GuardianDemographicsQuestionnaireSchema


class GuardianDemographicsQuestionnaireEndpoint(flask_restful.Resource):
    schema = GuardianDemographicsQuestionnaireSchema()

    def get(self, id):
        guardian_demographics_questionnaire = db.session.query(GuardianDemographicsQuestionnaire).filter(GuardianDemographicsQuestionnaire.id == id).first()
        if guardian_demographics_questionnaire is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(guardian_demographics_questionnaire)

    def delete(self, id):
        try:
            db.session.query(GuardianDemographicsQuestionnaire).filter(GuardianDemographicsQuestionnaire.id == id).delete()
            db.session.commit()
        except IntegrityError as error:
            raise RestException(RestException.CAN_NOT_DELETE)
        return

    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(GuardianDemographicsQuestionnaire).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)


class GuardianDemographicsQuestionnaireListEndpoint(flask_restful.Resource):
    guardian_demographics_questionnaire_schema = GuardianDemographicsQuestionnaireSchema()
    guardian_demographics_questionnaires_schema = GuardianDemographicsQuestionnaireSchema(many=True)

    def get(self):
        guardian_demographics_questionnaires = db.session.query(GuardianDemographicsQuestionnaire).all()
        return self.guardian_demographics_questionnaires_schema.dump(guardian_demographics_questionnaires)

    def post(self):
        request_data = request.get_json()
        new_quest, errors = self.guardian_demographics_questionnaire_schema.load(request_data)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        db.session.add(new_quest)
        db.session.commit()
        return self.guardian_demographics_questionnaire_schema.dump(new_quest)
