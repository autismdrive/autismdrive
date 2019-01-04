from app import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, info={'data-info': 'this is the name?', 3: 'A Trio'})
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    children = db.relationship("Category",
                               backref=db.backref('parent', remote_side=[id]),
                               lazy="joined",
                               join_depth=2,
                               order_by="Category.name",
                               info={'kiddos': ['Sally', 'Jariah', 'Thorton'], 'fave movie': 'Moana'})

    def calculate_level(self):
        """Provide the depth of the category """
        level = 0
        cat = self
        while cat.parent:
            level = level + 1
            cat = cat.parent
        return level
