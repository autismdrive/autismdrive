import datetime

from app import db


class Training(db.Model):
    __tablename__ = 'training'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    description = db.Column(db.String)
    outcomes_description = db.Column(db.String)
    organization_id = db.Column('organization_id', db.Integer,
                               db.ForeignKey('organization.id'))
    image_url = db.Column(db.String)  # Should be the url for a feature image
    image_caption = db.Column(db.String)
    website = db.Column(db.String)
    categories = db.relationship("TrainingCategory", back_populates="training")

    def indexable_content(self):
        return ' '.join(filter(None, (self.description, self.outcomes_description)))
