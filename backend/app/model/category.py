from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from app.database import Base


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    display_order = Column(Integer, nullable=True)
    children = relationship(
        "Category",
        backref=backref("parent", remote_side=[id]),
        lazy="joined",
        join_depth=2,
        order_by="Category.display_order,Category.name",
    )
    hit_count = 0  # when returning categories in the context of a search.

    def calculate_level(self):
        """Provide the depth of the category"""
        level = 0
        cat = self
        while cat.parent and isinstance(cat, Category):
            level = level + 1
            cat = cat.parent
        return level

    # Returns an array of paths that should be used to search for
    # this category. , for instance "animals,cats,smelly-cats" would return
    # an array of three paths: ["animal", "animal,cats" and "animal,cats,smelly-cats"
    # but using the id of the category, not the name.
    def all_search_paths(self):
        cat = self
        paths = [cat.search_path()]
        while cat.parent:
            cat = cat.parent
            paths.append(cat.search_path())
        return paths

    def search_path(self):
        cat = self
        path = str(cat.id)
        while cat.parent and cat.parent.id:
            cat = cat.parent
            path = str(cat.id) + "," + path
        return path
