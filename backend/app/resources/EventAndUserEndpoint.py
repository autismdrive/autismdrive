import flask_restful
from flask import request
from sqlalchemy import cast, Integer

from app.database import session
from app.models import EventUser
from app.models import Event, EventUser, User
from app.rest_exception import RestException
from app.schemas import EventUserSchema


class EventByUserEndpoint(flask_restful.Resource):

    schema = EventUserSchema()

    def get(self, user_id):
        event_users = (
            session.query(EventUser)
            .join(EventUser.event)
            .filter(EventUser.user_id == cast(user_id, Integer))
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
            .filter(EventUser.event_id == cast(event_id, Integer))
            .order_by(User.name)
            .all()
        )
        return self.schema.dump(event_users, many=True)


class EventUserEndpoint(flask_restful.Resource):
    schema = EventUserSchema()

    def get(self, id):
        model = session.query(EventUser).filter_by(id=cast(id, Integer)).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    def delete(self, id):
        session.query(EventUser).filter_by(id=cast(id, Integer)).delete()
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
