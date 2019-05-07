import flask_restful
from flask import request

from app import db, RestException
from app.model.category import Category
from app.model.event import Event
from app.model.event_category import EventCategory
from app.resources.schema import EventCategorySchema, CategoryEventsSchema, EventCategoriesSchema


class EventByCategoryEndpoint(flask_restful.Resource):

    schema = CategoryEventsSchema()

    def get(self, category_id):
        event_categories = db.session.query(EventCategory)\
            .join(EventCategory.event)\
            .filter(EventCategory.category_id == category_id)\
            .order_by(Event.title)\
            .all()
        return self.schema.dump(event_categories, many=True)


class CategoryByEventEndpoint(flask_restful.Resource):

    schema = EventCategoriesSchema()

    def get(self, event_id):
        event_categories = db.session.query(EventCategory).\
            join(EventCategory.category).\
            filter(EventCategory.event_id == event_id).\
            order_by(Category.name).\
            all()
        return self.schema.dump(event_categories,many=True)

    def post(self, event_id):
        request_data = request.get_json()
        event_categories = self.schema.load(request_data, many=True).data
        db.session.query(EventCategory).filter_by(event_id=event_id).delete()
        for c in event_categories:
            db.session.add(EventCategory(event_id=event_id,
                           category_id=c.category_id))
        db.session.commit()
        return self.get(event_id)


class EventCategoryEndpoint(flask_restful.Resource):
    schema = EventCategorySchema()

    def get(self, id):
        model = db.session.query(EventCategory).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        db.session.query(EventCategory).filter_by(id=id).delete()
        db.session.commit()
        return None


class EventCategoryListEndpoint(flask_restful.Resource):
    schema = EventCategorySchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data).data
        db.session.query(EventCategory).filter_by(event_id=load_result.event_id,
                                                     category_id=load_result.category_id).delete()
        db.session.add(load_result)
        db.session.commit()
        return self.schema.dump(load_result)
