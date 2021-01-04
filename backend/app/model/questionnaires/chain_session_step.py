from marshmallow import missing, pre_load
from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

from app import db, ma
from app.schema.model_schema import ModelSchema
from app.export_service import ExportService
from app.model.chain_step import ChainStep
from app.model.questionnaires.challenging_behavior import ChallengingBehavior, ChallengingBehaviorSchema
from app.schema.chain_step_schema import ChainStepSchema


class ChainSessionStep(db.Model):
    __tablename__ = "chain_session_step"
    __label__ = "ChainSessionStep"
    __no_export__ = True  # This will be transferred as a part of a parent class
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 1

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    chain_session_id = db.Column(
        "chain_session_id",
        db.Integer,
        db.ForeignKey("chain_session.id")
    )

    @declared_attr
    def chain_step_id(cls):
        options = []
        try:
            chain_steps = db.session.query(ChainStep).all()
            sorted_steps = sorted(chain_steps, key=lambda chain_step: chain_step.id)
            options = [{"value": s.id, "label": s.instruction} for s in sorted_steps]
        except:
            pass

        return db.Column("chain_step_id", db.Integer, db.ForeignKey('chain_step.id'), info={
                "display_order": 1,
                "type": "select",
                "template_options": {
                    "required": True,
                    "label": 'Task',
                    "options": options,
                },
            }
         )

    date = db.Column(
        db.DateTime,
        info={
            "display_order": 2,
            "type": "datepicker",
            "template_options": {
                "required": True,
                "label": 'Step Date',
            },
        },
    )

    status = db.Column(
        db.String,
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Step Status",
                "required": True,
                "options": [
                    {
                        "value": "not_complete",
                        "label": "Not complete"
                    },
                    {
                        "value": "focus",
                        "label": "Focus"
                    },
                    {
                        "value": "mastered",
                        "label": "Mastered"
                    },
                ],
            },
        },
    )

    completed = db.Column(
        db.Boolean,
        info={
            "display_order": 4,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Task Complete?",
                "required": True,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    was_prompted = db.Column(
        db.Boolean,
        info={
            "display_order": 5,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Was Prompted?",
                "required": True,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    prompt_level = db.Column(
        db.String,
        info={
            "display_order": 6,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "What prompt did you use to complete the step?",
                "required": True,
                "options": [
                    {
                        "value": "none",
                        "label": "No Prompt (Independent)"
                    },
                    {
                        "value": "shadow",
                        "label": "Shadow Prompt (approximately one inch)"
                    },
                    {
                        "value": "partial_physical",
                        "label": "Partial Physical Prompt (thumb and index finger)"
                    },
                    {
                        "value": "full_physical",
                        "label": "Full Physical Prompt (hand-over-hand)"
                    },
                ],
            },
        },
    )

    had_challenging_behavior = db.Column(
        db.Boolean,
        info={
            "display_order": 7,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Challenging Behavior?",
                "required": True,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    challenging_behavior_severity = db.Column(
        db.String,
        info={
            "display_order": 8,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "How severe was the challenging behavior?",
                "required": True,
                "options": [
                    {
                        "value": "mild",
                        "label": "Mild (did not interfere with task)"
                    },
                    {
                        "value": "moderate",
                        "label": "Moderate (interfered with task, but we were able to work through it)"
                    },
                    {
                        "value": 'severe',
                        "label": "Severe (we were not able to complete the task due to the severity of the behavior)"
                    },
                ],
            },
        },
    )

    challenging_behaviors = db.relationship(
        "ChallengingBehavior",
        backref=db.backref("chain_session_step", lazy=True),
        cascade="all, delete-orphan",
        passive_deletes=True
    )


    @declared_attr
    def participant_id(cls):
        return db.Column("participant_id", db.Integer, db.ForeignKey("stardrive_participant.id"))

    @declared_attr
    def user_id(cls):
        return db.Column("user_id", db.Integer, db.ForeignKey("stardrive_user.id"))

    def get_field_groups(self):
        field_groups = {
            "challenging_behaviors": {
                "type": "repeat",
                "display_order": 9,
                "wrappers": ["card"],
                "repeat_class": ChallengingBehavior,
                "template_options": {
                    "label": "",
                    "description": "Add a challenging behavior",
                },
            },
        }
        return field_groups


class ChainSessionStepSchema(ModelSchema):
    # @pre_load
    # def set_field_session(self, data, **kwargs):
    #     self.fields['challenging_behaviors'].schema.session = self.session
    #     return data

    class Meta(ModelSchema.Meta):
        model = ChainSessionStep
        fields = (
            "id",
            "last_updated",
            "chain_step_id",
            "chain_step",
            "date",
            "status",
            "completed",
            "was_prompted",
            "prompt_level",
            "had_challenging_behavior",
            "challenging_behavior_severity",
            "challenging_behaviors",
        )
    challenging_behaviors = ma.Nested(ChallengingBehaviorSchema, many=True)
    chain_step = ma.Method('get_chain_step', dump_only=True)

    def get_chain_step(self, obj):
        if obj is None:
            return missing

        db_chain_step = db.session.query(ChainStep).filter_by(id=obj.chain_step_id).first()
        return ChainStepSchema().dump(db_chain_step)
