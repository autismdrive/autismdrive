import copy
import datetime

import flask_restful
from flask import request
from marshmallow import EXCLUDE
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.auth import auth
from app.database import session, get_class
from app.enums import Permission
from app.export_service import ExportService
from app.export_xls_service import ExportXlsService
from app.models import ChainSession, ChainQuestionnaire, ChainSessionStep
from app.rest_exception import RestException
from app.schemas import ExportInfoSchema
from app.utils import pascal_case_it, patch_dict
from app.wrappers import requires_permission


# The Questionnaire Endpoint expects a "type" that is the exact Class name of a file
# located in the Questionnaire Package. It should have the following properties:
#   * It is saved in a snaked cased file of the same name as the class.
#   * It extends db.Model
#   * it has an id field called "id"
#   * It has a date field called "last_updated"
#   * When calling the endpoint, use the snakecase format of the name.


class QuestionnaireEndpoint(flask_restful.Resource):
    @auth.login_required
    def get(self, name, questionnaire_id: int):
        """
        Returns a single questionnaire record.

        Parameters:
            name (str):
                Snake-cased name of the questionnaire class (should also match the table name),
                found in app.model.questionnaires.
                E.g., clinical_diagnoses_questionnaire -> ClinicalDiagnosesQuestionnaire

            questionnaire_id (int): ID of the questionnaire record to retrieve

        Returns: A single questionnaire record.
        """
        name = pascal_case_it(name)
        class_ref = get_class(name)
        instance = (
            session.execute(select(class_ref).filter(class_ref.id == questionnaire_id)).unique().scalar_one_or_none()
        )
        if instance is None:
            raise RestException(RestException.NOT_FOUND)
        schema = ExportService.get_schema(name)
        return schema.dump(instance)

    @auth.login_required
    def delete(self, name, questionnaire_id: int):
        """
        Deletes a single questionnaire record.

        Parameters:
            name (str):
                Snake-cased name of the questionnaire class (should also match the table name),
                found in app.model.questionnaires.
                E.g., clinical_diagnoses_questionnaire -> ClinicalDiagnosesQuestionnaire

            questionnaire_id (int): ID of the questionnaire record to delete
        """
        try:
            name = pascal_case_it(name)
            class_ref = get_class(name)
            instance = session.scalars(select(class_ref).filter_by(id=questionnaire_id)).first()

            if instance is not None:
                session.delete(instance)
                session.commit()
        except IntegrityError as error:
            raise RestException(RestException.CAN_NOT_DELETE, details=error)
        finally:
            session.close()

        return "", 200

    @auth.login_required
    def put(self, name, questionnaire_id: int):
        """
        Modifies an existing questionnaire record.

        Parameters:
            name (str):
                Snake-cased name of the questionnaire class (should also match the table name),
                found in app.model.questionnaires.
                E.g., clinical_diagnoses_questionnaire -> ClinicalDiagnosesQuestionnaire

            questionnaire_id (int): ID of the questionnaire record to retrieve

        Returns: The updated questionnaire record.
        """
        name = pascal_case_it(name)
        class_ref = get_class(name)
        # statement = select(class_ref)
        #
        # if name == "ChainQuestionnaire":
        #     statement = statement.options(
        #         joinedload(ChainQuestionnaire.sessions).options(
        #             joinedload(ChainSession.step_attempts).options(joinedload(ChainSessionStep.challenging_behaviors))
        #         )
        #     )

        try:
            instance = (
                session.query(class_ref)
                .populate_existing()
                .with_for_update(nowait=True, of=class_ref)
                .filter_by(id=questionnaire_id)
                .first()
            )
        except Exception as error:
            raise RestException(RestException.NOT_FOUND, details=error)

        schema = ExportService.get_schema(name)
        request_dict: dict = request.get_json()

        try:
            updated = schema.load(request_dict, instance=instance, unknown=EXCLUDE)
        except Exception as error:
            raise RestException(RestException.INVALID_OBJECT, details=error)

        try:
            session.add(updated)
            session.commit()
        except IntegrityError as error:
            raise RestException(RestException.INVALID_OBJECT, details=error)

        return schema.dump(updated)


class QuestionnaireListEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.data_admin)
    def get(self, name):
        name = pascal_case_it(name)
        class_ref = get_class(name)
        schema = ExportService.get_schema(name, many=True)
        questionnaires = session.query(class_ref).all()
        return schema.dump(questionnaires)


class QuestionnaireListMetaEndpoint(flask_restful.Resource):
    def get(self, name):
        """
        Retrieves metadata about the given questionnaire name. Includes JSON Formly field definition.
        Used for data export to get meta without specifying flow and relationship.

        Returns:
            A dict object containing the metadata about the questionnaire. Example:
            {
                table: {
                    question_type: "sensitive",
                    label: "Clinical Diagnosis"
                },
                fields: [
                    {
                    name: "id",
                    key: "id",
                    display_order: 0
                    },
                    ...
                ]
            }
        """
        name = pascal_case_it(name)
        class_ref = get_class(name)
        questionnaire = class_ref()
        meta = {"table": {}}
        try:
            meta["table"]["question_type"] = questionnaire.__question_type__
            meta["table"]["label"] = questionnaire.__label__
        except:
            pass  # If these fields don't exist, just keep going.
        meta["fields"] = []

        # This will move fields referenced by the field groups into the group, but will otherwise add them
        # the base meta object if they are not contained within a group.
        for c in questionnaire.__table__.columns:
            if c.info:
                c.info["name"] = c.name
                c.info["key"] = c.name
                meta["fields"].append(c.info)
            elif c.type.python_type == datetime.datetime:
                meta["fields"].append({"name": c.name, "key": c.name, "display_order": 0, "type": "DATETIME"})
            else:
                meta["fields"].append({"name": c.name, "key": c.name, "display_order": 0})

        # Sort the fields
        meta["fields"] = sorted(meta["fields"], key=lambda field: field["display_order"])

        return meta


class QuestionnaireInfoEndpoint(flask_restful.Resource):
    def get(self):
        """
        Lists available questionnaires. Used for data export to get meta without specifying flow and relationship.

        Returns:
            list[ExportInfoSchema] - A list of dict objects, including the following info for each questionnaire:
                table_name (str): Snake-case database table name. E.g., "chain_session_questionnaire",
                class_name (str): Pascal-case class name for Model class. E.g., "ChainSession",
                display_name (str): Questionnaire title. E.g., "Chain Session Assessment",
                size (int): Number of questionnaire records in the database,
                url (str): Export endpoint. E.g., "/api/export/chain_session_questionnaire",
                question_type (str): 'sensitive' | 'identifying' | 'unrestricted' | 'sub-table'
                sub_tables (list[ExportInfoSchema]): A list of sub-tables within this table, if applicable.
        """
        info_list = ExportService.get_table_info()
        info_list = [item for item in info_list if item.question_type]
        info_list = sorted(info_list, key=lambda item: item.table_name)
        return ExportInfoSchema(many=True).dump(info_list)


class QuestionnaireDataExportEndpoint(flask_restful.Resource):
    @staticmethod
    def request_wants_json():
        best = request.accept_mimetypes.best_match(["application/json", "text/html"])
        return best == "application/json" and request.accept_mimetypes[best] > request.accept_mimetypes["text/html"]

    @auth.login_required
    @requires_permission(Permission.data_admin)
    def get(self, name):
        from flask import current_app

        name = pascal_case_it(name)
        if self.request_wants_json():
            schema = ExportService.get_schema(name, many=True)
            return schema.dump(ExportService().get_data(name))
        else:
            return ExportXlsService.export_xls(name=name, app=current_app)


class QuestionnaireUserDataExportEndpoint(flask_restful.Resource):
    @staticmethod
    def request_wants_json():
        best = request.accept_mimetypes.best_match(["application/json", "text/html"])
        return best == "application/json" and request.accept_mimetypes[best] > request.accept_mimetypes["text/html"]

    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, name, user_id):
        from flask import current_app

        name = pascal_case_it(name)
        if self.request_wants_json():
            schema = ExportService.get_schema(name, many=True)
            return schema.dump(ExportService().get_data(name))
        else:
            return ExportXlsService.export_xls(name=name, user_id=user_id, app=current_app)
