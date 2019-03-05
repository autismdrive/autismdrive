from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.education_mixin import EducationMixin


class EducationSelfQuestionnaire(db.Model, EducationMixin):
    __tablename__ = "education_self_questionnaire"
    __label__ = "Education"

    attends_school_label = '"Do you attend an academic program, such as a school, college, or university?"'
    school_type_label = '"Is this a public school, private school, or are you home schooled?"'
    school_services_label = '"Please check the following services you currently receive through your academic " \
                            "program (check all that apply):"'
    placement_other_hide_expression = '!(model.self_placement && model.self_placement.schoolOther)'
    current_grade_hide_expression = '!(model.self_placement && model.self_placement.highSchool)'

    self_placement = db.Column(
        db.String,
        info={
            "display_order": 4.1,
            "type": "select",
            "template_options": {
                "label": "What type of program is it?",
                "required": False,
                "options": [
                    {"value": "highSchool", "label": "High school, please specify CURRENT GRADE below"},
                    {"value": "vocational", "label": "Vocational school where I am learning job or life skills"},
                    {"value": "college", "label": "College/university"},
                    {"value": "graduate", "label": "Graduate school"},
                    {"value": "schoolOther", "label": "Other"},
                ],
            },
        },
    )

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["placement_group"]["fields"] = [
            "self_placement",
            "placement_other",
            "current_grade"
        ]
        return field_groups


class EducationSelfQuestionnaireSchema(ModelSchema):
    class Meta:
        model = EducationSelfQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "attends_school",
            "school_name",
            "school_type",
            "self_placement",
            "placement_other",
            "current_grade",
            "school_services",
            "school_services_other",
        )
