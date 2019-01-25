import datetime
import importlib
import flask_restful
from flask import request
from sqlalchemy.exc import IntegrityError

from app import db, RestException


# The Questionnaire Endpoint expects a "type" that is the exact Class name of a file
# located in the Questionnaire Package. It should have the following properties:
#   * It is saved in a snaked cased file of the same name as the class.
#   * It extends db.Model
#   * it has an id field called "id"
#   * It has a date field called "last_updated"
#   * When calling the endpoint, use the snakecase format of the name.

class QuestionnaireEndpoint(flask_restful.Resource):

    QUESTION_PACKAGE = "app.model.questionnaires"

    def get(self, name, id):
        class_ref = self.get_class(name)
        instance = db.session.query(class_ref).filter(class_ref.id == id).first()
        if instance is None:
            raise RestException(RestException.NOT_FOUND)
        schema = self.get_schema(name)
        return schema.dump(instance)

    def delete(self, name, id):
        try:
            class_ref = self.get_class(name)
            db.session.query(class_ref).filter(class_ref.id == id).delete()
            db.session.commit()
        except IntegrityError as error:
            raise RestException(RestException.CAN_NOT_DELETE)
        return

    def put(self, name, id):
        class_ref = self.get_class(name)
        instance = db.session.query(class_ref).filter(class_ref.id == id).first()
        schema = self.get_schema(name)
        request_data = request.get_json()
        updated, errors = schema.load(request_data, instance=instance, session=db.session)
        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        return schema.dump(updated)

    @staticmethod
    def get_class(name):
        module_name = QuestionnaireEndpoint.QUESTION_PACKAGE + "." + name;
        class_name = QuestionnaireEndpoint.camel_case_it(name)
        return QuestionnaireEndpoint.str_to_class(module_name, class_name)

    @staticmethod
    def get_schema(name, many=False):
        module_name = QuestionnaireEndpoint.QUESTION_PACKAGE + "." + name
        schema_name = QuestionnaireEndpoint.camel_case_it(name) + "Schema"
        return QuestionnaireEndpoint.str_to_class(module_name, schema_name)(many=many)

    @staticmethod
    def get_meta_schema(name):
        module_name = QuestionnaireEndpoint.QUESTION_PACKAGE + "." + name
        schema_name = QuestionnaireEndpoint.camel_case_it(name) + "MetaSchema"
        return QuestionnaireEndpoint.str_to_class(module_name, schema_name)()

    @staticmethod
    def camel_case_it(name):
        first, *rest = name.split('_')
        return first.capitalize() + ''.join(word.capitalize() for word in rest)

    # Given a string, creates an instance of that class
    @staticmethod
    def str_to_class(module_name, class_name):
        try:
            module_ = importlib.import_module(module_name)
            try:
                return getattr(module_, class_name)
            except AttributeError:
                # FIXME: Get some damn logging.
                print("Error class does not exist:" + class_name)
                # logging.ERROR('Class does not exist')
        except ImportError:
            # FIXME: Get some damn logging.
            print("Module does not exist:" + module_name)
            #   logging.('Module does not exist')
        return None


class QuestionnaireListEndpoint(flask_restful.Resource):

    def get(self, name):
        class_ref = QuestionnaireEndpoint.get_class(name)
        schema = QuestionnaireEndpoint.get_schema(name, many=True)
        questionnaires = db.session.query(class_ref).all()
        return schema.dump(questionnaires)

    def post(self, name):
        request_data = request.get_json()
        schema = QuestionnaireEndpoint.get_schema(name)
        new_quest, errors = schema.load(request_data, session=db.session)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        db.session.add(new_quest)
        db.session.commit()
        return schema.dump(new_quest)


class QuestionnaireMetaEndpoint(flask_restful.Resource):

    def get(self, name):
        schema = QuestionnaireEndpoint.get_meta_schema(name)
        class_ref = QuestionnaireEndpoint.get_class(name)
        questionnaire = db.session.query(class_ref).first()
        return schema.dump(questionnaire)
