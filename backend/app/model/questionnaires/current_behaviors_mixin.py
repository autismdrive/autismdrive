import datetime

from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.question_service import QuestionService


class CurrentBehaviorsMixin(object):
    info = {}
    __question_type__ = QuestionService.TYPE_UNRESTRICTED
    __label__ = "Current Behaviors"
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    @declared_attr
    def participant_id(cls):
        return db.Column("participant_id", db.Integer, db.ForeignKey("stardrive_participant.id"))

    @declared_attr
    def user_id(cls):
        return db.Column("user_id", db.Integer, db.ForeignKey("stardrive_user.id"))

    has_academic_difficulties = db.Column(
        db.Boolean,
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "label": '',
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
            "expression_properties": {}
        },
    )
    academic_difficulty_areas = db.Column(
        db.String,
        info={
            "display_order": 4,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "label": '',
                "required": True,
                "options": [
                    {"value": "math", "label": "Math"},
                    {"value": "reading", "label": "Reading"},
                    {"value": "writing", "label": "Writing"},
                    {"value": "other", "label": "Other"},
                ],
            },
            "expression_properties": {},
            "hide_expression": "!(model.has_academic_difficulties)",
        },
    )
    academic_difficulty_other = db.Column(
        db.String,
        info={
            "display_order": 4.2,
            "type": "input",
            "template_options": {
                "placeholder": "Enter area of academic difficulty"
            },
            "hide_expression": "!(model.academic_difficulty_areas && (model.academic_difficulty_areas.other))",
        },
    )
