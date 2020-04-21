from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
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
    insurance = db.Column(db.String)
    organization_name = db.Column(db.String)
    phone = db.Column(db.String)
    phone_extension = db.Column(db.String)
    website = db.Column(db.String)
    contact_email = db.Column(db.String)
    video_code = db.Column(db.String)
    is_uva_education_content = db.Column(db.Boolean)
    is_draft = db.Column(db.Boolean)
    ages = db.Column(db.ARRAY(db.String), default=[])
    languages = db.Column(db.ARRAY(db.String), default=[])
    covid19_categories = db.Column(ARRAY(db.String), default=[])
    categories = db.relationship("ResourceCategory", back_populates="resource")

    __mapper_args__ = {
        'polymorphic_identity': 'resource',
        'polymorphic_on': type
    }

    def indexable_content(self):
        return ' '.join(filter(None, (self.category_names(),
                                      self.title,
                                      self.description,
                                      self.insurance)))

    def category_names(self):
        cat_text = ''
        for cat in self.categories:
            cat_text = cat_text + ' ' + cat.category.name

        if self.ages is not None and len(self.ages) > 0:
            cat_text = cat_text + ' ' + ' '.join(self.ages)
        if self.languages is not None and len(self.languages) > 0:
            cat_text = cat_text + ' ' + ' '.join(self.languages)
        if self.covid19_categories is not None and len(self.covid19_categories) > 0:
            cat_text = cat_text + ' ' + ' '.join(self.covid19_categories)

        return cat_text
