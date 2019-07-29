import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError

from app import RestException, db, elastic_index
from app.model.event import Event
from app.schema.schema import EventSchema


class EventEndpoint(flask_restful.Resource):

    schema = EventSchema()

    def get(self, id):
        model = db.session.query(Event).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        event = db.session.query(Event).filter_by(id=id).first()

        if event is not None:
            elastic_index.remove_document(event, 'Event')

        db.session.query(Event).filter_by(id=id).delete()
        db.session.commit()
        return None

    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Event).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        elastic_index.update_document(updated, 'Event')
        return self.schema.dump(updated)


class EventListEndpoint(flask_restful.Resource):

    eventsSchema = EventSchema(many=True)
    eventSchema = EventSchema()

    def get(self):
        events = db.session.query(Event).all()
        return self.eventsSchema.dump(events)

    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.eventSchema.load(request_data).data
            db.session.add(load_result)
            db.session.commit()
            elastic_index.add_document(load_result, 'Event')
            return self.eventSchema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)
