import datetime

import flask_restful
from flask import request, g
from marshmallow import ValidationError
from elasticsearch import NotFoundError

from app import RestException, db, elastic_index, auth
from app.model.resource import Resource
from app.model.resource_category import ResourceCategory
from app.model.admin_note import AdminNote
from app.model.resource_change_log import ResourceChangeLog
from app.schema.schema import ResourceSchema
from app.model.event import Event
from app.model.location import Location
from app.model.user import Role
from app.wrappers import requires_roles


class ResourceEndpoint(flask_restful.Resource):

    schema = ResourceSchema()

    def get(self, id):
        model = db.session.query(Resource).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_roles(Role.admin)
    def delete(self, id):
        resource = db.session.query(Resource).filter_by(id=id).first()
        resource_id = resource.id

        try:
            elastic_index.remove_document(resource, 'Resource')
        except NotFoundError:
            pass

        db.session.query(AdminNote).filter_by(resource_id=id).delete()
        db.session.query(Event).filter_by(id=id).delete()
        db.session.query(Location).filter_by(id=id).delete()
        db.session.query(ResourceCategory).filter_by(resource_id=id).delete()
        db.session.query(Resource).filter_by(id=id).delete()
        db.session.commit()
        self.log_update(resource_id=resource_id, change_type='delete')
        return None

    @auth.login_required
    @requires_roles(Role.admin)
    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Resource).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        elastic_index.update_document(updated, 'Resource')
        self.log_update(resource_id=updated.id, change_type='edit')
        return self.schema.dump(updated)

    def log_update(self, resource_id, change_type):
        log = ResourceChangeLog(resource_id=resource_id, user_id=g.user.id, type=change_type)
        db.session.add(log)
        db.session.commit()


class ResourceListEndpoint(flask_restful.Resource):

    resourcesSchema = ResourceSchema(many=True)
    resourceSchema = ResourceSchema()

    def get(self):
        resources = db.session.query(Resource).all()
        return self.resourcesSchema.dump(resources)

    @auth.login_required
    @requires_roles(Role.admin)
    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.resourceSchema.load(request_data).data
            db.session.add(load_result)
            db.session.commit()
            elastic_index.add_document(load_result, 'Resource')
            self.log_update(resource_id=load_result.id, change_type='create')
            return self.resourceSchema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)

    def log_update(self, resource_id, change_type):
        log = ResourceChangeLog(resource_id=resource_id, user_id=g.user.id, type=change_type)
        db.session.add(log)
        db.session.commit()
