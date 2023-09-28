from flask_sqlalchemy.model import Model
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy import func
from sqlalchemy.orm import declarative_base

from app.database import Base
from app.schema.model_schema import ModelSchema


class EmailLog(Base):
    __tablename__ = "email_log"
    id = Column(Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("stardrive_user.id"))
    type = Column(String)
    tracking_code = Column(String)
    viewed = Column(Boolean)
    date_viewed = Column(DateTime)
    last_updated = Column(DateTime(timezone=True), default=func.now())


class EmailLogSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EmailLog
