from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, Boolean, BigInteger, ARRAY
from sqlalchemy.ext.declarative import declared_attr

from app.export_service import ExportService


class EducationMixin(object):
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5
    school_services_other_hide_expression = (
        '!(model.school_services && model.school_services.includes("servicesOther"))'
    )

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    time_on_task_ms = Column(BigInteger, default=0)

    @declared_attr
    def participant_id(cls):
        return Column("participant_id", Integer, ForeignKey("stardrive_participant.id"))

    @declared_attr
    def user_id(cls):
        return Column("user_id", Integer, ForeignKey("stardrive_user.id"))

    @declared_attr
    def attends_school(cls):
        return Column(
            Boolean,
            info={
                "display_order": 1,
                "type": "radio",
                "template_options": {
                    "label": "Attend a school or program?",
                    "required": False,
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {
                    "template_options.label": cls.attends_school_desc,
                },
            },
        )

    school_name = Column(
        String,
        info={
            "display_order": 2,
            "type": "input",
            "template_options": {
                "label": "Name of the school or program",
                "required": False,
            },
            "hide_expression": "!(model.attends_school)",
        },
    )

    @declared_attr
    def school_type(cls):
        return Column(
            String,
            info={
                "display_order": 3,
                "type": "radio",
                "template_options": {
                    "label": "Type of School",
                    "required": False,
                    "options": [
                        {"value": "public", "label": "Public"},
                        {"value": "private", "label": "Private"},
                        {"value": "homeschool", "label": "Home School"},
                    ],
                },
                "expression_properties": {
                    "template_options.label": cls.school_type_desc,
                },
                "hide_expression": "!(model.attends_school)",
            },
        )

    @declared_attr
    def placement_other(cls):
        return Column(
            String,
            info={
                "display_order": 4.3,
                "type": "input",
                "template_options": {
                    "label": "Enter school placement",
                    "required": True,
                },
                "hide_expression": cls.placement_other_hide_expression,
                "expression_properties": {"template_options.required": "!" + cls.placement_other_hide_expression},
            },
        )

    @declared_attr
    def current_grade(cls):
        return Column(
            String,
            info={
                "display_order": 5,
                "type": "input",
                "template_options": {
                    "label": "School grade level",
                    "required": True,
                },
                "hide_expression": cls.current_grade_hide_expression,
                "expression_properties": {"template_options.required": "!" + cls.current_grade_hide_expression},
            },
        )

    @declared_attr
    def school_services(cls):
        return Column(
            ARRAY(String),
            info={
                "display_order": 6.1,
                "type": "multicheckbox",
                "template_options": {
                    "type": "array",
                    "required": False,
                    "options": [
                        {"value": "504mod", "label": "504 Modification Plan"},
                        {"value": "iep", "label": "Individualized Education Program (IEP)"},
                        {"value": "1:1aide", "label": "1:1 aide or paraprofessional in classroom"},
                        {
                            "value": "partTimeInstruction",
                            "label": "Part-time specialized instruction in a resource room or "
                            "special education classroom",
                        },
                        {
                            "value": "fullTimeInstruction",
                            "label": "Full-time specialized instruction in a resource room or "
                            "special education classroom",
                        },
                        {"value": "specializedSchool", "label": "Specialized school for special learning needs"},
                        {"value": "dayTreatment", "label": "Day treatment or residential center"},
                        {
                            "value": "disabilitySupports",
                            "label": "Disability supports services (at college/vocational " "school)",
                        },
                        {"value": "servicesNone", "label": "None of the above"},
                        {"value": "servicesOther", "label": "Other"},
                    ],
                },
                "expression_properties": {
                    "template_options.label": cls.school_services_desc,
                },
                "hide_expression": "!(model.attends_school)",
            },
        )

    school_services_other = Column(
        String,
        info={
            "display_order": 6.2,
            "type": "input",
            "template_options": {
                "label": "Describe additional services",
                "required": True,
            },
            "hide_expression": school_services_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + school_services_other_hide_expression},
        },
    )

    def get_field_groups(self):
        return {
            "placement_group": {
                "display_order": 4,
                "wrappers": ["card"],
                "template_options": {"label": "Placement"},
                "hide_expression": "!(model.attends_school)",
            },
            "school_services_group": {
                "fields": ["school_services", "school_services_other"],
                "display_order": 6,
                "wrappers": ["card"],
                "template_options": {"label": "School Services"},
                "hide_expression": "!(model.attends_school)",
            },
        }
