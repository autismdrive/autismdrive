from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

from app import db
Base = declarative_base()


class Resource(db.Model):
    __tablename__ = 'resource'
    __label__ = "Online Information"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    title = db.Column(db.String)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String)
    organization_id = db.Column('organization_id', db.Integer,
                               db.ForeignKey('organization.id'))
    phone = db.Column(db.String)
    website = db.Column(db.String)
    video_code = db.Column(db.String)
    is_uva_education_content = db.Column(db.Boolean)
    ages = db.Column(db.ARRAY(db.String), default=[])
    categories = db.relationship("ResourceCategory", back_populates="resource")

    __mapper_args__ = {
        'polymorphic_identity': 'resource',
        'polymorphic_on': type
    }

    def indexable_content(self):
        return ' '.join(filter(None, (self.category_names(),
                                      self.title,
                                      self.description)))

    def category_names(self):
        cat_text = ''
        for cat in self.categories:
            cat_text = cat_text + ' ' + cat.category.indexable_content()

        return cat_text + ' ' + ' '.join(self.ages)
