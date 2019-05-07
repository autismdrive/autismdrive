from app import db
from sqlalchemy.ext.declarative import declarative_base

from app.model.category import Category
from app.model.location import Location
Base = declarative_base()


class LocationCategory(db.Model):
    __tablename__ = 'location_category'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)
    location = db.relationship(Location, backref='location_categories')
    category = db.relationship(Category, backref='category_locations')

