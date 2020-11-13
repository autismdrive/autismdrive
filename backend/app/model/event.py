import datetime

from app import db
from app.model.location import Location


class Event(Location):
    __tablename__ = 'event'
    __label__ = "Events and Training"
    id = db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)
    date = db.Column(db.DateTime)
    time = db.Column(db.String)
    ticket_cost = db.Column(db.String)
    location_name = db.Column(db.String)
    includes_registration = db.Column(db.Boolean)
    webinar_link = db.Column(db.String)
    post_survey_link = db.Column(db.String)
    max_users = db.Column(db.Integer)
    registered_users = db.relationship("EventUser", back_populates='event')
    registration_url = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    post_event_description = db.Column(db.String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'event',
    }

    def indexable_content(self):
        return ' '.join(filter(None, (self.title,
                                      self.description,
                                      self.post_event_description,
                                      self.insurance,
                                      self.category_names(),)))
