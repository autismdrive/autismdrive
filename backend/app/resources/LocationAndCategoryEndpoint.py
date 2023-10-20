import flask_restful
from flask import request

from app.database import session
from app.elastic_index import elastic_index
from app.models import Category, ResourceCategory, Location
from app.rest_exception import RestException
from app.schemas import LocationCategorySchema, CategoryLocationsSchema, LocationCategoriesSchema


class LocationByCategoryEndpoint(flask_restful.Resource):

    schema = CategoryLocationsSchema()

    def get(self, category_id):
        location_categories = (
            session.query(ResourceCategory)
            .join(ResourceCategory.resource)
            .filter(ResourceCategory.category_id == category_id, ResourceCategory.type == "location")
            .order_by(Location.title)
            .all()
        )
        return self.schema.dump(location_categories, many=True)


class CategoryByLocationEndpoint(flask_restful.Resource):

    schema = LocationCategoriesSchema()

    def get(self, location_id):
        location_categories = (
            session.query(ResourceCategory)
            .join(ResourceCategory.category)
            .filter(ResourceCategory.resource_id == location_id)
            .order_by(Category.name)
            .all()
        )
        return self.schema.dump(location_categories, many=True)

    def post(self, location_id):
        request_data = request.get_json()

        for item in request_data:
            item["resource_id"] = location_id

        location_categories = self.schema.load(request_data, many=True)
        session.query(ResourceCategory).filter_by(resource_id=location_id).delete()
        for c in location_categories:
            session.add(ResourceCategory(resource_id=location_id, category_id=c.category_id, type="location"))
        session.commit()
        instance = session.query(Location).filter_by(id=location_id).first()
        elastic_index.update_document(document=instance, latitude=instance.latitude, longitude=instance.longitude)
        return self.get(location_id)


class LocationCategoryEndpoint(flask_restful.Resource):
    schema = LocationCategorySchema()

    def get(self, id):
        model = session.query(ResourceCategory).filter_by(id=id).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        session.query(ResourceCategory).filter_by(id=id).delete()
        session.commit()
        return None


class LocationCategoryListEndpoint(flask_restful.Resource):
    schema = LocationCategorySchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data).data
        session.query(ResourceCategory).filter_by(
            resource_id=load_result.resource_id, category_id=load_result.category_id
        ).delete()
        session.add(load_result)
        session.commit()
        return self.schema.dump(load_result)
