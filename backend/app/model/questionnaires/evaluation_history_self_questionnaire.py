from app import db, ma
from app.model.questionnaires.evaluation_history_mixin import EvaluationHistoryMixin
from app.schema.model_schema import ModelSchema


class EvaluationHistorySelfQuestionnaire(db.Model, EvaluationHistoryMixin):
    __tablename__ = "evaluation_history_self_questionnaire"
    __label__ = "Evaluation History"

    has_autism_diagnosis_label = '"Have you been formally diagnosed with Autism Spectrum Disorder?"'
    self_identifies_autistic_label = '"Do you have autism?"'
    years_old_at_first_diagnosis_label = '"How old were you (in years) when you were first diagnosed with ASD?"'
    who_diagnosed_label = '"Who first diagnosed you with ASD?"'
    where_diagnosed_label = '"Where did you receive this diagnosis?"'
    gives_permission_to_link_evaluation_data_desc = '"Do we have your permission to link your evaluation data to the UVA Autism Database?"'
    has_iq_test_desc = '"Have you been given an IQ or intelligence test?"'

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["partner_centers"]["template_options"]["label"] = \
            "Have you ever been evaluated at any of the following centers?"
        return field_groups


class EvaluationHistorySelfQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EvaluationHistorySelfQuestionnaire
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
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.questionnaireendpoint', name='evaluation_history_self_questionnaire', id='<id>'),
    })
