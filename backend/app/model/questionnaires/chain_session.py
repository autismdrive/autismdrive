from marshmallow import fields, missing, pre_load
from sqlalchemy import func, Column, Integer, DateTime, BigInteger, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, backref, declared_attr

from app.database import session, Base
from app.export_service import ExportService
from app.model.chain_step import ChainStep
from app.schema.chain_step_schema import ChainStepSchema
from app.schema.model_schema import ModelSchema


class ChainQuestionnaire(Base):
    __tablename__ = "chain_questionnaire"
    __label__ = "SkillSTAR Chain Questionnaire"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

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
    def sessions(cls):
        return relationship(
            "ChainSession",
            backref=backref(cls.__tablename__, lazy=True),
            cascade="all, delete-orphan",
            passive_deletes=True,
        )


class ChainSession(Base):
    """
    SkillStar: Chain Session
    """

    __tablename__ = "chain_session"
    __label__ = "SkillSTAR Chain Session"
    __no_export__ = True  # This will be transferred as a part of a parent class
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    time_on_task_ms = Column(BigInteger, default=0)

    chain_questionnaire_id = Column("chain_questionnaire_id", Integer, ForeignKey("chain_questionnaire.id"))

    date = Column(
        DateTime(timezone=True),
        info={
            "display_order": 1,
            "type": "datepicker",
            "template_options": {
                "required": True,
                "label": "Session Date",
            },
        },
    )

    completed = Column(
        Boolean,
        info={
            "display_order": 2,
            "type": "radio",
            "template_options": {
                "required": True,
                "label": "Session Complete?",
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    session_type = Column(
        String,
        info={
            "display_order": 2,
            "type": "radio",
            "template_options": {
                "required": True,
                "label": "Session Type",
                "options": [
                    {"value": "training", "label": "Training"},
                    {"value": "probe", "label": "Probe"},
                    {"value": "booster", "label": "Booster"},
                ],
            },
        },
    )


class ChainSessionSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields["step_attempts"].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = ChainSession
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "date",
            "completed",
            "session_type",
            "session_number",
            "chain_questionnaire_id",
            "step_attempts",
        )

    step_attempts = fields.Nested(lambda: ChainSessionStepSchema, many=True)
    participant_id = fields.Method("get_participant_id", dump_only=True)
    user_id = fields.Method("get_user_id", dump_only=True)
    session_number = fields.Method("get_session_number", dump_only=True)

    def get_participant_id(self, obj):
        if obj is None:
            return missing

        return obj.chain_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing

        return obj.chain_questionnaire.user_id

    def get_session_number(self, obj):
        if obj is None:
            return missing

        # Sort sessions by date
        sorted_sessions = sorted(obj.chain_questionnaire.sessions, key=lambda k: k.date)

        # Find this session and return its index, incremented.
        for i, session in enumerate(sorted_sessions):
            if obj.id == session.id:
                return i + 1

        # Session not found.
        return -1


class ChallengingBehavior(Base):
    __tablename__ = "challenging_behavior"
    __label__ = "ChallengingBehavior"
    __no_export__ = True  # This will be transferred as a part of a parent class

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    chain_session_step_id = Column("chain_session_step_id", Integer, ForeignKey("chain_session_step.id"))
    time = Column(
        DateTime,
        info={
            "display_order": 1,
            "type": "datepicker",
            "template_options": {
                "label": "Time challenging behavior occurred",
            },
        },
    )

    def get_field_groups(self):
        info = {}
        return info


class ChallengingBehaviorSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ChallengingBehavior
        fields = ("id", "last_updated", "chain_session_step_id", "time")


class ChainSessionStep(Base):
    __tablename__ = "chain_session_step"
    __label__ = "ChainSessionStep"
    __no_export__ = True  # This will be transferred as a part of a parent class
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 1
    training_session_hide_expression = '!(model.session_type && (model.session_type === "training"))'
    focus_step_hide_expression = "!model.was_focus_step"

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    chain_session_id = Column("chain_session_id", Integer, ForeignKey(ChainSession.id))

    @declared_attr
    def chain_step_id(cls):
        options = []
        try:
            chain_steps = session.query(ChainStep).all()
            sorted_steps = sorted(chain_steps, key=lambda chain_step: chain_step.id)
            options = [{"value": s.id, "label": s.instruction} for s in sorted_steps]
        except:
            pass

        return Column(
            "chain_step_id",
            Integer,
            ForeignKey("chain_step.id"),
            info={
                "display_order": 1,
                "type": "select",
                "template_options": {
                    "required": True,
                    "label": "Task",
                    "options": options,
                },
            },
        )

    date = Column(
        DateTime(timezone=True),
        info={
            "display_order": 2,
            "type": "datepicker",
            "template_options": {
                "required": True,
                "label": "Step Date",
            },
        },
    )

    was_focus_step = Column(
        Boolean,
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
            "expression_properties": {"template_options.required": "!" + training_session_hide_expression},
        },
    )

    target_prompt_level = Column(
        String,
        info={
            "display_order": 4,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "What prompt level was targeted for the focus step?",
                "required": True,
                "options": [
                    {"value": "none", "label": "No Prompt (Independent)"},
                    {"value": "shadow", "label": "Shadow Prompt (approximately one inch)"},
                    {"value": "partial_physical", "label": "Partial Physical Prompt (thumb and index finger)"},
                    {"value": "full_physical", "label": "Full Physical Prompt (hand-over-hand)"},
                ],
            },
            "hide_expression": focus_step_hide_expression,
            "expression_properties": {"template_options.required": "!" + focus_step_hide_expression},
        },
    )

    status = Column(
        String,
        info={
            "display_order": 5,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Step Status",
                "required": True,
                "options": [
                    {"value": "not_yet_started", "label": "Not yet started"},
                    {"value": "not_complete", "label": "Not complete"},
                    {"value": "focus", "label": "Focus"},
                    {"value": "mastered", "label": "Mastered"},
                    {"value": "booster_needed", "label": "Booster needed"},
                    {"value": "booster_mastered", "label": "Booster mastered"},
                ],
            },
        },
    )

    completed = Column(
        Boolean,
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

    was_prompted = Column(
        Boolean,
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

    prompt_level = Column(
        String,
        info={
            "display_order": 8,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "What prompt did you use to complete the step?",
                "required": True,
                "options": [
                    {"value": "none", "label": "No Prompt (Independent)"},
                    {"value": "shadow", "label": "Shadow Prompt (approximately one inch)"},
                    {"value": "partial_physical", "label": "Partial Physical Prompt (thumb and index finger)"},
                    {"value": "full_physical", "label": "Full Physical Prompt (hand-over-hand)"},
                ],
            },
        },
    )

    had_challenging_behavior = Column(
        Boolean,
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

    reason_step_incomplete = Column(
        String,
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

    challenging_behaviors = relationship(
        "ChallengingBehavior",
        backref=backref("chain_session_step", lazy=True),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    num_stars = Column(Integer, nullable=True)


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
            "chain_session_id",
            "chain_step_id",
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
            "session_number",
            "num_stars",
            "challenging_behaviors",
            "chain_step",
        )

    participant_id = fields.Method("get_participant_id", dump_only=True)
    user_id = fields.Method("get_user_id", dump_only=True)
    challenging_behaviors = fields.Nested(ChallengingBehaviorSchema, many=True)
    chain_step = fields.Method("get_chain_step", dump_only=True)
    session_type = fields.Method("get_session_type", dump_only=True)
    session_number = fields.Method("get_session_number", dump_only=True)

    def get_chain_step(self, obj):
        if obj is None:
            return missing

        db_chain_step = session.query(ChainStep).filter_by(id=obj.chain_step_id).first()
        return ChainStepSchema().dump(db_chain_step)

    def get_session_type(self, obj):
        if obj is None:
            return missing

        return obj.chain_session.session_type

    def get_session_number(self, obj):
        if obj is None:
            return missing

        # Sort sessions by date
        sorted_sessions = sorted(obj.chain_session.chain_questionnaire.sessions, key=lambda k: k.date)

        # Find this session and return its index, incremented.
        for i, session in enumerate(sorted_sessions):
            if obj.chain_session.id == session.id:
                return i + 1

        # Session not found.
        return -1

    def get_participant_id(self, obj):
        if obj is None:
            return missing

        return obj.chain_session.chain_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing

        return obj.chain_session.chain_questionnaire.user_id


ChainSession.step_attempts = relationship(
    "ChainSessionStep", backref="chain_session", cascade="all, delete-orphan", passive_deletes=True
)


class ChainQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields["sessions"].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = ChainQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "sessions",
        )

    sessions = fields.Nested(ChainSessionSchema, many=True)


def _get_chain_session_field_groups(_self):
    return {
        "step_attempts": {
            "type": "repeat",
            "display_order": 3,
            "wrappers": ["card"],
            "repeat_class": ChainSessionStep,
            "template_options": {
                "label": "Which tasks were attempted?",
                "description": "Add a step",
            },
            "expression_properties": {},
        },
    }


def _get_chain_session_step_field_groups(_self):
    return {
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


def _get_chain_questionnaire_field_groups(_self):
    return {
        "sessions": {
            "type": "repeat",
            "display_order": 3,
            "wrappers": ["card"],
            "repeat_class": ChainSession,
            "template_options": {
                "label": "Chain Session",
                "description": "Add a session",
            },
            "expression_properties": {},
        },
    }


ChainSession.get_field_groups = _get_chain_session_field_groups
ChainSessionStep.get_field_groups = _get_chain_session_step_field_groups
ChainQuestionnaire.get_field_groups = _get_chain_questionnaire_field_groups
