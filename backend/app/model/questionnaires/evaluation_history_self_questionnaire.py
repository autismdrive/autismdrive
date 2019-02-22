from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.evaluation_history_mixin import EvaluationHistoryMixin


class EvaluationHistorySelfQuestionnaire(db.Model, EvaluationHistoryMixin):
    __tablename__ = "evaluation_history_self_questionnaire"

    def get_meta(self):
        info = {}

        info.update(EvaluationHistoryMixin.info)

        info["field_groups"]["partner_centers"]["template_options"]["label"] = \
            "Have you ever been evaluated at any of the following centers?"

        for c in self.metadata.tables["evaluation_history_self_questionnaire"].columns:
            if c.info:
                info[c.name] = c.info

        info["self_identifies_autistic"]["template_options"]["label"] = "Do you self-identify as having Autism?"
        info["has_autism_diagnosis"]["template_options"]["label"] = "Have you been formally diagnosed with Autism Spectrum Disorder?"
        info["years_old_at_first_diagnosis"]["template_options"]["label"] = "How old were you when you were first diagnosed with ASD?"
        info["who_diagnosed"]["template_options"]["label"] = "Who first diagnosed you with ASD?"
        info["where_diagnosed"]["template_options"]["label"] = "Where did you receive this diagnosis?"
        info["gives_permission_to_link_evaluation_data"]["template_options"]["label"] = "Do we have your permission to link your evaluation data to the UVA Autism Database?"
        info["has_iq_test"]["template_options"]["label"] = "Have you been given an IQ or intelligence test?"
        info["recent_iq_score"]["template_options"]["label"] = "What was your most recent IQ score?"

        return info


class EvaluationHistorySelfQuestionnaireSchema(ModelSchema):
    class Meta:
        model = EvaluationHistorySelfQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "self_identifies_autistic",
            "has_autism_diagnosis",
            "years_old_at_first_diagnosis",
            "who_diagnosed",
            "who_diagnosed_other",
            "where_diagnosed",
            "where_diagnosed_other",
            "partner_centers_evaluation",
            "gives_permission_to_link_evaluation_data",
            "has_iq_test",
            "recent_iq_score",
        )


class EvaluationHistorySelfQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = EvaluationHistorySelfQuestionnaire
        fields = ("get_meta",)
