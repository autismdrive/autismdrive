import datetime

from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.question_service import QuestionService


class EvaluationHistoryMixin(object):
    __question_type__ = QuestionService.TYPE_SENSITIVE
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    @declared_attr
    def participant_id(cls):
        return db.Column("participant_id", db.Integer, db.ForeignKey("stardrive_participant.id"))

    @declared_attr
    def user_id(cls):
        return db.Column("user_id", db.Integer, db.ForeignKey("stardrive_user.id"))

    self_identifies_autistic = db.Column(
        db.Boolean,
        info={
            "display_order": 1,
            "type": "radio",
            "default_value": True,
            "template_options": {
                "label": '',
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
            "expression_properties": {},
        },
    )
    has_autism_diagnosis = db.Column(
        db.Boolean,
        info={
            "display_order": 2,
            "type": "radio",
            "default_value": True,
            "template_options": {
                "label": '',
                "required": True,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
            "expression_properties": {},
        },
    )
    years_old_at_first_diagnosis = db.Column(
        db.Integer,
        info={
            "display_order": 3,
            "type": "input",
            "template_options": {
                "label": '',
                "required": True,
            },
            "expression_properties": {},
        },
    )
    who_diagnosed = db.Column(
        db.String,
        info={
            "display_order": 4,
            "type": "select",
            "template_options": {
                "label": '',
                "required": True,
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
            "expression_properties": {},
        },
    )
    who_diagnosed_other = db.Column(
        db.String,
        info={
            "display_order": 5,
            "type": "input",
            "template_options": {"placeholder": "First diagnosed by"},
            "hide_expression": '!(model.who_diagnosed && (model.who_diagnosed === "diagnosisOther"))',
        },
    )
    where_diagnosed = db.Column(
        db.String,
        info={
            "display_order": 6,
            "type": "select",
            "template_options": {
                "label": '',
                "required": True,
                "options": [
                    {"value": "1uvaDp", "label": "UVA Developmental Pediatrics or UVA Child Development and Rehabilitation Center (formerly Kluge Children's Rehabilitation Center, KCRC)"},
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
                    {"value": "12kki", "label": "Center for Autism and Related Disorders (Kennedy Krieger Institute)"},
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
            "expression_properties": {},
        },
    )
    where_diagnosed_other = db.Column(
        db.String,
        info={
            "display_order": 7,
            "type": "input",
            "template_options": {"placeholder": "Where diagnosed?"},
            "hide_expression": '!(model.where_diagnosed && (model.where_diagnosed === "diagnosisOther"))',
        },
    )
    partner_centers_evaluation = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 8.1,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "uva", "label": "UVA Developmental Pediatrics or UVA Child Development and Rehabilitation"
                                              " Center (formerly Kluge Children's Rehabilitation Center, KCRC)"},
                    {"value": "sjc", "label": "Sheila Johnson Center or Curry School of Education"},
                    {"value": "via", "label": "Virginia Institute of Autism (VIA)"},
                    {"value": "fc", "label": "Faison Center"},
                    {"value": "inova", "label": "INOVA Health System"},
                ],
            },
        },
    )
    gives_permission_to_link_evaluation_data = db.Column(
        db.Boolean,
        info={
            "display_order": 9,
            "type": "radio",
            "default_value": True,
            "template_options": {
                "label": "Permission to link?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
            "expression_properties": {},
            "hide_expression": "!(model.partner_centers_evaluation && (model.partner_centers_evaluation.uva "
                               "|| model.partner_centers_evaluation.sjc || model.partner_centers_evaluation.via "
                               "|| model.partner_centers_evaluation.fc || model.partner_centers_evaluation.inova))",
        },
    )
    has_iq_test = db.Column(
        db.Boolean,
        info={
            "display_order": 10,
            "type": "radio",
            "default_value": True,
            "template_options": {
                "label": "IQ or intelligence test?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
            "expression_properties": {},
        },
    )
    recent_iq_score = db.Column(
        db.Integer,
        info={
            "display_order": 11,
            "type": "input",
            "template_options": {"placeholder": "IQ score"},
            "expression_properties": {},
            "hide_expression": "!(model.has_iq_test)",
        },
    )

    def get_field_groups(self):
        return {
            "partner_centers": {
                "fields": ["partner_centers_evaluation", "gives_permission_to_link_evaluation_data"],
                "display_order": 8,
                "wrappers": ["card"],
                "template_options": {
                    "label": ''
                },
                "expression_properties": {},
            }
        }
