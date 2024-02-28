import datetime

import flask_restful
from flask import request, g
from marshmallow import ValidationError

from app.auth import auth
from app.database import session
from app.elastic_index import elastic_index
from app.enums import Permission
from app.models import Event, EventUser, Geocode, ResourceChangeLog
from app.rest_exception import RestException
from app.schemas import SchemaRegistry
from app.utils.resource_utils import to_database_object_dict
from app.wrappers import requires_permission


class EventEndpoint(flask_restful.Resource):

    schema = SchemaRegistry.EventSchema()

    def get(self, event_id: int):
        model = session.query(Event).filter_by(id=event_id).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_permission(Permission.delete_resource)
    def delete(self, event_id: int):
        event = session.query(Event).filter_by(id=event_id).first()

        if event is None:
            raise RestException(RestException.NOT_FOUND)

        event_title = event.title
        event_dict = to_database_object_dict(self.schema, event)
        elastic_index.remove_document(event_dict)

        session.query(EventUser).filter_by(event_id=event_id).delete()
        session.query(Event).filter_by(id=event_id).delete()
        session.commit()
        self.log_update(event_id=event_id, event_title=event_title, change_type="delete")
        return None

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def put(self, event_id: int):
        request_data = request.get_json()
        instance = session.query(Event).filter_by(id=event_id).first()
        if (
            instance.zip != request_data["zip"]
            or instance.street_address1 != request_data["street_address1"]
            or instance.latitude is None
        ):
            address_dict = {
                "street": request_data["street_address1"],
                "city": request_data["city"],
                "state": request_data["state"],
                "zip": request_data["zip"],
            }
            geocode = Geocode.get_geocode(address_dict=address_dict)
            request_data["latitude"] = geocode["lat"]
            request_data["longitude"] = geocode["lng"]
        try:
            updated = self.schema.load(data=request_data, instance=instance, session=session)
        except Exception as e:
            raise RestException(RestException.INVALID_OBJECT, details=e.args[0])
        updated.last_updated = datetime.datetime.utcnow()
        session.add(updated)
        session.commit()
        elastic_index.update_document(document=to_database_object_dict(self.schema, updated))
        self.log_update(event_id=updated.id, event_title=updated.title, change_type="edit")
        return self.schema.dump(updated)

    @staticmethod
    def log_update(event_id, event_title, change_type):
        log = ResourceChangeLog(
            resource_id=event_id,
            resource_title=event_title,
            user_id=g.user.id,
            user_email=g.user.email,
            type=change_type,
        )
        session.add(log)
        session.commit()


class EventListEndpoint(flask_restful.Resource):

    events_schema = SchemaRegistry.EventSchema(many=True)
    event_schema = SchemaRegistry.EventSchema()

    def get(self):
        events = session.query(Event).all()
        return self.events_schema.dump(events)

    @auth.login_required
    @requires_permission(Permission.create_resource)
    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.event_schema.load(data=request_data, session=session)
            address_dict = {
                "street": load_result.street_address1,
                "city": load_result.city,
                "state": load_result.state,
                "zip": load_result.zip,
            }
            geocode = Geocode.get_geocode(address_dict=address_dict)
            load_result.latitude = geocode["lat"]
            load_result.longitude = geocode["lng"]
            session.add(load_result)
            session.commit()

            obj_dict = to_database_object_dict(self.event_schema, load_result)
            elastic_index.add_document(document=obj_dict)
            self.log_update(event_id=obj_dict.id, event_title=obj_dict.title, change_type="create")
            return self.event_schema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)

    @staticmethod
    def log_update(event_id, event_title, change_type):
        log = ResourceChangeLog(
            resource_id=event_id,
            resource_title=event_title,
            user_id=g.user.id,
            user_email=g.user.email,
            type=change_type,
        )
        session.add(log)
        session.commit()
