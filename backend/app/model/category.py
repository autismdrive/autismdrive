import datetime

from dateutil.tz import tzutc

from app import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(tz=tzutc()))
    children = db.relationship("Category",
                               backref=db.backref('parent', remote_side=[id]),
                               lazy="joined",
                               join_depth=2,
                               order_by="Category.name")

    def calculate_level(self):
        """Provide the depth of the category """
        level = 0
        cat = self
        while cat.parent:
            level = level + 1
            cat = cat.parent
        return level
