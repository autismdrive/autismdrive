from flask_marshmallow.fields import Hyperlinks, URLFor
from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, Boolean, BigInteger

from app.database import Base
from app.export_service import ExportService
from app.schema.model_schema import ModelSchema


class DevelopmentalQuestionnaire(Base):
    __tablename__ = "developmental_questionnaire"
    __label__ = "Birth and Developmental History"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    time_on_task_ms = Column(BigInteger, default=0)

    participant_id = Column("participant_id", Integer, ForeignKey("stardrive_participant.id"))
    user_id = Column("user_id", Integer, ForeignKey("stardrive_user.id"))
    had_birth_complications = Column(
        Boolean,
        info={
            "display_order": 1,
            "type": "radio",
            "template_options": {
                "label": "Were there any complications during the pregnancy or delivery?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    birth_complications_description = Column(
        String,
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Please describe:",
                "required": False,
            },
            "hide_expression": "!model.had_birth_complications",
        },
    )
    when_motor_milestones = Column(
        String,
        info={
            "display_order": 2,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "early", "label": "Early"},
                    {"value": "onTime", "label": "On-time"},
                    {"value": "delayed", "label": "Delayed"},
                    {"value": "notYet", "label": "Not yet acquired"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"When did " + '
                '(formState.preferredName || "Your child") + '
                '" reach their motor developmental milestones '
                '(e.g., walking, crawling, etc.)?"'
            },
        },
    )
    when_language_milestones = Column(
        String,
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "early", "label": "Early"},
                    {"value": "onTime", "label": "On-time"},
                    {"value": "delayed", "label": "Delayed"},
                    {"value": "notYet", "label": "Not yet acquired"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"When did " + '
                '(formState.preferredName || "Your child") + '
                '" reach their speech/language developmental milestones '
                '(e.g., babbling, using first words and phrases)?"'
            },
        },
    )
    when_toileting_milestones = Column(
        String,
        info={
            "display_order": 4,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "early", "label": "Early"},
                    {"value": "onTime", "label": "On-time"},
                    {"value": "delayed", "label": "Delayed"},
                    {"value": "notYet", "label": "Not yet acquired"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"When did " + '
                '(formState.preferredName || "Your child") + '
                '" reach their toileting milestones (e.g., potty training)?"'
            },
        },
    )

    def get_field_groups(self):
        return {}


class DevelopmentalQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = DevelopmentalQuestionnaire

    _links = Hyperlinks(
        {
            "self": URLFor("api.questionnaireendpoint", name="developmental_questionnaire", id="<id>"),
        }
    )
