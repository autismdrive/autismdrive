import datetime
import enum

from dateutil.tz import tzutc
from sqlalchemy import func

from app import db


class Status(enum.Enum):
    currently_enrolling = "Currently enrolling"
    study_in_progress = "Study in progress"
    results_being_analyzed = "Results being analyzed"
    study_results_published = "Study results published"

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)

    @classmethod
    def options(cls):
        return [item.name for item in cls]


class Study(db.Model):
    __tablename__ = 'study'
    __label__ = "Research Studies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    short_title = db.Column(db.String)
    short_description = db.Column(db.String)
    image_url = db.Column(db.String)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String)
    participant_description = db.Column(db.String)
    benefit_description = db.Column(db.String)
    investigators = db.relationship("StudyInvestigator", back_populates="study")
    coordinator_email = db.Column(db.String)
    eligibility_url = db.Column(db.String)
    results_url = db.Column(db.String)
    organization_name = db.Column(db.String)
    location = db.Column(db.String)
    num_visits = db.Column(db.Integer)
    status = db.Column(db.Enum(Status))
    ages = db.Column(db.ARRAY(db.String), default=[])
    languages = db.Column(db.ARRAY(db.String), default=[])
    categories = db.relationship("StudyCategory", back_populates="study")

    def indexable_content(self):
        return ' '.join(filter(None, (self.category_names(),
                                      self.title,
                                      self.short_title,
                                      self.short_description,
                                      self.description,
                                      self.participant_description,
                                      self.benefit_description,
                                      self.location)))

    def category_names(self):
        cat_text = ''
        for cat in self.categories:
            cat_text = cat_text + ' ' + cat.category.name

        if self.ages is not None and len(self.ages) > 0:
            cat_text = cat_text + ' ' + ' '.join(self.ages)
        if self.languages is not None and len(self.languages) > 0:
            cat_text = cat_text + ' ' + ' '.join(self.languages)

        return cat_text
