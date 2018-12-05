import datetime

from app import db


class Training(db.Model):
    __tablename__ = 'training'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    description = db.Column(db.String)
    outcomes = db.Column(db.String)
    image = db.Column(db.String)  # Should be the url for a feature image
    image_caption = db.Column(db.String)
    # Probably need related categories as well for recommendations, even though that isn't explicitly in the design
