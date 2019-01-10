import flask_restful
from flask import request
from sqlalchemy.exc import IntegrityError

from app import db, RestException
from app.model.contact_questionnaire import ContactQuestionnaire
from app.resources.schema import ContactQuestionnaireSchema, ContactQuestionnaireMetaSchema


class ContactQuestionnaireEndpoint(flask_restful.Resource):
    schema = ContactQuestionnaireSchema()

    def get(self, id):
        contact_questionnaire = db.session.query(ContactQuestionnaire).filter(ContactQuestionnaire.id == id).first()
        if contact_questionnaire is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(contact_questionnaire)

    def delete(self, id):
        try:
            db.session.query(ContactQuestionnaire).filter(ContactQuestionnaire.id == id).delete()
            db.session.commit()
        except IntegrityError as error:
            raise RestException(RestException.CAN_NOT_DELETE)
        return

    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(ContactQuestionnaire).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)


class ContactQuestionnaireListEndpoint(flask_restful.Resource):
    contact_questionnaire_schema = ContactQuestionnaireSchema()
    contact_questionnaires_schema = ContactQuestionnaireSchema(many=True)

    def get(self):
        contact_questionnaires = db.session.query(ContactQuestionnaire).all()
        return self.contact_questionnaires_schema.dump(contact_questionnaires)

    def post(self):
        request_data = request.get_json()
        new_quest, errors = self.contact_questionnaire_schema.load(request_data)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        db.session.add(new_quest)
        db.session.commit()
        return self.contact_questionnaire_schema.dump(new_quest)


class ContactQuestionnaireMetaEndpoint(flask_restful.Resource):
    contact_questionnaire_meta_schema = ContactQuestionnaireMetaSchema()

    def get(self):
        contact_questionnaire = db.session.query(ContactQuestionnaire).first()
        return self.contact_questionnaire_meta_schema.dump(contact_questionnaire)
