from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.export_service import ExportService


class CurrentBehaviorsMixin(object):
    info = {}
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __label__ = "Current Behaviors"
    __estimated_duration_minutes__ = 5
    academic_difficulty_other_hide_expression = '!(model.academic_difficulty_areas && model.academic_difficulty_areas.includes("other"))'

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    @declared_attr
    def participant_id(cls):
        return db.Column("participant_id", db.Integer, db.ForeignKey("stardrive_participant.id"))

    @declared_attr
    def user_id(cls):
        return db.Column("user_id", db.Integer, db.ForeignKey("stardrive_user.id"))

    @declared_attr
    def has_academic_difficulties(cls):
        return db.Column(
            db.Boolean,
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
        return db.Column(
            db.ARRAY(db.String),
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
                    "template_options.required": "model.has_academic_difficulties"
                },
                "hide_expression": "!(model.has_academic_difficulties)",
                "validators": {"required": "multicheckbox"},
            },
        )

    academic_difficulty_other = db.Column(
        db.String,
        info={
            "display_order": 4.2,
            "type": "input",
            "template_options": {
                "label": "Enter area of academic difficulty",
                "required": True
            },
            "hide_expression": academic_difficulty_other_hide_expression,
            "expression_properties": {
                "template_options.required": '!' + academic_difficulty_other_hide_expression
            }
        },
    )

    def get_field_groups(self):
        return {}