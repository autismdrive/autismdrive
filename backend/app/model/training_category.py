from app import db
from sqlalchemy.ext.declarative import declarative_base

from app.model.category import Category
from app.model.training import Training
Base = declarative_base()


class TrainingCategory(db.Model):
    __tablename__ = 'training_category'
    id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, db.ForeignKey(Training.id), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)
    training = db.relationship(Training, backref='training_categories')
    category = db.relationship(Category, backref='category_trainings')
