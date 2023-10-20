import flask_restful
from flask import request

from app.database import session
from app.elastic_index import elastic_index
from app.models import Category, ResourceCategory, Event
from app.rest_exception import RestException
from app.schemas import EventCategorySchema, CategoryEventsSchema, EventCategoriesSchema


class EventByCategoryEndpoint(flask_restful.Resource):

    schema = CategoryEventsSchema()

    def get(self, category_id):
        event_categories = (
            session.query(ResourceCategory)
            .join(ResourceCategory.resource)
            .filter(ResourceCategory.category_id == category_id)
            .order_by(Event.title)
            .all()
        )
        return self.schema.dump(event_categories, many=True)


class CategoryByEventEndpoint(flask_restful.Resource):

    schema = EventCategoriesSchema()

    def get(self, event_id):
        event_categories = (
            session.query(ResourceCategory)
            .join(ResourceCategory.category)
            .filter(ResourceCategory.resource_id == event_id)
            .order_by(Category.name)
            .all()
        )
        return self.schema.dump(event_categories, many=True)

    def post(self, event_id):
        request_data = request.get_json()

        for item in request_data:
            item["resource_id"] = event_id

        event_categories = self.schema.load(data=request_data, session=session, many=True)
        session.query(ResourceCategory).filter_by(resource_id=event_id).delete()
        for c in event_categories:
            session.add(ResourceCategory(resource_id=event_id, category_id=c.category_id, type="event"))
        session.commit()
        instance = session.query(Event).filter_by(id=event_id).first()
        elastic_index.update_document(document=instance, latitude=instance.latitude, longitude=instance.longitude)
        return self.get(event_id)


class EventCategoryEndpoint(flask_restful.Resource):
    schema = EventCategorySchema()

    def get(self, id):
        model = session.query(ResourceCategory).filter_by(id=id).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        session.query(ResourceCategory).filter_by(id=id).delete()
        session.commit()
        return None


class EventCategoryListEndpoint(flask_restful.Resource):
    schema = EventCategorySchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data).data
        session.query(ResourceCategory).filter_by(
            resource_id=load_result.event_id, category_id=load_result.category_id
        ).delete()
        session.add(load_result)
        session.commit()
        return self.schema.dump(load_result)
