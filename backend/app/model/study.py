import datetime
import enum

from dateutil.tz import tzutc

from app import db


class Status(enum.Enum):
    currently_enrolling = 1
    study_in_progress = 2
    results_being_analyzed = 3
    study_results_published = 4

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)

    @classmethod
    def options(cls):
        return [item.name for item in cls]


class Study(db.Model):
    __tablename__ = 'study'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    last_updated = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=tzutc()))
    description = db.Column(db.String)
    participant_description = db.Column(db.String)
    benefit_description = db.Column(db.String)
    investigators = db.relationship("StudyInvestigator", back_populates="study")
    organization_id = db.Column('organization_id', db.Integer,
                                db.ForeignKey('organization.id'))
    location = db.Column(db.String)
    status = db.Column(db.Enum(Status))
    categories = db.relationship("StudyCategory", back_populates="study")

    def indexable_content(self):
        return ' '.join(filter(None, (self.description,
                                      self.participant_description,
                                      self.benefit_description,
                                      self.location)))
