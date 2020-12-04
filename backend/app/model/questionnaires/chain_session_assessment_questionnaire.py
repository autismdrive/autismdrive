from marshmallow import pre_load
from sqlalchemy import func

from app import db, ma
from app.export_service import ExportService
from app.schema.model_schema import ModelSchema
from app.model.questionnaires.chain_session_step_mixin import ChainSessionStepMixin
from app.model.questionnaires.chain_session_step import ChainSessionStepSchema


class ChainSessionAssessmentQuestionnaire(db.Model, ChainSessionStepMixin):
    """
    SkillStar: Chain Session Assessment Questionnaire
    """
    __tablename__ = "chain_session_assessment_questionnaire"
    __label__ = "SkillStar Chain Session Assessment"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    date_introduced = db.Column(db.DateTime(timezone=True), nullable=True)
    date_mastered = db.Column(db.DateTime(timezone=True), nullable=True)
    date_booster_required = db.Column(db.DateTime(timezone=True), nullable=True)
    date_booster_mastered = db.Column(db.DateTime(timezone=True), nullable=True)
    date_attempted = db.Column(db.DateTime(timezone=True), nullable=True)
    prompt_level = db.Column(db.String)
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

    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("stardrive_user.id")
    )

    def get_field_groups(self):
        return super().get_field_groups()


class ChainSessionAssessmentQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields['focus_steps'].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = ChainSessionAssessmentQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "focus_steps",
            "date_introduced",
            "date_mastered",
            "date_booster_required",
            "date_booster_mastered",
            "date_attempted",
            # "prompt_level",
            "_links"
        )
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.questionnaireendpoint', name="chain_session_assessment_questionnaire", id='<id>')
    })

    focus_steps = ma.Nested(ChainSessionStepSchema, many=True)

