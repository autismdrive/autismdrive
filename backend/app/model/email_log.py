from marshmallow import EXCLUDE
from sqlalchemy import func

from app import db
from app.schema.model_schema import ModelSchema


class EmailLog(db.Model):
    __tablename__ = 'email_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    type = db.Column(db.String)
    tracking_code = db.Column(db.String)
    viewed = db.Column(db.Boolean)
    date_viewed = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())


class EmailLogSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EmailLog
