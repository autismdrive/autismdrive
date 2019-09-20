from sqlalchemy import func

from app import db


class AdminNote(db.Model):
    __tablename__ = 'admin_note'
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    note = db.Column(db.String)
