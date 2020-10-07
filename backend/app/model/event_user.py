from sqlalchemy import func

from app import db

from app.model.user import User
from app.model.event import Event


class EventUser(db.Model):
    __tablename__ = 'event_user'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    event_id = db.Column(db.Integer, db.ForeignKey(Event.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    event = db.relationship(Event, backref='event_users')
    user = db.relationship(User, backref='user_events')
