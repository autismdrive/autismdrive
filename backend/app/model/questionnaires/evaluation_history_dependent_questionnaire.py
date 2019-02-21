from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.evaluation_history_mixin import EvaluationHistoryMixin


class EvaluationHistoryDependentQuestionnaire(db.Model, EvaluationHistoryMixin):
    __tablename__ = "evaluation_history_dependent_questionnaire"

    def get_meta(self):
        info = {}

        info.update(EvaluationHistoryMixin.info)

        info["field_groups"]["partner_centers"]["expression_properties"]["template_options.label"] = \
            '"Has " + (formState.mainModel.preferred_name || "your child") + ' \
            '" ever been evaluated at any of the following centers?"'

        for c in self.metadata.tables["evaluation_history_dependent_questionnaire"].columns:
            if c.info:
                info[c.name] = c.info

        info["self_identifies_autistic"]["expression_properties"]["template_options.label"] = \
            '"Does " + (formState.mainModel.preferred_name || "your child") + " self-identify as having Autism?"'
        info["has_autism_diagnosis"]["expression_properties"]["template_options.label"] = \
            '"Has " + (formState.mainModel.preferred_name || "your child") + " been formally diagnosed with Autism ' \
            'Spectrum Disorder?"'
        info["years_old_at_first_diagnosis"]["expression_properties"]["template_options.label"] = \
            '"How old was " + (formState.mainModel.preferred_name || "your child") + " when they were first ' \
            'diagnosed with ASD?"'
        info["who_diagnosed"]["expression_properties"]["template_options.label"] = \
            '"Who first diagnosed " + (formState.mainModel.preferred_name || "your child") + " with ASD?"'
        info["where_diagnosed"]["expression_properties"]["template_options.label"] = \
            '"Where did " + (formState.mainModel.preferred_name || "your child") + " receive this diagnosis?"'
        info["gives_permission_to_link_evaluation_data"]["expression_properties"]["template_options.label"] = \
            '"Do we have your permission to link " + (formState.mainModel.preferred_name + "\'s") + ' \
            '" evaluation data to the UVa Autism Database?"'
        info["has_iq_test"]["expression_properties"]["template_options.label"] = \
            '"Has " + (formState.mainModel.preferred_name) + " been given an IQ or intelligence test?"'
        info["recent_iq_score"]["expression_properties"]["template_options.label"] = \
            '"What was " + (formState.mainModel.preferred_name + "\'s") + " most recent IQ score?"'

        return info


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


class EvaluationHistoryDependentQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = EvaluationHistoryDependentQuestionnaire
        fields = ("get_meta",)
