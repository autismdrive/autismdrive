from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.education_mixin import EducationMixin


class EducationSelfQuestionnaire(db.Model, EducationMixin):
    __tablename__ = "education_self_questionnaire"

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

    def get_meta(self):
        info = {}

        info.update(EducationMixin.info)

        info["field_groups"]["placement_group"]["fields"] = [
            "self_placement",
            "placement_other",
        ]

        for c in self.metadata.tables["education_self_questionnaire"].columns:
            if c.info:
                info[c.name] = c.info

        info["attends_school"]["template_options"]["label"] = "Do you attend an academic program, such as a school, " \
                                                              "college, or university?"
        info["school_type"]["template_options"]["label"] = "Is this a public school, private school, or are you home " \
                                                           "schooled?"
        info["school_services"]["template_options"]["label"] = "Please check the following services you currently " \
                                                               "receive through your academic program (check all " \
                                                               "that apply):"
        info["placement_other"]["hide_expression"] = \
            '!(model.self_placement && model.dependent_placement.schoolOther)'
        info["current_grade"]["hide_expression"] = \
            '!(model.self_placement && model.dependent_placement.highSchool)'

        return info


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


class EducationSelfQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = EducationSelfQuestionnaire
        fields = ("get_meta",)
