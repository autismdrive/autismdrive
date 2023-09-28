from sqlalchemy import func, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.database import Base
from app.model.category import Category


class Resource(Base):
    __tablename__ = "resource"
    __label__ = "Online Information"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    title = Column(String)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    description = Column(String)
    insurance = Column(String)
    organization_name = Column(String)
    phone = Column(String)
    phone_extension = Column(String)
    website = Column(String)
    contact_email = Column(String)
    video_code = Column(String)
    is_uva_education_content = Column(Boolean)
    is_draft = Column(Boolean)
    ages = Column(ARRAY(String), default=[])
    languages = Column(ARRAY(String), default=[])
    covid19_categories = Column(ARRAY(String), default=[])
    should_hide_related_resources = Column(Boolean, default=False)

    __mapper_args__ = {"polymorphic_identity": "resource", "polymorphic_on": type}

    def indexable_content(self):
        return " ".join(
            filter(
                None,
                (
                    self.title,
                    self.description,
                    self.insurance,
                    self.category_names(),
                ),
            )
        )

    def category_names(self):
        cat_text = ""
        for cat in self.categories:
            cat_text = cat_text + " " + cat.category.name

        if self.ages is not None and len(self.ages) > 0:
            cat_text = cat_text + " " + " ".join(self.ages)
        if self.languages is not None and len(self.languages) > 0:
            cat_text = cat_text + " " + " ".join(self.languages)
        if self.covid19_categories is not None and len(self.covid19_categories) > 0:
            cat_text = cat_text + " " + " ".join(self.covid19_categories)

        return cat_text


class ResourceCategory(Base):
    __tablename__ = "resource_category"
    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    type = Column(String)
    resource_id = Column(Integer, ForeignKey(Resource.id), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    resource = relationship(Resource, backref="resource_categories")
    category = relationship(Category, backref="category_resources")


Resource.categories = relationship("ResourceCategory", back_populates="resource")
