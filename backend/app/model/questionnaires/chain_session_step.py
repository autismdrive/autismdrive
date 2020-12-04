from marshmallow import fields, missing
from sqlalchemy import func

from app import db
from app.schema.model_schema import ModelSchema


class ChainSessionStep(db.Model):
    __tablename__ = "chain_session_step"
    __label__ = "ChainSessionStep"
    __no_export__ = True  # This will be transferred as a part of a parent class

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    chain_session_assessment_questionnaire_id = db.Column(
        "chain_session_assessment_questionnaire_id",
        db.Integer,
        db.ForeignKey("chain_session_assessment_questionnaire.id"),
    )

    def get_field_groups(self):
        return {}


class ChainSessionStepSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ChainSessionStep
        fields = ("id", "last_updated", "chain_session_assessment_questionnaire_id", "participant_id", "user_id")
    participant_id = fields.Method('get_participant_id')
    user_id = fields.Method('get_user_id')
    chain_session_assessment_questionnaire_id = fields.Integer(required=False, allow_none=True)
    home_self_questionnaire_id = fields.Integer(required=False, allow_none=True)
    chain_session_assessment_questionnaire = fields.Nested('ChainSessionAssessmentQuestionnaire', required=False, allow_none=True)

    def get_participant_id(self, obj):
        if obj is None:
            return missing
        elif obj.chain_session_assessment_questionnaire is not None:
            return obj.chain_session_assessment_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing
        elif obj.chain_session_assessment_questionnaire is not None:
            return obj.chain_session_assessment_questionnaire.user_id
