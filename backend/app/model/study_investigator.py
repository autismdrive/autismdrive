from app import db

from app.model.investigator import Investigator
from app.model.study import Study


class StudyInvestigator(db.Model):
    __tablename__ = 'study_investigator'
    id = db.Column(db.Integer, primary_key=True)
    study_id = db.Column(db.Integer, db.ForeignKey(Study.id), nullable=False)
    investigator_id = db.Column(db.Integer, db.ForeignKey(Investigator.id), nullable=False)
    study = db.relationship(Study, backref='study_investigators')
    investigator = db.relationship(Investigator, backref='investigator_studiess')
