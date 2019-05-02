import datetime

from app import db


class StarResource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    last_updated= db.Column(db.DateTime, default=datetime.datetime.now)
    description = db.Column(db.String)
    organization_id = db.Column('organization_id', db.Integer,
                               db.ForeignKey('organization.id'))
    phone = db.Column(db.String)
    website = db.Column(db.String)
    categories = db.relationship("ResourceCategory", back_populates="resource")

    def indexable_content(self):
        return self.description
