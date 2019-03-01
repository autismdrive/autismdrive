import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.question_service import QuestionService


class DemographicsQuestionnaire(db.Model):
    __tablename__ = "demographics_questionnaire"
    __label__ = "Demographics"
    __question_type__ = QuestionService.TYPE_IDENTIFYING
    __estimated_duration_minutes__ = 8

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
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
                                "self_guardian": "Your sex at birth"
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
                                "dependent": '(model.preferred_name || "your child") + "\'s" '
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
            },
        },
    )
    gender_identity_other = db.Column(
        db.String,
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {"placeholder": "Enter gender identity"},
            "hide_expression": '!(model.gender_identity && (model.gender_identity === "genderOther"))',
        },
    )
    race_ethnicity = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 3.1,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
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
            },
        },
    )
    race_ethnicity_other = db.Column(
        db.String,
        info={
            "display_order": 3.2,
            "type": "input",
            "template_options": {"placeholder": "Enter race/ethnicity"},
            "hide_expression": "!(model.race_ethnicity && (model.race_ethnicity.raceOther))",
        },
    )

    def get_field_groups(self):
        return {
                "intro": {
                    "fields": [],
                    "display_order": 0,
                    "wrappers": ["help"],
                    "template_options": {
                        "description": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": "Please answer the following questions about yourself "
                                                    "(* indicates required response):",
                                "self_guardian": "Please answer the following questions about yourself "
                                                 "(* indicates required response):",
                                "dependent": "Please answer the following questions about your child or the person "
                                             "with autism on whom you are providing information",
                            }
                        },
                    },
                },
                "gender": {
                    "fields": ["gender_identity", "gender_identity_other"],
                    "display_order": 2,
                    "wrappers": ["card"],
                    "template_options": {
                        "label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": 'Your current gender identity (how you describe yourself)*:',
                                "self_guardian": 'Your current gender identity (how you describe yourself)*:',
                            }
                        }
                    },
                    "expression_properties": {
                        "template_options.label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "dependent": '(model.preferred_name || "Your child") + "\'s" + " current gender identity '
                                             '(how " + (model.preferred_name || "your child") + " describes themselves)*:"',
                            }
                        }
                    },
                },
                "race": {
                    "fields": ["race_ethnicity", "race_ethnicity_other"],
                    "display_order": 3,
                    "wrappers": ["card"],
                    "template_options": {
                        "label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": "What is your race/ethnicity? (select all that apply)",
                                "self_guardian": "What is your race/ethnicity? (select all that apply)",
                            }
                        }
                    },
                    "expression_properties": {
                        "template_options.label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "dependent": '"What is " + (model.preferred_name || "your child") + "\'s" + '
                                             '" race/ethnicity? (select all that apply)"',
                            }
                        },
                    },
                },
            }


class DemographicsQuestionnaireSchema(ModelSchema):
    class Meta:
        model = DemographicsQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "birth_sex",
            "gender_identity",
            "gender_identity_other",
            "race_ethnicity",
            "race_ethnicity_other",
        )
