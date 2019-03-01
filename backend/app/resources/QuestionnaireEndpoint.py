import datetime
import flask_restful
from flask import request
from sqlalchemy.exc import IntegrityError
from app import db, RestException, auth

# The Questionnaire Endpoint expects a "type" that is the exact Class name of a file
# located in the Questionnaire Package. It should have the following properties:
#   * It is saved in a snaked cased file of the same name as the class.
#   * It extends db.Model
#   * it has an id field called "id"
#   * It has a date field called "last_updated"
#   * When calling the endpoint, use the snakecase format of the name.
from app.question_service import QuestionService


class QuestionnaireEndpoint(flask_restful.Resource):

    @auth.login_required
    def get(self, name, id):
        class_ref = QuestionService.get_class(name)
        instance = db.session.query(class_ref).filter(class_ref.id == id).first()
        if instance is None:
            raise RestException(RestException.NOT_FOUND)
        schema = QuestionService.get_schema(name)
        return schema.dump(instance)

    @auth.login_required
    def delete(self, name, id):
        try:
            class_ref = QuestionService.get_class(name)
            instance = db.session.query(class_ref).filter(class_ref.id == id).first()
            db.session.delete(instance)
#            db.session.query(class_ref).filter(class_ref.id == id).delete()
            db.session.commit()
        except IntegrityError as error:
            raise RestException(RestException.CAN_NOT_DELETE)
        return

    @auth.login_required
    def put(self, name, id):
        class_ref = QuestionService.get_class(name)
        instance = db.session.query(class_ref).filter(class_ref.id == id).first()
        schema = QuestionService.get_schema(name, session=db.session)
        request_data = request.get_json()
        updated, errors = schema.load(request_data, instance=instance)
        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        return schema.dump(updated)



