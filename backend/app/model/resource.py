import datetime

from dateutil.tz import tzutc
from sqlalchemy.ext.declarative import declarative_base

from app import db
Base = declarative_base()


class Resource(db.Model):
    __tablename__ = 'resource'
    __label__ = "Online Information"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    title = db.Column(db.String)
    last_updated = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=tzutc()))
    description = db.Column(db.String)
    organization_id = db.Column('organization_id', db.Integer,
                               db.ForeignKey('organization.id'))
    phone = db.Column(db.String)
    website = db.Column(db.String)
    categories = db.relationship("ResourceCategory", back_populates="resource")

    __mapper_args__ = {
        'polymorphic_identity': 'resource',
        'polymorphic_on': type
    }

    def indexable_content(self):
        return self.description
