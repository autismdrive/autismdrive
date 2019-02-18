import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.question_service import QuestionService


class CurrentBehaviorsDependentQuestionnaire(db.Model):
    __tablename__ = "current_behaviors_dependent_questionnaire"
    __question_type__ = QuestionService.TYPE_UNRESTRICTED
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
    dependent_verbal_ability = db.Column(
        db.String,
        info={
            "display_order": 1,
            "type": "radio",
            "template_options": {
                "label": '(formState.mainModel.preferred_name || "Your child") + "\'s current verbal ability:"',
                "required": False,
                "options": [
                    {"value": "nonVerbal", "label": "Non-verbal"},
                    {"value": "singleWords", "label": "Single Words"},
                    {"value": "phraseSpeech", "label": "Phrase Speech"},
                    {"value": "fluentErrors", "label": "Fluent Speech with grammatical errors"},
                    {"value": "fluent", "label": "Fluent Speech"},
                ]
            }
        }
    )
    concerning_behaviors = db.Column(
        db.String,
        info={
            "display_order": 2,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "label": '"Does " + (formState.mainModel.preferred_name || "your child") + "currently engage in the '
                'following behaviors of concern?"',
                "required": False,
                "options": [
                    {"value": "aggression", "label": "Aggression"},
                    {"value": "anxiety", "label": "Anxiety"},
                    {
                        "value": "destruction",
                        "label": "Destruction of property",
                    },
                    {
                        "value": "hoarding",
                        "label": "Collecting or hoarding objects",
                    },
                    {
                        "value": "elopement",
                        "label": "Elopement (running away or leaving supervision without an adult)",
                    },
                    {
                        "value": "insistRoutine",
                        "label": "Insistence on routines",
                    },
                    {"value": "irritability", "label": "Irritability"},
                    {
                        "value": "pica",
                        "label": "Pica (eating inedible objects)",
                    },
                    {"value": "rectalDig", "label": "Rectal digging"},
                    {
                        "value": "repetitiveWords",
                        "label": "Repetitive words, sounds, or sentences",
                    },
                    {
                        "value": "restrictEating",
                        "label": "Restricted/picky eating",
                    },
                    {"value": "selfInjury", "label": "Self-injury"},
                    {
                        "value": "soiling",
                        "label": "Soiling property (through urination or fecal smearing)",
                    },
                    {"value": "spitting", "label": "Spitting"},
                    {"value": "screaming", "label": "Screaming"},
                    {"value": "stealing", "label": "Stealing"},
                    {
                        "value": "verbalAggression",
                        "label": "Verbal aggression (profanity or verbal threats)",
                    },
                    {"value": "tantrums", "label": "Tantrums"},
                    {"value": "concerningOther", "label": "Other"},
                ],
            },
        },
    )
    concerning_behaviors_other = db.Column(
        db.String,
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {"placeholder": "Enter concerning behavior"},
            "hide_expression": "!(model.concerning_behaviors && (model.concerning_behaviors.concerningOther))",
        },
    )
    has_academic_difficulties = db.Column(
        db.Boolean,
        info={
            "display_order": 3,
            "type": "radio",
            "default_value": True,
            "template_options": {
                "label": '"Does " + (formState.mainModel.preferred_name || "your child")) + '
                         '"have any difficulties with academics?"',
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    academic_difficulty_areas = db.Column(
        db.String,
        info={
            "display_order": 4,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "label": '"What areas of academics are difficult for " + (formState.mainModel.preferred_name || '
                         '"your child"))',
                "required": True,
                "options": [
                    {"value": "math", "label": "Math"},
                    {"value": "reading", "label": "Reading"},
                    {"value": "writing", "label": "Writing"},
                    {"value": "other", "label": "Other"},
                ],
            },
        },
    )
    academic_difficulty_other = db.Column(
        db.String,
        info={
            "display_order": 4.2,
            "type": "input",
            "template_options": {
                "placeholder": "Enter area of academic difficulty"
            },
            "hide_expression": "!(model.academic_difficulty_areas && (model.academic_difficulty_areas.other))",
        },
    )

    def get_meta(self):
        info = {
            "table": {
                "sensitive": False,
                "label": "Current Behaviors",
                "description": "",
            }
        }
        for c in self.metadata.tables[
            "current_behaviors_dependent_questionnaire"
        ].columns:
            if c.info:
                info[c.name] = c.info
        return info


class CurrentBehaviorsDependentQuestionnaireSchema(ModelSchema):
    class Meta:
        model = CurrentBehaviorsDependentQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "dependent_verbal_ability",
            "concerning_behaviors",
            "concerning_behaviors_other",
            "has_academic_difficulties",
            "academic_difficulty_areas",
            "academic_difficulty_other",
        )


class CurrentBehaviorsDependentQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = CurrentBehaviorsDependentQuestionnaire
        fields = ("get_meta",)