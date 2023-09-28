from flask_sqlalchemy.model import Model
from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, Boolean, BigInteger, ARRAY
from sqlalchemy.ext.declarative import declared_attr

from app.export_service import ExportService


class CurrentBehaviorsMixin(Model):
    info = {}
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __label__ = "Current Behaviors"
    __estimated_duration_minutes__ = 5
    academic_difficulty_other_hide_expression = (
        '!(model.academic_difficulty_areas && model.academic_difficulty_areas.includes("other"))'
    )

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    time_on_task_ms = Column(BigInteger, default=0)

    @declared_attr
    def participant_id(cls):
        return Column("participant_id", Integer, ForeignKey("stardrive_participant.id"))

    @declared_attr
    def user_id(cls):
        return Column("user_id", Integer, ForeignKey("stardrive_user.id"))

    @declared_attr
    def has_academic_difficulties(cls):
        return Column(
            Boolean,
            info={
                "display_order": 3,
                "type": "radio",
                "template_options": {
                    "label": "Academic Difficulties",
                    "required": False,
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": cls.has_academic_difficulties_desc,
                },
            },
        )

    @declared_attr
    def academic_difficulty_areas(cls):
        return Column(
            ARRAY(String),
            info={
                "display_order": 4,
                "type": "multicheckbox",
                "template_options": {
                    "type": "array",
                    "label": "Area of difficulty",
                    "required": True,
                    "options": [
                        {"value": "math", "label": "Math"},
                        {"value": "reading", "label": "Reading"},
                        {"value": "writing", "label": "Writing"},
                        {"value": "other", "label": "Other"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": cls.academic_difficulty_areas_desc,
                    "template_options.required": "model.has_academic_difficulties",
                },
                "hide_expression": "!(model.has_academic_difficulties)",
                "validators": {"required": "multicheckbox"},
            },
        )

    academic_difficulty_other = Column(
        String,
        info={
            "display_order": 4.2,
            "type": "input",
            "template_options": {"label": "Enter area of academic difficulty", "required": True},
            "hide_expression": academic_difficulty_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + academic_difficulty_other_hide_expression},
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_field_groups(self):
        return {}
