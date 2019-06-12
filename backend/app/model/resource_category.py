from app import db
from sqlalchemy.ext.declarative import declarative_base

from app.model.category import Category
from app.model.resource import Resource
Base = declarative_base()


class ResourceCategory(db.Model):
    __tablename__ = 'resource_category'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    resource_id = db.Column(db.Integer, db.ForeignKey(Resource.id), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)
    resource = db.relationship(Resource, backref='resource_categories')
    category = db.relationship(Category, backref='category_resources')

