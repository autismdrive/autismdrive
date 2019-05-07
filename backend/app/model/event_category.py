from app import db
from sqlalchemy.ext.declarative import declarative_base

from app.model.category import Category
from app.model.event import Event
Base = declarative_base()


class EventCategory(db.Model):
    __tablename__ = 'event_category'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey(Event.id), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)
    event = db.relationship(Event, backref='event_categories')
    category = db.relationship(Category, backref='category_events')

