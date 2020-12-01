from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.export_service import ExportService


class TaskAssessmentMixin(object):
    """
    SkillStar: Task Assessment
    """
    info = {}
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __label__ = "Task Assessment"
    __estimated_duration_minutes__ = 1

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)
    tasks = [
        {"id": "task_01", "label": "Put toothpaste on your toothbrush"},
        {"id": "task_02", "label": "Put toothpaste away"},
        {"id": "task_03", "label": "Rinse toothbrush"},
        {"id": "task_04", "label": "Brush top surface of bottom teeth on right side."},
        {"id": "task_05", "label": "Brush top surface of bottom teeth on left side."},
        {"id": "task_06", "label": "Brush top surface of top teeth on right side"},
        {"id": "task_07", "label": "Brush top surface of top teeth on left side"},
        {"id": "task_08", "label": "Brush outside surface (facing cheek) of bottom teeth on right side"},
        {"id": "task_09", "label": "Brush outside surface (facing lips) of bottom teeth at the front of your mouth"},
        {"id": "task_10", "label": "Brush outside surface (facing cheek) of bottom teeth on left side"},
        {"id": "task_11", "label": "Brush outside surface (facing cheek) of top teeth on right side"},
        {"id": "task_12", "label": "Brush outside surface (facing lips) of top teeth at the front of your mouth"},
        {"id": "task_13", "label": "Brush outside surface (facing cheek) of top teeth on left side"},
        {"id": "task_14", "label": "Brush the inside surface (facing tongue) of bottom teeth on right side."},
        {"id": "task_15", "label": "Brush the inside surface (facing tongue) of bottom teeth on left side"},
        {"id": "task_16", "label": "Brush the inside surface (facing tongue) of top teeth on left side."},
        {"id": "task_17", "label": "Brush the inside surface (facing tongue) of top teeth on right side."},
        {"id": "task_18", "label": "Spit in the sink"},
        {"id": "task_19", "label": "Rinse toothbrush and put it away"},
        {"id": "task_20", "label": "Get your cup and fill with water"},
        {"id": "task_21", "label": "Rinse mouth and spit in sink"},
        {"id": "task_22", "label": "Wipe your face with a towel"},
        {"id": "task_23", "label": "Clean up"},
    ]

    @declared_attr
    def participant_id(cls):
        return db.Column("participant_id", db.Integer, db.ForeignKey("stardrive_participant.id"))

    @declared_attr
    def user_id(cls):
        return db.Column("user_id", db.Integer, db.ForeignKey("stardrive_user.id"))

    @declared_attr
    def is_task_complete(cls):
        options = []
        for task in cls.tasks:
            options.append({
                "value": task["id"] + "_complete",
                "label": task["label"],
            })
        return db.Column(
            db.ARRAY(db.String),
            info={
                "display_order": 1.1,
                "type": "multicheckbox",
                "template_options": {
                    "type": "array",
                    "label": "Task Complete?",
                    "required": True,
                    "description": "(select all that apply)",
                    "options": options,
                    "validators": {"required": "multicheckbox"},
                },
            },
        )

    @declared_attr
    def has_challenging_behavior(cls):
        options = []
        for task in cls.tasks:
            options.append({
                "value": task["id"] + "_challenge",
                "label": task["label"],
            })
        return db.Column(
            db.ARRAY(db.String),
            info={
                "display_order": 1.1,
                "type": "multicheckbox",
                "template_options": {
                    "type": "array",
                    "label": "Challenging Behavior?",
                    "required": True,
                    "description": "(select all that apply)",
                    "options": options,
                    "validators": {"required": "multicheckbox"},
                },
            },
        )

    def get_field_groups(self):
        return {}
