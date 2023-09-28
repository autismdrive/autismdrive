import flask_restful
from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.auth import auth
from app.database import session
from app.model.category import Category
from app.model.resource import ResourceCategory
from app.model.role import Permission
from app.model.study import StudyCategory
from app.model.user_favorite import UserFavorite
from app.rest_exception import RestException
from app.schema.schema import CategorySchema, ParentCategorySchema
from app.wrappers import requires_permission


class CategoryEndpoint(flask_restful.Resource):
    schema = CategorySchema()

    def get(self, id):
        category = session.query(Category).filter(Category.id == id).first()
        if category is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(category)

    @auth.login_required
    @requires_permission(Permission.taxonomy_admin)
    def delete(self, id):
        try:
            session.query(StudyCategory).filter_by(category_id=id).delete()
            session.query(ResourceCategory).filter_by(category_id=id).delete()
            session.query(UserFavorite).filter_by(category_id=id).delete()
            session.query(Category).filter_by(id=id).delete()
            session.commit()
        except IntegrityError as error:
            raise RestException(RestException.CAN_NOT_DELETE)
        return

    @auth.login_required
    @requires_permission(Permission.taxonomy_admin)
    def put(self, id):
        request_data = request.get_json()
        instance = session.query(Category).filter_by(id=id).first()
        try:
            updated = self.schema.load(data=request_data, session=session, instance=instance)
        except Exception as e:
            raise RestException(RestException.INVALID_OBJECT, details=e)
        session.add(updated)
        session.commit()
        return self.schema.dump(updated)


class CategoryListEndpoint(flask_restful.Resource):
    category_schema = CategorySchema()
    categories_schema = ParentCategorySchema(many=True)

    def get(self):
        categories = (
            session.query(Category)
            .options(joinedload(Category.children))
            .order_by(Category.display_order)
            .order_by(Category.name)
            .all()
        )
        return self.categories_schema.dump(categories)

    @auth.login_required
    @requires_permission(Permission.taxonomy_admin)
    def post(self):
        request_data = request.get_json()
        try:
            new_cat = self.category_schema.load(data=request_data, session=session)
        except Exception as e:
            raise RestException(RestException.INVALID_OBJECT, details=e)
        session.add(new_cat)
        session.commit()
        return self.category_schema.dump(new_cat)


class RootCategoryListEndpoint(flask_restful.Resource):
    categories_schema = CategorySchema(many=True)

    def get(self):
        categories = (
            session.query(Category)
            .filter(Category.parent_id == None)
            .order_by(Category.display_order)
            .order_by(Category.name)
            .all()
        )
        return self.categories_schema.dump(categories)


class CategoryNamesListEndpoint(flask_restful.Resource):
    def get(self):
        categories = (
            session.query(Category)
            .options(joinedload(Category.children))
            .order_by(Category.display_order)
            .order_by(Category.name)
            .all()
        )
        cat_names_list = []
        for cat in categories:
            cat_names_list.append(cat.name)
        return cat_names_list
