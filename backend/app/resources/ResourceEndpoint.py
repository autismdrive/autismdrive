import datetime

import flask_restful
from elasticsearch import NotFoundError
from flask import request, g
from marshmallow import ValidationError
from sqlalchemy import cast, Integer

from app.auth import auth
from app.database import session
from app.elastic_index import elastic_index
from app.models import AdminNote, Resource, ResourceCategory, Location, Event, UserFavorite, ResourceChangeLog
from app.models import ResourceCategory
from app.enums import Permission
from app.rest_exception import RestException
from app.schemas import ResourceSchema
from app.wrappers import requires_permission


class ResourceEndpoint(flask_restful.Resource):

    schema = ResourceSchema()

    def get(self, id):
        model = session.query(Resource).filter_by(id=cast(id, Integer)).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_permission(Permission.delete_resource)
    def delete(self, id):
        resource = session.query(Resource).filter_by(id=cast(id, Integer)).first()
        resource_id = resource.id
        resource_title = resource.title

        try:
            elastic_index.remove_document(resource)
        except NotFoundError:
            pass

        session.query(AdminNote).filter_by(resource_id=cast(id, Integer)).delete()
        session.query(Event).filter_by(id=cast(id, Integer)).delete()
        session.query(Location).filter_by(id=cast(id, Integer)).delete()
        session.query(ResourceCategory).filter_by(resource_id=cast(id, Integer)).delete()
        session.query(UserFavorite).filter_by(resource_id=cast(id, Integer)).delete()
        session.query(Resource).filter_by(id=cast(id, Integer)).delete()
        session.commit()
        self.log_update(resource_id=resource_id, resource_title=resource_title, change_type="delete")
        return None

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def put(self, id):
        request_data = request.get_json()
        instance = session.query(Resource).filter_by(id=cast(id, Integer)).first()
        try:
            updated = self.schema.load(request_data, instance=instance, session=session)
        except Exception as e:
            raise RestException(RestException.INVALID_OBJECT, details=e)
        updated.last_updated = datetime.datetime.utcnow()
        session.add(updated)
        session.commit()
        elastic_index.update_document(document=updated)
        self.log_update(resource_id=updated.id, resource_title=updated.title, change_type="edit")
        return self.schema.dump(updated)

    def log_update(self, resource_id, resource_title, change_type):
        log = ResourceChangeLog(
            resource_id=resource_id,
            resource_title=resource_title,
            user_id=g.user.id,
            user_email=g.user.email,
            type=change_type,
        )
        session.add(log)
        session.commit()


class ResourceListEndpoint(flask_restful.Resource):

    resourcesSchema = ResourceSchema(many=True)
    resourceSchema = ResourceSchema()

    def get(self):
        resources = session.query(Resource).all()
        return self.resourcesSchema.dump(resources)

    @auth.login_required
    @requires_permission(Permission.create_resource)
    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.resourceSchema.load(request_data)
            session.add(load_result)
            session.commit()
            db_resource = session.query(Resource).filter(Resource.id == cast(load_result.id, Integer)).first()
            elastic_index.add_document(document=db_resource)
            self.log_update(resource_id=db_resource.id, resource_title=db_resource.title, change_type="create")
            return self.resourceSchema.dump(db_resource)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)

    def log_update(self, resource_id, resource_title, change_type):
        log = ResourceChangeLog(
            resource_id=resource_id,
            resource_title=resource_title,
            user_id=g.user.id,
            user_email=g.user.email,
            type=change_type,
        )
        session.add(log)
        session.commit()


class EducationResourceListEndpoint(flask_restful.Resource):

    resourcesSchema = ResourceSchema(many=True)

    def get(self):
        resources = (
            session.query(Resource)
            .filter_by(is_uva_education_content=True, is_draft=False)
            .order_by(Resource.last_updated.desc())
            .all()
        )
        return self.resourcesSchema.dump(resources)


class Covid19ResourceListEndpoint(flask_restful.Resource):

    resourcesSchema = ResourceSchema(many=True)

    def get(self, category):
        resources = (
            session.query(Resource)
            .filter(Resource.covid19_categories.any(category), Resource.is_draft == False)
            .order_by(Resource.last_updated.desc())
            .all()
        )
        return self.resourcesSchema.dump(resources)
