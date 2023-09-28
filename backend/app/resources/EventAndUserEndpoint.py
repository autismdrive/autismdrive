import flask_restful
from flask import request

from app.database import session
from app.model.event import Event, EventUser
from app.model.user import User
from app.rest_exception import RestException
from app.schema.schema import EventUserSchema


class EventByUserEndpoint(flask_restful.Resource):

    schema = EventUserSchema()

    def get(self, user_id):
        event_users = (
            session.query(EventUser)
            .join(EventUser.event)
            .filter(EventUser.user_id == user_id)
            .order_by(Event.title)
            .all()
        )
        return self.schema.dump(event_users, many=True)


class UserByEventEndpoint(flask_restful.Resource):

    schema = EventUserSchema()

    def get(self, event_id):
        event_users = (
            session.query(EventUser)
            .join(EventUser.user)
            .filter(EventUser.event_id == event_id)
            .order_by(User.name)
            .all()
        )
        return self.schema.dump(event_users, many=True)


class EventUserEndpoint(flask_restful.Resource):
    schema = EventUserSchema()

    def get(self, id):
        model = session.query(EventUser).filter_by(id=id).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        session.query(EventUser).filter_by(id=id).delete()
        session.commit()
        return None


class EventUserListEndpoint(flask_restful.Resource):
    schema = EventUserSchema()

    def post(self):
        request_data = request.get_json()
        load_result = self.schema.load(request_data).data
        session.query(EventUser).filter_by(event_id=load_result.event_id, user_id=load_result.user_id).delete()
        session.add(load_result)
        session.commit()
        return self.schema.dump(load_result)
