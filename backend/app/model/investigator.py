import datetime
from app import db


class Investigator(db.Model):
    __tablename__ = 'investigator'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    name = db.Column(db.String)
    title = db.Column(db.String)
    organization_id = db.Column('organization_id', db.Integer, db.ForeignKey('organization.id'))
    bio_link = db.Column(db.String)
