from sqlalchemy import func

from app import db
from sqlalchemy.ext.declarative import declarative_base

from app.model.user import User
from app.model.resource import Resource
from app.model.category import Category
Base = declarative_base()


class UserFavorite(db.Model):
    __tablename__ = 'user_favorite'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    type = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey(Resource.id))
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    age_range = db.Column(db.String)
    language = db.Column(db.String)
    covid19_category = db.Column(db.String)
    user = db.relationship(User, backref='user_favorites')
    resource = db.relationship(Resource, backref='user_favorites')
    category = db.relationship(Category, backref='user_favorites')
