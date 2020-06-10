from app import db
from app.model.event import Event


class Webinar(Event):
    __tablename__ = 'webinar'
    __label__ = "Webinars"
    id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    webinar_link = db.Column(db.String)
    survey_link = db.Column(db.String)
    max_users = db.Column(db.Integer)
    registered_users = db.relationship("WebinarUser", back_populates='webinar')

    __mapper_args__ = {
        'polymorphic_identity': 'webinar',
    }
