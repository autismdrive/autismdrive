from sqlalchemy import func

from app import db
from sqlalchemy.ext.declarative import declarative_base

from app.model.user import User
from app.model.study import Study
Base = declarative_base()


class StudyUser(db.Model):
    __tablename__ = 'study_user'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.String)
    study_id = db.Column(db.Integer, db.ForeignKey(Study.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    study = db.relationship(Study, backref='study_users')
    user = db.relationship(User, backref='user_studies')
