import datetime

from app import db


class Study(db.Model):
    __tablename__ = 'study'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    last_updated= db.Column(db.DateTime, default=datetime.datetime.now)
    description = db.Column(db.String)
    researcher_description = db.Column(db.String)
    participant_description = db.Column(db.String)
    outcomes = db.Column(db.String)
    enrollment_date = db.Column(db.DateTime)
    current_enrolled = db.Column(db.Integer)
    total_participants = db.Column(db.Integer)
    study_start = db.Column(db.DateTime)
    study_end = db.Column(db.DateTime)

    # need to add in related categories as well (perhaps a related model?)
    # we'll change current_enrolled to a count of related participants if that's how we connect things.
