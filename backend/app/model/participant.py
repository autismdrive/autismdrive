import datetime

from app import db


class Participant(db.Model):
    # The participant model is used to track enrollment and participation in studies. Participants are associated
    # with a user account; sometimes that of themselves and sometimes that of their guardian.
    __tablename__ = 'stardrive_participant'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    users = db.relationship("UserParticipant", back_populates="participant")
