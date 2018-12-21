import flask_restful
from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app import db, RestException
from app.model.category import Category
from app.resources.schema import CategorySchema, ParentCategorySchema
from app.resources.Auth import login_optional


class CategoryEndpoint(flask_restful.Resource):
    schema = CategorySchema()

    def get(self, id):
        category = db.session.query(Category).filter(Category.id == id).first()
        if category is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(category)

    def delete(self, id):
        try:
            db.session.query(Category).filter(Category.id == id).delete()
            db.session.commit()
        except IntegrityError as error:
            raise RestException(RestException.CAN_NOT_DELETE)
        return

    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Category).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)


class CategoryListEndpoint(flask_restful.Resource):
    category_schema = CategorySchema()
    categories_schema = CategorySchema(many=True)

    def get(self):
        categories = db.session.query(Category)\
            .options(joinedload(Category.children))\
            .filter(Category.parent_id == None)\
            .order_by(Category.name)\
            .all()
        return self.categories_schema.dump(categories)

    def post(self):
        request_data = request.get_json()
        new_cat, errors = self.category_schema.load(request_data)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        db.session.add(new_cat)
        db.session.commit()
        return self.category_schema.dump(new_cat)


class RootCategoryListEndpoint(flask_restful.Resource):
    categories_schema = ParentCategorySchema(many=True)

    def get(self):
        categories = db.session.query(Category)\
            .filter(Category.parent_id == None)\
            .order_by(Category.display_order, Category.name)\
            .all()
        return self.categories_schema.dump(categories)
