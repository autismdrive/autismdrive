from sqlalchemy import func

from app import db


class ZipCode(db.Model):
    __tablename__ = 'zip_code'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
