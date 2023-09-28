from flask_marshmallow import fields
from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, Boolean, BigInteger, ARRAY

from app.database import Base
from app.export_service import ExportService
from app.model.event import Event
from app.schema.model_schema import ModelSchema


class RegistrationQuestionnaire(Base):
    __tablename__ = "registration_questionnaire"
    __label__ = "Registration"
    __question_type__ = ExportService.TYPE_IDENTIFYING
    __estimated_duration_minutes__ = 5

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    time_on_task_ms = Column(BigInteger, default=0)

    participant_id = Column("participant_id", Integer, ForeignKey("stardrive_participant.id"))
    user_id = Column("user_id", Integer, ForeignKey("stardrive_user.id"))
    event_id = Column(Integer, ForeignKey(Event.id), nullable=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    zip_code = Column(Integer)
    relationship_to_autism = Column(ARRAY(String), default=[])
    relationship_other = Column(String)
    marketing_channel = Column(ARRAY(String), default=[])
    marketing_other = Column(String)
    newsletter_consent = Column(Boolean)

    def get_field_groups(self):
        return {}


class RegistrationQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = RegistrationQuestionnaire
        ordered = True
        include_fk = True

    _links = fields.Hyperlinks(
        {
            "self": fields.URLFor("api.questionnaireendpoint", name="registration_questionnaire", id="<id>"),
        }
    )
