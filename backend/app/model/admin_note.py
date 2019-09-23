from sqlalchemy import func

from app import db
from app.model.resource import Resource
from app.model.user import User


class AdminNote(db.Model):
    __tablename__ = 'admin_note'
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    user = db.relationship(User, backref='admin_notes')
    resource = db.relationship(Resource, backref='admin_notes')
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    note = db.Column(db.String)
