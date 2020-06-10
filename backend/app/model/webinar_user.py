from sqlalchemy import func

from app import db

from app.model.user import User
from app.model.webinar import Webinar


class WebinarUser(db.Model):
    __tablename__ = 'webinar_user'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    webinar_id = db.Column(db.Integer, db.ForeignKey(Webinar.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    webinar = db.relationship(Webinar, backref='webinar_users')
    user = db.relationship(User, backref='user_webinars')
