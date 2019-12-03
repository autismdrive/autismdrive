import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError
from elasticsearch import NotFoundError

from app import RestException, db, elastic_index
from app.model.resource import Resource
from app.model.resource_category import ResourceCategory
from app.model.admin_note import AdminNote
from app.schema.schema import ResourceSchema


class ResourceEndpoint(flask_restful.Resource):

    schema = ResourceSchema()

    def get(self, id):
        model = db.session.query(Resource).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        resource = db.session.query(Resource).filter_by(id=id).first()

        try:
            elastic_index.remove_document(resource, 'Resource')
        except NotFoundError:
            pass

        db.session.query(AdminNote).filter_by(resource_id=id).delete()
        db.session.query(ResourceCategory).filter_by(resource_id=id).delete()
        db.session.query(Resource).filter_by(id=id).delete()
        db.session.commit()
        return None

    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Resource).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        elastic_index.update_document(updated, 'Resource')
        return self.schema.dump(updated)


class ResourceListEndpoint(flask_restful.Resource):

    resourcesSchema = ResourceSchema(many=True)
    resourceSchema = ResourceSchema()

    def get(self):
        resources = db.session.query(Resource).all()
        return self.resourcesSchema.dump(resources)

    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.resourceSchema.load(request_data).data
            db.session.add(load_result)
            db.session.commit()
            elastic_index.add_document(load_result, 'Resource')
            return self.resourceSchema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)
