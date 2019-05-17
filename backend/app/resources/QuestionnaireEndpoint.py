import datetime
import flask_restful
import os
from flask import request
from sqlalchemy.exc import IntegrityError
from app import app, db, RestException, auth
from app.model.user import Role
from app.wrappers import requires_roles
from data_export_service import DataExport

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


class QuestionnaireListEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, name):
        class_ref = QuestionService.get_class(name)
        schema = QuestionService.get_schema(name, many=True)
        questionnaires = db.session.query(class_ref).all()
        return schema.dump(questionnaires)


class QuestionnaireListMetaEndpoint(flask_restful.Resource):

    def get(self, name):
        class_ref = QuestionService.get_class(name)
        questionnaire = db.session.query(class_ref).first()
        meta = {"table": {}}
        try:
            meta["table"]['question_type'] = questionnaire.__question_type__
            meta["table"]["label"] = questionnaire.__label__
        except:
            pass  # If these fields don't exist, just keep going.
        meta["fields"] = []

        # This will move fields referenced by the field groups into the group, but will otherwise add them
        # the base meta object if they are not contained within a group.
        for c in questionnaire.__table__.columns:
            if c.info:
                c.info['name'] = c.name
                c.info['key'] = c.name
                meta['fields'].append(c.info)
            elif c.type.python_type == datetime.datetime:
                meta['fields'].append({'name': c.name, 'key': c.name, 'display_order': 0, 'type': 'DATETIME'})
            else:
                meta['fields'].append({'name': c.name, 'key': c.name, 'display_order': 0})

        # Sort the fields
        meta['fields'] = sorted(meta['fields'], key=lambda field: field['display_order'])

        return meta


class QuestionnaireNamesEndpoint(flask_restful.Resource):

    def get(self):
        all_file_names = os.listdir(os.path.dirname(app.instance_path) + '/app/model/questionnaires')
        non_questionnaires = ['mixin', '__']
        questionnaire_file_names = []
        for index, file_name in enumerate(all_file_names):
            if any(string in file_name for string in non_questionnaires):
                pass
            else:
                f = file_name.replace(".py", "")
                questionnaire_file_names.append(f)
        return sorted(questionnaire_file_names)


class QuestionnaireDataExportEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, name):
        return DataExport.export(name=name, app=app)
