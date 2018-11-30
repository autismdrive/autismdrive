import datetime

from app import db


class StarResource(db.model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    last_updated= db.Column(db.DateTime, default=datetime.datetime.now)
    description = db.Column(db.String)
    image = db.Column(db.String) # Should be the url for a feature image
    image_caption = db.Column(db.String)
    organization = db.Column(db.String)
    street_address1 = db.Column(db.String)
    street_address2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    county = db.Column(db.String)
    phone = db.Column(db.String)
    website = db.Column(db.String)
    # need to add in related categories as well (perhaps a related model?)
