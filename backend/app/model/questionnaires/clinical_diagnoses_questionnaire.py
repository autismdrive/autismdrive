import datetime

from dateutil.tz import tzutc
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import func

from app import db, ma
from app.export_service import ExportService


class ClinicalDiagnosesQuestionnaire(db.Model):
    __tablename__ = "clinical_diagnoses_questionnaire"
    __label__ = "Clinical Diagnosis"
    __question_type__ = ExportService.TYPE_SENSITIVE
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("stardrive_user.id")
    )
    developmental = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 1.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "intellectual", "label": "Intellectual disability"},
                    {"value": "globalDevelopmental", "label": "Global developmental delay"},
                    {"value": "learning", "label": "Learning disability"},
                    {"value": "speechLanguage", "label": "Speech or language disorder"},
                    {"value": "coordination", "label": "Developmental coordination disorder"},
                    {"value": "deaf", "label": "Deaf/hard of hearing"},
                    {"value": "visual", "label": "Visual impairment"},
                    {"value": "fetalAlcohol", "label": "Fetal alcohol spectrum disorder"},
                    {"value": "developmentalOther", "label": "Other developmental condition"},
                    {"value": "noDisclose", "label": "I choose not to disclose"},
                ],
            },
        },
    )
    developmental_other = db.Column(
        db.String,
        info={
            "display_order": 1.2,
            "type": "input",
            "template_options": {
                "label": "Enter developmental condition",
                "appearance": "standard"
            },

            "hide_expression": '!(model.developmental && model.developmental.includes("developmentalOther"))',
        },
    )
    mental_health = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 2,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "anxiety", "label": "Anxiety Disorder"},
                    {"value": "adhd", "label": "Attention-deficit/hyperactivity disorder (ADHD)"},
                    {"value": "bipolar", "label": "Bipolar Disorder"},
                    {"value": "depression", "label": "Depression"},
                    {"value": "ocd", "label": "Obsessive compulsive disorder (OCD)"},
                    {"value": "odd", "label": "Oppositional Defiant Disorder (ODD)"},
                    {"value": "ptsd", "label": "Post-traumatic stress disorder (PTSD)"},
                    {"value": "schizophrenia", "label": "Schizophrenia or Psychotic Disorder"},
                    {"value": "tourette", "label": "Tourette Syndrome or Tic Disorder"},
                    {"value": "mentalHealthOther", "label": "Other mental health condition"},
                    {"value": "noDisclose", "label": "I choose not to disclose"},
                ],
            },
        },
    )
    mental_health_other = db.Column(
        db.String,
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {
                "label": "Enter mental health condition",
                "appearance": "standard"
            },
            "hide_expression": '!(model.mental_health && model.mental_health.includes("mentalHealthOther"))',
        },
    )
    medical = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 3.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "gastrointestinal", "label": "Chronic Gastrointestinal (GI) problems"},
                    {"value": "seizure", "label": "Epilepsy (seizure disorder)"},
                    {"value": "insomnia", "label": "Insomnia (problems falling or staying asleep)"},
                    {"value": "cerebralPalsy", "label": "Cerebral palsy"},
                    {"value": "asthma", "label": "Asthma"},
                    {"value": "earInfections", "label": "Chronic ear infections"},
                    {"value": "medicalOther", "label": "Other health problem"},
                    {"value": "noDisclose", "label": "I choose not to disclose"},
                ],
            },
        },
    )
    medical_other = db.Column(
        db.String,
        info={
            "display_order": 3.2,
            "type": "input",
            "template_options": {
                "label": "Enter medical condition",
                "appearance": "standard"
            },
            "hide_expression": '!(model.medical && model.medical.includes("medicalOther"))',
        },
    )
    genetic = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 4.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "fragileX", "label": "Fragile X syndrome"},
                    {"value": "tuberousSclerosis", "label": "Tuberous Sclerosis"},
                    {"value": "corneliaDeLange", "label": "Cornelia de Lange syndrome"},
                    {"value": "down", "label": "Down syndrome"},
                    {"value": "angelman", "label": "Angelman syndrome"},
                    {"value": "rett", "label": "Rett syndrome"},
                    {"value": "22q11.2deletion", "label": "22q11.2 Deletion syndrome"},
                    {"value": "geneticOther", "label": "Other genetic condition"},
                    {"value": "noDisclose", "label": "I choose not to disclose"},
                ],
            },
        },
    )
    genetic_other = db.Column(
        db.String,
        info={
            "display_order": 4.2,
            "type": "input",
            "template_options": {
                "label": "Enter genetic condition",
                "appearance": "standard"
            },
            "hide_expression": '!(model.genetic && model.genetic.includes("geneticOther"))',
        },
    )

    def get_field_groups(self):
        return {
                "intro": {
                    "fields": [],
                    "display_order": 0,
                    "wrappers": ["help"],
                    "template_options": {
                        "label": "",
                        "description": "",
                    },
                    "expression_properties": {
                        "template_options.label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": '"Do you CURRENTLY have any of the following diagnoses? (please check all that apply)"',
                                "self_guardian": '"Do you CURRENTLY have any of the following diagnoses? (please check all that apply)"',
                                "dependent": '"Does " + (formState.preferredName || "your child") + " CURRENTLY have any of the following diagnoses? (please check all that apply)"',
                            }
                        },
                        "template_options.description": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": '"You may choose not to disclose confidential health information, however, this may cause to you to be excluded from some studies."',
                                "self_guardian": '"You may choose not to disclose confidential health information, however, this may cause to you to be excluded from some studies."',
                                "dependent": '"You may choose not to disclose confidential health information, however, this may cause " + (formState.preferredName || "your child") + " to be excluded from some studies."',
                            }
                        },
                    }
                },
                "developmental_group": {
                    "fields": ["developmental", "developmental_other"],
                    "display_order": 1,
                    "wrappers": ["card"],
                    "template_options": {"label": "Developmental"},
                },
                "mental_health_group": {
                    "fields": ["mental_health", "mental_health_other"],
                    "display_order": 2,
                    "wrappers": ["card"],
                    "template_options": {"label": "Mental health"},
                },
                "medical_group": {
                    "fields": ["medical", "medical_other"],
                    "display_order": 3,
                    "wrappers": ["card"],
                    "template_options": {"label": "Medical"},
                },
                "genetic_group": {
                    "fields": ["genetic", "genetic_other"],
                    "display_order": 4,
                    "wrappers": ["card"],
                    "template_options": {"label": "Genetic Conditions"},
                },
            }


class ClinicalDiagnosesQuestionnaireSchema(ModelSchema):
    class Meta:
        model = ClinicalDiagnosesQuestionnaire
        ordered = True
        include_fk = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.questionnaireendpoint', name="clinical_diagnoses_questionnaire", id='<id>')
    })
