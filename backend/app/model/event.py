import datetime

from app import db


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    last_updated= db.Column(db.DateTime, default=datetime.datetime.now)
    description = db.Column(db.String)
    date = db.Column(db.DateTime)
    time = db.Column(db.String)
    ticket_cost = db.Column(db.String)
    organization_id = db.Column('organization_id', db.Integer,
                               db.ForeignKey('organization.id'))
    primary_contact = db.Column(db.String)
    location_name = db.Column(db.String)
    street_address1 = db.Column(db.String)
    street_address2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    phone = db.Column(db.String)
    website = db.Column(db.String)
    categories = db.relationship("EventCategory", back_populates="event")

    def indexable_content(self):
        return self.description
