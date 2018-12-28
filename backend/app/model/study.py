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
    outcomes_description = db.Column(db.String)
    organization_id = db.Column('organization_id', db.Integer,
                               db.ForeignKey('organization.id'))
    enrollment_start_date = db.Column(db.DateTime)
    enrollment_end_date = db.Column(db.DateTime)
    current_num_participants = db.Column(db.Integer)
    max_num_participants = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    website = db.Column(db.String)
    categories = db.relationship("StudyCategory", back_populates="study")

    # we'll change current_num_participants to a count of related participants if that's how we connect things.
