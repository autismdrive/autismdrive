import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError
from sqlalchemy import select, Select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.interfaces import LoaderOption
from sqlalchemy.sql.base import ExecutableOption

from app.auth import auth
from app.database import session
from app.elastic_index import elastic_index
from app.enums import Permission
from app.log_service import LogService
from app.models import AdminNote, Resource, Location, Event, UserFavorite, ResourceCategory
from app.resources.CategoryEndpoint import add_joins_to_statement as add_cat_joins
from app.rest_exception import RestException
from app.schemas import SchemaRegistry
from app.utils.resource_utils import to_database_object_dict
from app.wrappers import requires_permission


def add_joins_to_statement(statement: Select | ExecutableOption) -> Select | LoaderOption:
    return statement.options(
        joinedload(Resource.resource_categories).joinedload(ResourceCategory.category),
        add_cat_joins(joinedload(Resource.categories)),
    )


def get_all_resources(filter_statement=None, with_joins=False) -> list[Resource]:
    statement = select(Resource)

    if with_joins:
        statement = add_joins_to_statement(statement)

    if filter_statement:
        statement = statement.filter(filter_statement)

    return session.execute(statement).unique().scalars().all()


def get_resource_by_id(resource_id: int, with_joins=False) -> Resource:
    """
    Returns a Resource matching the given ID from the database. Optionally include joins to Categories.

    CAUTION: Make sure to close the session after calling this function!
    """
    statement = select(Resource)

    if with_joins:
        statement = add_joins_to_statement(statement)

    statement = statement.filter_by(id=resource_id)
    return session.execute(statement).unique().scalar_one_or_none()


class ResourceEndpoint(flask_restful.Resource):

    schema = SchemaRegistry.ResourceSchema()

    def get(self, resource_id: int):
        model = get_resource_by_id(resource_id, with_joins=True)
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_permission(Permission.delete_resource)
    def delete(self, resource_id: int):
        resource = get_resource_by_id(resource_id, with_joins=False)

        if resource is None:
            raise RestException(RestException.NOT_FOUND)

        resource_title = resource.title
        resource_dict = to_database_object_dict(self.schema, resource)

        elastic_index.remove_document(resource_dict)
        session.query(AdminNote).filter_by(resource_id=resource_id).delete()
        session.query(Event).filter_by(id=resource_id).delete()
        session.query(Location).filter_by(id=resource_id).delete()
        session.query(ResourceCategory).filter_by(resource_id=resource_id).delete()
        session.query(UserFavorite).filter_by(resource_id=resource_id).delete()
        session.query(Resource).filter_by(id=resource_id).delete()
        session.commit()
        LogService.log_resource_change(resource_id=resource_id, resource_title=resource_title, change_type="delete")
        return None

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def put(self, resource_id: int):
        request_data = request.get_json()
        instance = get_resource_by_id(resource_id, with_joins=False)
        try:
            updated = self.schema.load(request_data, instance=instance, session=session)
        except Exception as e:
            raise RestException(RestException.INVALID_OBJECT, details=e)
        updated.last_updated = datetime.datetime.utcnow()
        session.add(updated)
        session.commit()
        elastic_index.update_document(document=to_database_object_dict(self.schema, updated))
        LogService.log_resource_change(resource_id=updated.id, resource_title=updated.title, change_type="edit")
        return self.schema.dump(updated)


class ResourceListEndpoint(flask_restful.Resource):

    resources_schema = SchemaRegistry.ResourceSchema(many=True)
    resource_schema = SchemaRegistry.ResourceSchema()

    def get(self):
        statement = add_joins_to_statement(select(Resource))
        resources = session.execute(statement).unique().scalars().all()
        return self.resources_schema.dump(resources)

    @auth.login_required
    @requires_permission(Permission.create_resource)
    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.resource_schema.load(request_data)
            session.add(load_result)
            session.commit()

            db_resource = get_resource_by_id(load_result.id, with_joins=True)

            elastic_index.add_document(document=to_database_object_dict(self.resource_schema, db_resource))
            LogService.log_resource_change(
                resource_id=db_resource.id, resource_title=db_resource.title, change_type="create"
            )
            return self.resource_schema.dump(db_resource)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)


class EducationResourceListEndpoint(flask_restful.Resource):

    resourcesSchema = SchemaRegistry.ResourceSchema(many=True)

    def get(self):
        statement = add_joins_to_statement(select(Resource))

        resources = (
            session.execute(
                statement.filter_by(is_uva_education_content=True, is_draft=False).order_by(
                    Resource.last_updated.desc()
                )
            )
            .unique()
            .scalars()
            .all()
        )
        return self.resourcesSchema.dump(resources)


class Covid19ResourceListEndpoint(flask_restful.Resource):

    resourcesSchema = SchemaRegistry.ResourceSchema(many=True)

    def get(self, category):
        statement = add_joins_to_statement(select(Resource))

        resources = (
            session.execute(
                statement.filter(Resource.covid19_categories.any(category))
                .filter_by(is_draft=False)
                .order_by(Resource.last_updated.desc())
            )
            .unique()
            .scalars()
            .all()
        )
        return self.resourcesSchema.dump(resources)
