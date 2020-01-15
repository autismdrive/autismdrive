from sqlalchemy import func

from app import db


class ResourceChangeLog(db.Model):
    __tablename__ = 'resource_change_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    resource_id = db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'))
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
