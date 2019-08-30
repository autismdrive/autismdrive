import datetime
import flask_restful
import os

from dateutil.tz import tzutc
from flask import request
from sqlalchemy.exc import IntegrityError
from app import app, db, RestException, auth
from app.export_service import ExportService
from app.export_xls_service import ExportXlsService
from app.model.export_info import ExportInfoSchema
from app.model.user import Role
from app.wrappers import requires_roles

# The Questionnaire Endpoint expects a "type" that is the exact Class name of a file
# located in the Questionnaire Package. It should have the following properties:
#   * It is saved in a snaked cased file of the same name as the class.
#   * It extends db.Model
#   * it has an id field called "id"
#   * It has a date field called "last_updated"
#   * When calling the endpoint, use the snakecase format of the name.

class QuestionnaireEndpoint(flask_restful.Resource):

    @auth.login_required
    def get(self, name, id):
        name = ExportService.camel_case_it(name)
        class_ref = ExportService.get_class(name)
        instance = db.session.query(class_ref).filter(class_ref.id == id).first()
        if instance is None:
            raise RestException(RestException.NOT_FOUND)
        schema = ExportService.get_schema(name)
        return schema.dump(instance)

    @auth.login_required
    def delete(self, name, id):
        try:
            name = ExportService.camel_case_it(name)
            class_ref = ExportService.get_class(name)
            instance = db.session.query(class_ref).filter(class_ref.id == id).first()
            db.session.delete(instance)
#            db.session.query(class_ref).filter(class_ref.id == id).delete()
            db.session.commit()
        except IntegrityError as error:
            raise RestException(RestException.CAN_NOT_DELETE)
        return

    @auth.login_required
    def put(self, name, id):
        name = ExportService.camel_case_it(name)
        class_ref = ExportService.get_class(name)
        instance = db.session.query(class_ref).filter(class_ref.id == id).first()
        schema = ExportService.get_schema(name, session=db.session)
        request_data = request.get_json()
        if "_links" in request_data:
            request_data.pop("_links")
        updated, errors = schema.load(request_data, instance=instance)

        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now(tz=tzutc())
        db.session.add(updated)
        db.session.commit()
        return schema.dump(updated)


class QuestionnaireListEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, name):
        name = ExportService.camel_case_it(name)
        class_ref = ExportService.get_class(name)
        schema = ExportService.get_schema(name, many=True)
        questionnaires = db.session.query(class_ref).all()
        return schema.dump(questionnaires)


class QuestionnaireListMetaEndpoint(flask_restful.Resource):
    # Used for data export to get meta without specifying flow and relationship
    def get(self, name):
        name = ExportService.camel_case_it(name)
        class_ref = ExportService.get_class(name)
        questionnaire = class_ref()
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


class QuestionnaireInfoEndpoint(flask_restful.Resource):

    def get(self):

        info_list = ExportService.get_table_info()
        info_list = [item for item in info_list if item.question_type]
        info_list = sorted(info_list, key=lambda item: item.table_name)
        return ExportInfoSchema(many=True).dump(info_list)


class QuestionnaireDataExportEndpoint(flask_restful.Resource):

    @staticmethod
    def request_wants_json():
        best = request.accept_mimetypes \
            .best_match(['application/json', 'text/html'])
        return best == 'application/json' and \
               request.accept_mimetypes[best] > \
               request.accept_mimetypes['text/html']

    @auth.login_required
    @requires_roles(Role.admin)
    def get(self, name):
        name = ExportService.camel_case_it(name)
        if self.request_wants_json():
            schema = ExportService.get_schema(name, many=True)
            return schema.dump(ExportService().get_data(name))
        else:
            return ExportXlsService.export_xls(name=name, app=app)
