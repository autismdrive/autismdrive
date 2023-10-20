import flask_restful
from flask import request

from app.database import session
from app.elastic_index import elastic_index
from app.models import Category, Resource, ResourceCategory
from app.models import ResourceCategory
from app.rest_exception import RestException
from app.schemas import ResourceCategorySchema, CategoryResourcesSchema, ResourceCategoriesSchema


class ResourceByCategoryEndpoint(flask_restful.Resource):

    schema = CategoryResourcesSchema()

    def get(self, category_id):
        resource_categories = (
            session.query(ResourceCategory)
            .join(ResourceCategory.resource)
            .filter(ResourceCategory.category_id == category_id)
            .order_by(Resource.title)
            .all()
        )
        return self.schema.dump(resource_categories, many=True)


class CategoryByResourceEndpoint(flask_restful.Resource):

    schema = ResourceCategoriesSchema()

    def get(self, resource_id):
        resource_categories = (
            session.query(ResourceCategory)
            .join(ResourceCategory.category)
            .filter(ResourceCategory.resource_id == resource_id)
            .order_by(Category.name)
            .all()
        )
        return self.schema.dump(resource_categories, many=True)

    def post(self, resource_id):
        request_data = request.get_json()

        for item in request_data:
            item["resource_id"] = resource_id

        resource_categories = self.schema.load(request_data, many=True)
        session.query(ResourceCategory).filter_by(resource_id=resource_id).delete()
        for c in resource_categories:
            session.add(ResourceCategory(resource_id=resource_id, category_id=c.category_id, type="resource"))
        session.commit()
        instance = session.query(Resource).filter_by(id=resource_id).first()
        elastic_index.update_document(document=instance)
        return self.get(resource_id)


class ResourceCategoryEndpoint(flask_restful.Resource):
    schema = ResourceCategorySchema()

    def get(self, id):
        model = session.query(ResourceCategory).filter_by(id=id).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        session.query(ResourceCategory).filter_by(id=id).delete()
        session.commit()
        return None


class ResourceCategoryListEndpoint(flask_restful.Resource):
    schema = ResourceCategorySchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(data=request_data, session=session)
        session.query(ResourceCategory).filter_by(
            resource_id=load_result.resource_id, category_id=load_result.category_id
        ).delete()
        session.add(load_result)
        session.commit()
        return self.schema.dump(load_result)
