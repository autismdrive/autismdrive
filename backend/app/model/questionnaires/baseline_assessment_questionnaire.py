from marshmallow import pre_load
from sqlalchemy import func

from app import db, ma
from app.export_service import ExportService
from app.schema.model_schema import ModelSchema
from app.model.questionnaires.task_assessment_mixin import TaskAssessmentMixin


class BaselineAssessmentQuestionnaire(db.Model, TaskAssessmentMixin):
    """
    SkillStar: Baseline Assessment Questionnaire
    """
    __tablename__ = "baseline_assessment_questionnaire"
    __label__ = "SkillStar Baseline Assessment"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("stardrive_user.id")
    )

    def get_field_groups(self):
        return super().get_field_groups()


class BaselineAssessmentQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = BaselineAssessmentQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "is_task_complete",
            "has_challenging_behavior",
            "_links"
        )
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.questionnaireendpoint', name="baseline_assessment_questionnaire", id='<id>')
    })
