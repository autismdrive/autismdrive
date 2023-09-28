from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, Boolean, BigInteger, ARRAY
from sqlalchemy.ext.declarative import declared_attr

from app.export_service import ExportService


class EvaluationHistoryMixin(object):
    __question_type__ = ExportService.TYPE_SENSITIVE
    __estimated_duration_minutes__ = 5
    who_diagnosed_other_hide_expression = '!(model.who_diagnosed && (model.who_diagnosed === "diagnosisOther"))'
    where_diagnosed_other_hide_expression = '!(model.where_diagnosed && (model.where_diagnosed === "diagnosisOther"))'

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
    def has_autism_diagnosis(cls):
        return Column(
            Boolean,
            info={
                "display_order": 1,
                "type": "radio",
                "template_options": {
                    "required": True,
                    "label": "Formal Diagnosis?",
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {"template_options.description": cls.has_autism_diagnosis_label},
            },
        )

    @declared_attr
    def self_identifies_autistic(cls):
        return Column(
            Boolean,
            info={
                "display_order": 2,
                "type": "radio",
                "template_options": {
                    "required": False,
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {"template_options.label": cls.self_identifies_autistic_label},
            },
        )

    @declared_attr
    def years_old_at_first_diagnosis(cls):
        return Column(
            Integer,
            info={
                "display_order": 3,
                "type": "input",
                "template_options": {
                    "label": "Age at Diagnosis",
                    "type": "number",
                    "max": 130,
                },
                "expression_properties": {
                    "template_options.description": cls.years_old_at_first_diagnosis_label,
                    "template_options.required": "model.has_autism_diagnosis",
                },
                "hide_expression": "!(model.has_autism_diagnosis)",
                "validation": {
                    "messages": {
                        "max": "Please enter age in years",
                    }
                },
            },
        )

    @declared_attr
    def who_diagnosed(cls):
        return Column(
            String,
            info={
                "display_order": 4,
                "type": "select",
                "template_options": {
                    "label": "First Diagnosed by:",
                    "placeholder": "Please select from these options",
                    "options": [
                        {
                            "value": "pediatrician",
                            "label": "Pediatrician/Developmental pediatrician/Primary care physician",
                        },
                        {"value": "psychiatrist", "label": "Psychiatrist"},
                        {"value": "neurologist", "label": "Neurologist"},
                        {"value": "psychologist", "label": "Psychologist"},
                        {
                            "value": "healthTeam",
                            "label": "Team of healthcare professionals",
                        },
                        {"value": "diagnosisOther", "label": "Other"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": cls.who_diagnosed_label,
                    "template_options.required": "model.has_autism_diagnosis",
                },
                "hide_expression": "!(model.has_autism_diagnosis)",
            },
        )

    who_diagnosed_other = Column(
        String,
        info={
            "display_order": 5,
            "type": "input",
            "template_options": {
                "label": "Diagnosed by other?",
                "placeholder": "Please Describe",
                "required": True,
            },
            "hide_expression": who_diagnosed_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + who_diagnosed_other_hide_expression},
        },
    )

    @declared_attr
    def where_diagnosed(cls):
        return Column(
            String,
            info={
                "display_order": 6,
                "type": "radio",
                "className": "vertical-radio-group",
                "template_options": {
                    "label": "Diagnosed At",
                    "placeholder": "Please select from these options",
                    "options": [
                        {
                            "value": "1uvaDp",
                            "label": "UVA Developmental Pediatrics or UVA Child Development and Rehabilitation Center (formerly Kluge Children's Rehabilitation Center, KCRC)",
                        },
                        {"value": "2sjcCse", "label": "Sheila Johnson Center or Curry School of Education"},
                        {"value": "3via", "label": "Virginia Institute of Autism (VIA)"},
                        {"value": "4school", "label": "School system"},
                        {"value": "5evms", "label": "Eastern Virginia Medical School (EVMS)"},
                        {"value": "6chkd", "label": "Children’s Hospital of the Kings Daughters (CHKD)"},
                        {"value": "7cas", "label": "Commonwealth Autism Services (Virginia Commonwealth University)"},
                        {"value": "8vtAc", "label": "Virginia Tech Autism Clinic"},
                        {"value": "9gmu", "label": "George Mason University"},
                        {"value": "10brAac", "label": "Blue Ridge Autism and Achievement Center"},
                        {"value": "11cnh", "label": "Children’s National Hospital"},
                        {
                            "value": "12kki",
                            "label": "Center for Autism and Related Disorders (Kennedy Krieger Institute)",
                        },
                        {"value": "13vcu", "label": "Children’s Hospital of Richmond (VCU)"},
                        {"value": "14vtc", "label": "Virginia Tech Carilion"},
                        {"value": "15centra", "label": "CENTRA Lynchburg"},
                        {"value": "16apg", "label": "Alexandria Pediatrician Group"},
                        {"value": "17cc", "label": "Carilion Clinic"},
                        {"value": "18mwh", "label": "Mary Washington Hospital"},
                        {"value": "19rna", "label": "Roanoke Neurological Associates"},
                        {"value": "20ruac", "label": "Radford University Autism Center"},
                        {"value": "21rcim", "label": "Rimland Center for Integrative Medicine"},
                        {"value": "22occa", "label": "One Child Center for Autism (Williamsburg)"},
                        {"value": "23inova", "label": "INOVA Health System"},
                        {"value": "24sentara", "label": "Sentara Health System"},
                        {"value": "25psv", "label": "Pediatric Specialists of Virginia"},
                        {"value": "diagnosisOther", "label": "Other"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": cls.where_diagnosed_label,
                    "template_options.required": "model.has_autism_diagnosis",
                },
                "hide_expression": "!(model.has_autism_diagnosis)",
            },
        )

    where_diagnosed_other = Column(
        String,
        info={
            "display_order": 7,
            "type": "input",
            "template_options": {
                "label": "Where was this diagnosis made?",
                "required": True,
            },
            "hide_expression": where_diagnosed_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + where_diagnosed_other_hide_expression},
        },
    )

    partner_centers_evaluation = Column(
        ARRAY(String),
        info={
            "display_order": 8.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {
                        "value": "uva",
                        "label": "UVA Developmental Pediatrics or UVA Child Development and Rehabilitation"
                        " Center (formerly Kluge Children's Rehabilitation Center, KCRC)",
                    },
                    {"value": "sjc", "label": "Sheila Johnson Center or Curry School of Education"},
                    {"value": "via", "label": "Virginia Institute of Autism (VIA)"},
                    {"value": "fc", "label": "Faison Center"},
                    {"value": "inova", "label": "INOVA Health System"},
                    {"value": "none", "label": "None of the above"},
                ],
            },
        },
    )

    @declared_attr
    def gives_permission_to_link_evaluation_data(cls):
        return Column(
            Boolean,
            info={
                "display_order": 9,
                "type": "radio",
                "template_options": {
                    "label": "Permission to Link Data",
                    "required": False,
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": cls.gives_permission_to_link_evaluation_data_desc,
                },
                "hide_expression": '!(model.partner_centers_evaluation && (model.partner_centers_evaluation.length > 0) && !model.partner_centers_evaluation.includes("none"))',
            },
        )

    @declared_attr
    def has_iq_test(cls):
        return Column(
            Boolean,
            info={
                "display_order": 10,
                "type": "radio",
                "template_options": {
                    "required": False,
                    "label": "Taken an IQ Test?",
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": cls.has_iq_test_desc,
                },
            },
        )

    @declared_attr
    def recent_iq_score(cls):
        return Column(
            Integer,
            info={
                "display_order": 11,
                "type": "input",
                "template_options": {
                    "label": "IQ Score",
                    "placeholder": "Please enter the number of the most recent score, if known. Otherwise, leave this field blank.",
                    "type": "number",
                    "max": 200,
                    "min": 0,
                },
                "hide_expression": "!(model.has_iq_test)",
            },
        )

    def get_field_groups(self):
        return {
            "partner_centers": {
                "fields": ["partner_centers_evaluation", "gives_permission_to_link_evaluation_data"],
                "display_order": 8,
                "wrappers": ["card"],
                "template_options": {"label": ""},
                "expression_properties": {},
            }
        }
