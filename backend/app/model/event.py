import datetime

from dateutil.tz import tzutc

from app import db
from app.model.location import Location


class Event(Location):
    __tablename__ = 'event'
    __label__ = "Events and Training"
    id = db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=tzutc()))
    date = db.Column(db.DateTime)
    time = db.Column(db.String)
    ticket_cost = db.Column(db.String)
    location_name = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'event',
    }
