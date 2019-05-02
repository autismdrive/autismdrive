import flask_restful
from flask import request

from app import db, RestException
from app.model.category import Category
from app.model.location import Location
from app.model.location_category import LocationCategory
from app.resources.schema import LocationCategorySchema, CategoryLocationsSchema, LocationCategoriesSchema


class LocationByCategoryEndpoint(flask_restful.Resource):

    schema = CategoryLocationsSchema()

    def get(self, category_id):
        location_categories = db.session.query(LocationCategory)\
            .join(LocationCategory.location)\
            .filter(LocationCategory.category_id == category_id)\
            .order_by(Location.title)\
            .all()
        return self.schema.dump(location_categories, many=True)


class CategoryByLocationEndpoint(flask_restful.Resource):

    schema = LocationCategoriesSchema()

    def get(self, location_id):
        location_categories = db.session.query(LocationCategory).\
            join(LocationCategory.category).\
            filter(LocationCategory.location_id == location_id).\
            order_by(Category.name).\
            all()
        return self.schema.dump(location_categories,many=True)

    def post(self, location_id):
        request_data = request.get_json()
        location_categories = self.schema.load(request_data, many=True).data
        db.session.query(LocationCategory).filter_by(location_id=location_id).delete()
        for c in location_categories:
            db.session.add(LocationCategory(location_id=location_id,
                           category_id=c.category_id))
        db.session.commit()
        return self.get(location_id)


class LocationCategoryEndpoint(flask_restful.Resource):
    schema = LocationCategorySchema()

    def get(self, id):
        model = db.session.query(LocationCategory).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        db.session.query(LocationCategory).filter_by(id=id).delete()
        db.session.commit()
        return None


class LocationCategoryListEndpoint(flask_restful.Resource):
    schema = LocationCategorySchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data).data
        db.session.query(LocationCategory).filter_by(location_id=load_result.location_id,
                                                     category_id=load_result.category_id).delete()
        db.session.add(load_result)
        db.session.commit()
        return self.schema.dump(load_result)