from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.education_mixin import EducationMixin


class EducationDependentQuestionnaire(db.Model, EducationMixin):
    __tablename__ = "education_dependent_questionnaire"

    dependent_placement = db.Column(
        db.String,
        info={
            "display_order": 4.2,
            "type": "select",
            "template_options": {
                "label": '',
                "required": False,
                "options": [
                    {"value": "daycare", "label": "Daycare center"},
                    {"value": "preschool", "label": "Preschool"},
                    {"value": "kindergarten", "label": "Kindergarten"},
                    {"value": "grades1to12", "label": "1st through 12th grade, please specify CURRENT GRADE below"},
                    {"value": "vocational", "label": "Vocational school where I am learning job or life skills"},
                    {"value": "college", "label": "College/university"},
                    {"value": "graduate", "label": "Graduate school"},
                    {"value": "schoolOther", "label": "Other"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"What is " + (formState.mainModel.preferred_name || "your child") + "\'s '
                                          'current grade/school placement?"',
            },
        },
    )

    def get_meta(self):
        info = {}

        info.update(EducationMixin.info)

        info["field_groups"]["placement_group"]["fields"] = [
            "dependent_placement",
            "placement_other",
        ]

        for c in self.metadata.tables["education_dependent_questionnaire"].columns:
            if c.info:
                info[c.name] = c.info

        info["attends_school"]["expression_properties"]["template_options.label"] = \
            '"Does " + (formState.mainModel.preferred_name || "your child") + " attend school?"'
        info["school_type"]["expression_properties"]["template_options.label"] = \
            '"Is " + (formState.mainModel.preferred_name || "your child") + "\'s school:"'
        info["school_services"]["expression_properties"]["template_options.label"] = \
            '"Please check the following services " + (formState.mainModel.preferred_name || "your child") + ' \
            '" currently receives in school (check all that apply):"'
        info["placement_other"]["hide_expression"] = \
            '!(model.dependent_placement && model.dependent_placement.schoolOther)'
        info["current_grade"]["hide_expression"] = \
            '!(model.dependent_placement && model.dependent_placement.grades1to12)'

        return info


class EducationDependentQuestionnaireSchema(ModelSchema):
    class Meta:
        model = EducationDependentQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "attends_school",
            "school_name",
            "school_type",
            "dependent_placement",
            "placement_other",
            "current_grade",
            "school_services",
            "school_services_other",
        )


class EducationDependentQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = EducationDependentQuestionnaire
        fields = ("get_meta",)
