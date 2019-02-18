import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.question_service import QuestionService


class EducationDependentQuestionnaire(db.Model):
    __tablename__ = "education_dependent_questionnaire"
    __question_type__ = QuestionService.TYPE_IDENTIFYING
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("stardrive_user.id")
    )
    attends_school = db.Column(
        db.Boolean,
        info={
            "display_order": 1,
            "type": "radio",
            "default_value": True,
            "template_options": {
                "label": '"Does " + (formState.mainModel.preferred_name || "your child") + " attend school?")',
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    school_name = db.Column(
        db.String,
        info={
            "display_order": 2,
            "type": "input",
            "template_options": {
                "label": "What is the name of the school or program?",
                "required": False,
            },
        },
    )
    school_type = db.Column(
        db.String,
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "label": '"Is " + (formState.mainModel.preferred_name || "your child") + "\'s school:")',
                "required": False,
                "options":[
                    {"value": "public", "label": "Public"},
                    {"value": "private", "label": "Private"},
                    {"value": "homeschool", "label": "Home School"},
                ]
            },
        },
    )
    dependent_placement = db.Column(
        db.String,
        info={
            "display_order": 4.2,
            "type": "select",
            "template_options": {
                "label": '"What is " + (formState.mainModel.preferred_name || "your child") + "\'s current grade/school placement?"',
                "required": False,
                "options": [
                    {"value": "daycare", "label": "Daycare center"},
                    {"value": "preschool", "label": "Preschool"},
                    {"value": "kindergarten", "label": "Kindergarten"},
                    {
                        "value": "grades1to12",
                        "label": "1st through 12th grade, please specify CURRENT GRADE below",
                    },
                    {
                        "value": "vocational",
                        "label": "Vocational school where I am learning job or life skills",
                    },
                    {"value": "college", "label": "College/university"},
                    {"value": "graduate", "label": "Graduate school"},
                    {"value": "schoolOther", "label": "Other"},
                ],
            },
        },
    )
    placement_other = db.Column(
        db.String,
        info={
            "display_order": 4.3,
            "type": "input",
            "template_options": {"placeholder": "Enter school placement"},
            "hide_expression": '!(model.dependent_placement && model.dependent_placement.schoolOther)',
        },
    )
    current_grade = db.Column(
        db.String,
        info={
            "display_order": 5,
            "type": "input",
            "template_options": {"placeholder": "Enter grade"},
            "hide_expression": '!(model.dependent_placement && model.dependent_placement.grades1to12)',
        },
    )
    school_services = db.Column(
        db.String,
        info={
            "display_order": 6.1,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "label": '"Please check the following services " + (formState.mainModel.preferred_name || "your child") + " currently receives in school (check all that apply):"',
                "required": False,
                "options": [
                    {"value": "504mod", "label": "504 Modification Plan"},
                    {
                        "value": "iep",
                        "label": "Individualized Education Program (IEP)",
                    },
                    {
                        "value": "1:1aide",
                        "label": "1:1 aide or paraprofessional in classroom",
                    },
                    {
                        "value": "partTimeInstruction",
                        "label": "Part-time specialized instruction in a resource room or special education classroom",
                    },
                    {
                        "value": "fullTimeInstruction",
                        "label": "Full-time specialized instruction in a resource room or special education classroom",
                    },
                    {
                        "value": "specializedSchool",
                        "label": "Specialized school for special learning needs",
                    },
                    {
                        "value": "dayTreatment",
                        "label": "Day treatment or residential center",
                    },
                    {
                        "value": "disabilitySupports",
                        "label": "Disability supports services (at college/vocational school)",
                    },
                    {"value": "servicesOther", "label": "Other"},
                ],
            },
        },
    )
    school_services_other = db.Column(
        db.String,
        info={
            "display_order": 6.2,
            "type": "input",
            "template_options": {"placeholder": "Enter service"},
            "hide_expression": '!(model.school_services && (model.schoolServices.servicesOther))',
        },
    )

    def get_meta(self):
        info = {
            "table": {
                "sensitive": False,
                "label": "Education",
                "description": "",
            },
            "field_groups": {
                "placement_group": {
                    "fields": [
                        "dependent_placement",
                        "placement_other",
                    ],
                    "display_order": 4,
                    "wrappers": ["card"],
                    "template_options": {"label": "Placement"},
                },
                "school_services_group": {
                    "fields": ["school_services", "school_services_other"],
                    "display_order": 6,
                    "wrappers": ["card"],
                    "template_options": {"label": "School Services"},
                },
            },
        }
        for c in self.metadata.tables["education_dependent_questionnaire"].columns:
            if c.info:
                info[c.name] = c.info
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
