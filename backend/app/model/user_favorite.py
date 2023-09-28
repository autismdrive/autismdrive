from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base
from app.model.category import Category
from app.model.resource import Resource
from app.model.user import User


class UserFavorite(Base):
    __tablename__ = "user_favorite"
    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    type = Column(String)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    resource_id = Column(Integer, ForeignKey(Resource.id))
    category_id = Column(Integer, ForeignKey(Category.id))
    age_range = Column(String)
    language = Column(String)
    covid19_category = Column(String)
    user = relationship(User, backref="user_favorites")
    resource = relationship(Resource, backref="user_favorites")
    category = relationship(Category, backref="user_favorites")
