import datetime

import flask_restful
from flask import request, g
from marshmallow import ValidationError
from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.interfaces import LoaderOption
from sqlalchemy.sql.base import ExecutableOption

from app.auth import auth
from app.database import session
from app.elastic_index import elastic_index
from app.enums import Role, Permission
from app.log_service import LogService
from app.models import Study, StudyInvestigator, StudyCategory, StudyUser, StudyChangeLog
from app.resources.CategoryEndpoint import add_joins_to_statement as add_cat_joins
from app.rest_exception import RestException
from app.schemas import SchemaRegistry
from app.utils.resource_utils import to_database_object_dict
from app.wrappers import requires_roles, requires_permission


def add_joins_to_statement(statement: Select | ExecutableOption) -> Select | LoaderOption:
    return statement.options(
        joinedload(Study.study_categories).joinedload(StudyCategory.category),
        add_cat_joins(joinedload(Study.categories)),
        joinedload(Study.study_investigators).joinedload(StudyInvestigator.investigator),
        joinedload(Study.investigators),
    )


def get_all_studies(filter_statement=None, with_joins=False) -> list[Study]:
    statement = select(Study)

    if with_joins:
        statement = add_joins_to_statement(statement)

    if filter_statement:
        statement = statement.filter(filter_statement)

    return session.execute(statement).unique().scalars().all()


def get_study_by_id(study_id: int, with_joins=False) -> Study:
    """
    Returns a Study matching the given ID from the database. Optionally include joins to Categories.

    CAUTION: Make sure to close the session after calling this function!
    """
    statement = select(Study)

    if with_joins:
        statement = add_joins_to_statement(statement)

    statement = statement.filter_by(id=study_id)
    return session.execute(statement).unique().scalar_one_or_none()


class StudyEndpoint(flask_restful.Resource):
    schema = SchemaRegistry.StudySchema()

    def get(self, study_id: int):
        model = get_study_by_id(study_id, with_joins=True)
        session.close()

        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_permission(Permission.edit_study)
    def delete(self, study_id: int):
        study = get_study_by_id(study_id, with_joins=False)

        if study is None:
            raise RestException(RestException.NOT_FOUND)

        study_title = study.title
        study_dict = to_database_object_dict(self.schema, study)
        elastic_index.remove_document(study_dict)
        session.query(StudyUser).filter_by(study_id=study_id).delete()
        session.query(StudyInvestigator).filter_by(study_id=study_id).delete()
        session.query(StudyCategory).filter_by(study_id=study_id).delete()
        session.query(Study).filter_by(id=study_id).delete()
        session.commit()

        LogService.log_study_change(study_id=study_id, study_title=study_title, change_type="delete")
        return None

    @auth.login_required
    @requires_permission(Permission.edit_study)
    def put(self, study_id: int):
        request_data = request.get_json()
        instance = get_study_by_id(study_id, with_joins=False)
        try:
            updated = self.schema.load(request_data, instance=instance)
        except Exception as errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.utcnow()
        session.add(updated)
        session.commit()
        elastic_index.update_document(document=to_database_object_dict(self.schema, updated))
        db_study = get_study_by_id(study_id, with_joins=True)

        LogService.log_study_change(study_id=study_id, study_title=db_study.title, change_type="edit")
        return self.schema.dump(db_study)


class StudyListEndpoint(flask_restful.Resource):

    studies_schema = SchemaRegistry.StudySchema(many=True)
    study_schema = SchemaRegistry.StudySchema()

    def get(self):
        studies = session.execute(add_joins_to_statement(select(Study))).unique().scalars().all()
        return self.studies_schema.dump(studies)

    @auth.login_required
    @requires_permission(Permission.edit_study)
    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.study_schema.load(request_data)
            session.add(load_result)
            session.commit()
            study_id = load_result.id
            session.close()

            db_study = get_study_by_id(study_id, with_joins=True)
            elastic_index.add_document(document=to_database_object_dict(self.study_schema, db_study))
            LogService.log_study_change(study_id=study_id, study_title=db_study.title, change_type="create")

            return self.study_schema.dump(db_study)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)


class StudyByStatusListEndpoint(flask_restful.Resource):
    studiesSchema = SchemaRegistry.StudySchema(many=True)

    def get(self, status):
        statement = add_joins_to_statement(select(Study)).filter_by(status=status).order_by(Study.last_updated.desc())
        studies = session.execute(statement).unique().scalars().all()
        return self.studiesSchema.dump(studies)


class StudyByAgeEndpoint(flask_restful.Resource):
    studiesSchema = SchemaRegistry.StudySchema(many=True)

    def get(self, status, age):
        statement = (
            add_joins_to_statement(select(Study))
            .filter_by(status=status)
            .filter(Study.ages.any(age))
            .order_by(Study.last_updated.desc())
        )
        studies = session.execute(statement).unique().scalars().all()
        return self.studiesSchema.dump(studies)
