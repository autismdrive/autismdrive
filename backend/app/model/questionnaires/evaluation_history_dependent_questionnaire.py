from marshmallow_sqlalchemy import ModelSchema

from app import db, ma
from app.model.questionnaires.evaluation_history_mixin import EvaluationHistoryMixin


class EvaluationHistoryDependentQuestionnaire(db.Model, EvaluationHistoryMixin):
    __tablename__ = "evaluation_history_dependent_questionnaire"
    __label__ = "Evaluation History"

    self_identifies_autistic_label = '"Does " + (formState.preferredName || "your child") + " self-identify as having Autism?"'
    has_autism_diagnosis_label = '"Has " + (formState.preferredName || "your child") + " been formally diagnosed with Autism Spectrum Disorder?"'
    years_old_at_first_diagnosis_label = '"How old (in years) was " + (formState.preferredName || "your child") + " when they were first diagnosed with ASD?"'
    who_diagnosed_label = '"Who first diagnosed " + (formState.preferredName || "your child") + " with ASD?"'
    where_diagnosed_label = '"Where did " + (formState.preferredName || "your child") + " receive this diagnosis?"'
    gives_permission_to_link_evaluation_data_desc = '"Do we have your permission to link " + (formState.preferredName + "\'s") + " evaluation data to the UVa Autism Database?"'
    has_iq_test_desc = '"Has " + (formState.preferredName) + " been given an IQ or intelligence test?"'

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["partner_centers"]["expression_properties"]["template_options.label"] = \
            '"Has " + (formState.preferredName || "your child") + ' \
            '" ever been evaluated at any of the following centers?"'
        return field_groups


class EvaluationHistoryDependentQuestionnaireSchema(ModelSchema):
    class Meta:
        model = EvaluationHistoryDependentQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
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
            "_links"
        )
        ordered = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.questionnaireendpoint', name='evaluation_history_dependent_questionnaire', id='<id>'),
    })