import flask_restful
from flask import request
from sqlalchemy import update, select, Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.interfaces import LoaderOption
from sqlalchemy.sql.base import ExecutableOption

from app.auth import auth
from app.database import session
from app.enums import Permission
from app.models import Category, ResourceCategory, StudyCategory, UserFavorite, Resource, Study
from app.rest_exception import RestException
from app.schemas import SchemaRegistry
from app.wrappers import requires_permission


def add_joins_to_statement(statement: Select | ExecutableOption) -> Select | LoaderOption:
    return statement.options(
        joinedload(Category.parent),
        joinedload(Category.children),
        joinedload(Category.resources),
        joinedload(Category.studies),
    )


def get_category_by_id(category_id: int, with_joins=False) -> Category | None:
    """
    Returns a Category matching the given ID from the database. Optionally include joins to parent and child Categories.

    CAUTION: Make sure to close the session after calling this function!
    """
    statement = select(Category)

    if with_joins:
        statement = add_joins_to_statement(statement)

    statement = statement.filter_by(id=category_id)
    return session.execute(statement).unique().scalar_one_or_none()


class CategoryEndpoint(flask_restful.Resource):
    schema = SchemaRegistry.CategorySchema()

    def get(self, category_id: int):
        category = get_category_by_id(category_id, with_joins=True)
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
        old_cat = get_category_by_id(category_id, with_joins=False)

        if old_cat is None:
            raise RestException(RestException.NOT_FOUND)

        try:
            schema = SchemaRegistry.CategoryUpdateSchema()
            updated_cat = schema.load(data=request_data, session=session, instance=old_cat)
            updated_dict = schema.dump(updated_cat)
        except Exception as e:
            raise RestException(RestException.INVALID_OBJECT, details=e)

        update_statement = update(Category).where(Category.id == category_id).values(updated_dict)
        session.execute(update_statement)
        session.commit()
        session.close()

        db_updated = get_category_by_id(category_id, with_joins=True)
        return self.schema.dump(db_updated)


class CategoryListEndpoint(flask_restful.Resource):
    category_schema = SchemaRegistry.CategorySchema()
    categories_schema = SchemaRegistry.ParentCategorySchema(many=True)

    def get(self):
        statement = add_joins_to_statement(select(Category))
        categories = session.execute(statement.order_by(Category.display_order, Category.name)).unique().scalars().all()
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
        db_cat = get_category_by_id(new_cat.id, with_joins=True)
        return self.category_schema.dump(db_cat)


class RootCategoryListEndpoint(flask_restful.Resource):
    categories_schema = SchemaRegistry.CategorySchema(many=True)

    def get(self):
        statement = add_joins_to_statement(select(Category))
        categories = (
            session.execute(
                statement.filter(Category.parent_id.is_(None)).order_by(Category.display_order).order_by(Category.name)
            )
            .unique()
            .scalars()
            .all()
        )
        return self.categories_schema.dump(categories)


class CategoryNamesListEndpoint(flask_restful.Resource):
    def get(self):
        statement = add_joins_to_statement(select(Category))
        categories = (
            session.execute(statement.order_by(Category.display_order).order_by(Category.name)).unique().scalars().all()
        )
        cat_names_list = []
        for cat in categories:
            cat_names_list.append(cat.name)
        return cat_names_list
