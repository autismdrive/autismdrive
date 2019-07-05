import datetime

from dateutil.tz import tzutc

from app import db
from sqlalchemy.ext.declarative import declarative_base

from app.model.category import Category
from app.model.study import Study
Base = declarative_base()


class StudyCategory(db.Model):
    __tablename__ = 'study_category'
    id = db.Column(db.Integer, primary_key=True)
    study_id = db.Column(db.Integer, db.ForeignKey(Study.id), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)
    study = db.relationship(Study, backref='study_categories')
    category = db.relationship(Category, backref='category_studies')
    last_updated = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=tzutc()))
