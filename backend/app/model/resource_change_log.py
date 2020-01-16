from sqlalchemy import func

from app import db


class ResourceChangeLog(db.Model):
    __tablename__ = 'resource_change_log'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    user_id = db.Column(db.Integer)
    resource_id = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
