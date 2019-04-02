import datetime

from app import db


class StarResource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    last_updated= db.Column(db.DateTime, default=datetime.datetime.now)
    description = db.Column(db.String)
    image_url = db.Column(db.String) # Should be the url for a feature image
    image_caption = db.Column(db.String)
    organization_id = db.Column('organization_id', db.Integer,
                               db.ForeignKey('organization.id'))
    street_address1 = db.Column(db.String)
    street_address2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    county = db.Column(db.String)
    phone = db.Column(db.String)
    website = db.Column(db.String)
    categories = db.relationship("ResourceCategory", back_populates="resource")

    def indexable_content(self):
        return self.description
