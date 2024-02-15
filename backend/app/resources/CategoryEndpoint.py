import flask_restful
from flask import request
from sqlalchemy import update, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.auth import auth
from app.database import session
from app.enums import Permission
from app.models import Category, ResourceCategory, StudyCategory, UserFavorite
from app.rest_exception import RestException
from app.schemas import CategorySchema, ParentCategorySchema, CategoryUpdateSchema
from app.wrappers import requires_permission


class CategoryEndpoint(flask_restful.Resource):
    schema = CategorySchema()

    def get(self, category_id: int):
        category = session.query(Category).filter(Category.id == category_id).first()
        if category is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(category)

    @auth.login_required
    @requires_permission(Permission.taxonomy_admin)
    def delete(self, category_id: int):
        try:
            session.query(StudyCategory).filter_by(category_id=category_id).delete()
            session.query(ResourceCategory).filter_by(category_id=category_id).delete()
            session.query(UserFavorite).filter_by(category_id=category_id).delete()
            session.query(Category).filter_by(id=category_id).delete()
            session.commit()
        except IntegrityError as error:
            raise RestException(RestException.CAN_NOT_DELETE, details=error)
        return

    @auth.login_required
    @requires_permission(Permission.taxonomy_admin)
    def put(self, category_id: int):
        request_data = request.get_json()
        get_statement = select(Category).where(Category.id == category_id)
        old_cat = session.execute(get_statement).unique().scalar_one_or_none()

        if old_cat is None:
            raise RestException(RestException.NOT_FOUND)

        try:
            schema = CategoryUpdateSchema()
            updated_cat = schema.load(data=request_data, session=session, instance=old_cat)
            updated_dict = schema.dump(updated_cat)
        except Exception as e:
            raise RestException(RestException.INVALID_OBJECT, details=e)

        update_statement = update(Category).where(Category.id == category_id).values(updated_dict)
        session.execute(update_statement)
        session.commit()
        session.close()

        db_updated = session.execute(get_statement).unique().scalar_one()
        return self.schema.dump(db_updated)


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
