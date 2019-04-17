from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.education_mixin import EducationMixin


class EducationDependentQuestionnaire(db.Model, EducationMixin):
    __tablename__ = "education_dependent_questionnaire"
    __label__ = "Education"

    attends_school_desc = '"Does " + (formState.preferredName || "your child") + " attend school?"'
    school_type_desc = '"Is " + (formState.preferredName || "your child") + "\'s school:"'
    school_services_desc = '"Please check the following services " + (formState.preferredName || "your child") + " currently receives in school (check all that apply):"'
    placement_other_hide_expression = '!(model.dependent_placement && model.dependent_placement === "schoolOther")'
    current_grade_hide_expression = '!(model.dependent_placement && model.dependent_placement === "grades1to12")'

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
                    {"value": "homeSchool", "label": "Home schooled"},
                    {"value": "vocational", "label": "Vocational school where I am learning job or life skills"},
                    {"value": "college", "label": "College/university"},
                    {"value": "graduate", "label": "Graduate school"},
                    {"value": "schoolOther", "label": "Other"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"What is " + (formState.preferredName || "your child") + "\'s '
                                          'current grade/school placement?"',
            },
            "hide_expression": '!(model.attends_school)',
        },
    )

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["placement_group"]["fields"] = [
            "dependent_placement",
            "placement_other",
            "current_grade"
        ]
        return field_groups


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
        ordered = True
