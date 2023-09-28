import enum

from sqlalchemy import func, Column, Integer, String, DateTime, Enum, ARRAY, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.model.category import Category
from app.model.investigator import Investigator
from app.model.user import User


class Status(enum.Enum):
    currently_enrolling = "Currently enrolling"
    study_in_progress = "Study in progress"
    results_being_analyzed = "Results being analyzed"
    study_results_published = "Study results published"

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)

    @classmethod
    def options(cls):
        return [item.name for item in cls]


class Study(Base):
    __tablename__ = "study"
    __label__ = "Research Studies"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    short_title = Column(String)
    short_description = Column(String)
    image_url = Column(String)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    description = Column(String)
    participant_description = Column(String)
    benefit_description = Column(String)
    coordinator_email = Column(String)
    eligibility_url = Column(String)
    survey_url = Column(String)
    results_url = Column(String)
    organization_name = Column(String)
    location = Column(String)
    num_visits = Column(Integer)
    status = Column(Enum(Status))
    ages = Column(ARRAY(String), default=[])
    languages = Column(ARRAY(String), default=[])
    categories = relationship("StudyCategory", back_populates="study")

    def indexable_content(self):
        return " ".join(
            filter(
                None,
                (
                    self.category_names(),
                    self.title,
                    self.short_title,
                    self.short_description,
                    self.description,
                    self.participant_description,
                    self.benefit_description,
                    self.location,
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

        return cat_text


class StudyInvestigator(Base):
    __tablename__ = "study_investigator"
    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey(Study.id), nullable=False)
    investigator_id = Column(Integer, ForeignKey(Investigator.id), nullable=False)
    study = relationship(Study, backref="study_investigators")
    investigator = relationship(Investigator, backref="investigator_studies")
    last_updated = Column(DateTime(timezone=True), default=func.now())


Study.investigators = relationship(StudyInvestigator, back_populates="study")


class StudyCategory(Base):
    __tablename__ = "study_category"
    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey(Study.id), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    study = relationship(Study, backref="study_categories")
    category = relationship(Category, backref="category_studies")
    last_updated = Column(DateTime(timezone=True), default=func.now())


class StudyUserStatus(enum.Enum):
    inquiry_sent = 1
    enrolled = 2


class StudyUser(Base):
    __tablename__ = "study_user"
    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    status = Column(Enum(StudyUserStatus))
    study_id = Column(Integer, ForeignKey(Study.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    study = relationship(Study, backref="study_users")
    user = relationship(User, backref="user_studies")
