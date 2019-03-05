from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.evaluation_history_mixin import EvaluationHistoryMixin


class EvaluationHistoryDependentQuestionnaire(db.Model, EvaluationHistoryMixin):
    __tablename__ = "evaluation_history_dependent_questionnaire"
    __label__ = "Evaluation History"

    self_identifies_autistic_label = '"Does " + (model.preferred_name || "your child") + " self-identify as having Autism?"'
    has_autism_diagnosis_label = '"Has " + (model.preferred_name || "your child") + " been formally diagnosed with Autism Spectrum Disorder?"'
    years_old_at_first_diagnosis_label = '"How old was " + (model.preferred_name || "your child") + " when they were first diagnosed with ASD?"'
    who_diagnosed_label = '"Who first diagnosed " + (model.preferred_name || "your child") + " with ASD?"'
    where_diagnosed_label = '"Where did " + (model.preferred_name || "your child") + " receive this diagnosis?"'
    gives_permission_to_link_evaluation_data_label = '"Do we have your permission to link " + (model.preferred_name + "\'s") + " evaluation data to the UVa Autism Database?"'
    has_iq_test_label = '"Has " + (model.preferred_name) + " been given an IQ or intelligence test?"'
    recent_iq_score_label = '"What was " + (model.preferred_name + "\'s") + " most recent IQ score?"'

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["partner_centers"]["expression_properties"]["template_options.label"] = \
            '"Has " + (model.preferred_name || "your child") + ' \
            '" ever been evaluated at any of the following centers?"'


class EvaluationHistoryDependentQuestionnaireSchema(ModelSchema):
    class Meta:
        model = EvaluationHistoryDependentQuestionnaire
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
