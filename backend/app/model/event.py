from app import db
from app.model.location import Location


class Event(Location):
    __tablename__ = 'event'
    id = db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)
    date = db.Column(db.DateTime)
    time = db.Column(db.String)
    ticket_cost = db.Column(db.String)
    location_name = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'event',
    }
