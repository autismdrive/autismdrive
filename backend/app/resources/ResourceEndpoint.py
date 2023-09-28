import datetime

import flask_restful
from elasticsearch import NotFoundError
from flask import request, g
from marshmallow import ValidationError

from app.auth import auth
from app.database import session
from app.elastic_index import elastic_index
from app.model.admin_note import AdminNote
from app.model.event import Event
from app.model.location import Location
from app.model.resource import Resource, ResourceCategory
from app.model.resource_change_log import ResourceChangeLog
from app.model.role import Permission
from app.model.user_favorite import UserFavorite
from app.rest_exception import RestException
from app.schema.schema import ResourceSchema
from app.wrappers import requires_permission


class ResourceEndpoint(flask_restful.Resource):

    schema = ResourceSchema()

    def get(self, id):
        model = session.query(Resource).filter_by(id=id).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_permission(Permission.delete_resource)
    def delete(self, id):
        resource = session.query(Resource).filter_by(id=id).first()
        resource_id = resource.id
        resource_title = resource.title

        try:
            elastic_index.remove_document(resource, "Resource")
        except NotFoundError:
            pass

        session.query(AdminNote).filter_by(resource_id=id).delete()
        session.query(Event).filter_by(id=id).delete()
        session.query(Location).filter_by(id=id).delete()
        session.query(ResourceCategory).filter_by(resource_id=id).delete()
        session.query(UserFavorite).filter_by(resource_id=id).delete()
        session.query(Resource).filter_by(id=id).delete()
        session.commit()
        self.log_update(resource_id=resource_id, resource_title=resource_title, change_type="delete")
        return None

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def put(self, id):
        request_data = request.get_json()
        instance = session.query(Resource).filter_by(id=id).first()
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
            elastic_index.add_document(load_result, "Resource")
            self.log_update(resource_id=load_result.id, resource_title=load_result.title, change_type="create")
            return self.resourceSchema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT, details=load_result.errors)

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
