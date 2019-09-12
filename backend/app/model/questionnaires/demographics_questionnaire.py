import datetime

from dateutil.tz import tzutc
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import func

from app import db, ma
from app.export_service import ExportService


class DemographicsQuestionnaire(db.Model):
    __tablename__ = "demographics_questionnaire"
    __label__ = "Demographics"
    __question_type__ = ExportService.TYPE_SENSITIVE
    __estimated_duration_minutes__ = 8

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("stardrive_user.id")
    )
    birth_sex = db.Column(
        db.String,
        info={
            "display_order": 1,
            "type": "radio",
            "template_options": {
                "required": True,
                "label": {
                    "RELATIONSHIP_SPECIFIC": {
                                "self_participant": "Your sex at birth",
                                "self_guardian": "Your sex at birth",
                                "self_professional": "Your sex at birth"
                            }
                },
                "options": [
                    {"value": "male", "label": "Male"},
                    {"value": "female", "label": "Female"},
                    {"value": "intersex", "label": "Intersex"},
                ],
            },
            "expression_properties": {
                "template_options.label": {
                    "RELATIONSHIP_SPECIFIC": {
                                "dependent": '(formState.preferredName || "your child") + "\'s" '
                                             '+ " sex at birth"',
                            }
                },
            },
        },
    )
    gender_identity = db.Column(
        db.String,
        info={
            "display_order": 2.1,
            "type": "select",
            "template_options": {
                "required": True,
                "options": [
                    {"value": "male", "label": "Male"},
                    {"value": "female", "label": "Female"},
                    {"value": "intersex", "label": "Intersex"},
                    {"value": "transgender", "label": "Transgender"},
                    {"value": "genderOther", "label": "Other"},
                    {"value": "no_answer", "label": "Prefer not to answer"},
                ],
                "label": "Your current gender identity:",
                "description": "(how you describe yourself)"
            },
            "expression_properties": {
                "template_options.label": {
                    "RELATIONSHIP_SPECIFIC": {
                        "dependent": '(formState.preferredName || "Your child") + "\'s current gender identity"',
                    }
                },
                "template_options.description": {
                    "RELATIONSHIP_SPECIFIC": {
                        "dependent": '"(how " + (formState.preferredName || "your child") + " describes themselves):"',
                    }
                }
            },
        },
    )
    gender_identity_other = db.Column(
        db.String,
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {
                "label": "Enter gender identity",
                "appearance": "standard"
            },
            "hide_expression": '!(model.gender_identity && (model.gender_identity === "genderOther"))',
        },
    )
    race_ethnicity = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 3.1,
            "type": "multicheckbox",
            "template_options": {
                "label": "Race/Ethnicity",
                "type": "array",
                "required": True,
                "options": [
                    {"value": "raceBlack", "label": "Black / African / African American"},
                    {"value": "raceAsian", "label": "Asian / Asian American"},
                    {"value": "raceWhite", "label": "White / Caucasian"},
                    {"value": "raceHispanic", "label": "Hispanic / Latin(o / a)"},
                    {"value": "raceNative", "label": "Native American / Alaskan Native"},
                    {"value": "racePacific", "label": "Pacific Islander"},
                    {"value": "raceNoAnswer", "label": "Prefer not to answer"},
                    {"value": "raceOther", "label": "Other"},
                ],
                "description": "(select all that apply)"
            },
            "validators": {"required": "multicheckbox"},
        },
    )
    race_ethnicity_other = db.Column(
        db.String,
        info={
            "display_order": 3.2,
            "type": "input",
            "template_options": {
                "label": "Enter race/ethnicity",
                "appearance": "standard"
            },
            "hide_expression": '!(model.race_ethnicity && model.race_ethnicity.includes("raceOther"))',
        },
    )

    def get_field_groups(self):
        return {
                "gender": {
                    "fields": ["birth_sex", "gender_identity", "gender_identity_other"],
                    "display_order": 2,
                    "wrappers": ["card"],
                    "template_options": {
                        "label": "Gender"
                    }
                },
                "race": {
                    "fields": ["race_ethnicity", "race_ethnicity_other"],
                    "display_order": 3,
                    "wrappers": ["card"],
                    "template_options": {
                        "label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": "What is your race/ethnicity?",
                                "self_guardian": "What is your race/ethnicity?",
                                "self_professional": "What is your race/ethnicity?",
                            }
                        }
                    },
                    "expression_properties": {
                        "template_options.label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "dependent": '"What is " + (formState.preferredName || "your child") + "\'s" + '
                                             '" race/ethnicity?"',
                            }
                        },
                    },
                },
            }


class DemographicsQuestionnaireSchema(ModelSchema):
    class Meta:
        model = DemographicsQuestionnaire
        ordered = True
        include_fk = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.questionnaireendpoint', name="demographics_questionnaire", id='<id>')
    })