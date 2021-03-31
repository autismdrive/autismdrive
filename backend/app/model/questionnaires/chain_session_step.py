from marshmallow import fields, missing, pre_load
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
    training_session_hide_expression = '!(model.session_type && (model.session_type === "training"))'
    focus_step_hide_expression = '!model.was_focus_step'

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
        db.DateTime(timezone=True),
        info={
            "display_order": 2,
            "type": "datepicker",
            "template_options": {
                "required": True,
                "label": 'Step Date',
            },
        },
    )

    was_focus_step = db.Column(
        db.Boolean,
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Focus Step",
                "required": True,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
            "hide_expression": training_session_hide_expression,
            "expression_properties": {
                "template_options.required": '!' + training_session_hide_expression
            },
        },
    )

    target_prompt_level = db.Column(
        db.String,
        info={
            "display_order": 4,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "What prompt level was targeted for the focus step?",
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
            "hide_expression": focus_step_hide_expression,
            "expression_properties": {
                "template_options.required": '!' + focus_step_hide_expression
            },
        },
    )

    status = db.Column(
        db.String,
        info={
            "display_order": 5,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Step Status",
                "required": True,
                "options": [
                    {
                        "value": "not_yet_started",
                        "label": "Not yet started"
                    },
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
                    {
                        "value": "booster_needed",
                        "label": "Booster needed"
                    },
                    {
                        "value": "booster_mastered",
                        "label": "Booster mastered"
                    },
                ],
            },
        },
    )

    completed = db.Column(
        db.Boolean,
        info={
            "display_order": 6,
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
            "display_order": 7,
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
            "display_order": 8,
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
            "display_order": 9,
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

    reason_step_incomplete = db.Column(
        db.String,
        info={
            "display_order": 10,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "What was the primary reason for failing to complete the task?",
                "required": True,
                "options": [
                    {"value": "lack_of_attending", "label": "Lack of Attending"},
                    {"value": "challenging_behavior", "label": "Challenging Behavior"},
                    {"value": "sensory_issues", "label": "Sensory Issues(materials are aversive)"},
                    {"value": "other", "label": "Other"},
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

    def get_field_groups(self):
        field_groups = {
            "challenging_behaviors": {
                "type": "repeat",
                "display_order": 11,
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
            "participant_id",
            "user_id",
            "chain_step_id",
            "chain_step",
            "date",
            "session_type",
            "was_focus_step",
            "target_prompt_level",
            "status",
            "completed",
            "was_prompted",
            "prompt_level",
            "had_challenging_behavior",
            "reason_step_incomplete",
            "challenging_behaviors",
            "chain_session_id"
        )
    participant_id = fields.Method('get_participant_id', dump_only=True)
    user_id = fields.Method('get_user_id', dump_only=True)
    challenging_behaviors = ma.Nested(ChallengingBehaviorSchema, many=True)
    chain_step = ma.Method('get_chain_step', dump_only=True)
    session_type = ma.Method('get_session_type', dump_only=True)

    def get_chain_step(self, obj):
        if obj is None:
            return missing

        db_chain_step = db.session.query(ChainStep).filter_by(id=obj.chain_step_id).first()
        return ChainStepSchema().dump(db_chain_step)

    def get_session_type(self, obj):
        if obj is None:
            return missing

        if hasattr(obj, 'chain_session'):
            return obj.chain_session.session_type

    def get_participant_id(self, obj):
        print('get_participant_id', obj)
        return obj.chain_session.chain_questionnaire.participant_id

    def get_user_id(self, obj):
        print('get_user_id', obj)
        return obj.chain_session.chain_questionnaire.user_id
