from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.current_behaviors_mixin import CurrentBehaviorsMixin


class CurrentBehaviorsDependentQuestionnaire(db.Model, CurrentBehaviorsMixin):
    __tablename__ = "current_behaviors_dependent_questionnaire"

    has_academic_difficulties_desc = '"Does " + (formState.preferredName || "your child") + " have any difficulties with academics?"'
    academic_difficulty_areas_desc = '"What areas of academics are difficult for " + (formState.preferredName || "your child")'

    dependent_verbal_ability = db.Column(
        db.String,
        info={
            "display_order": 1,
            "type": "radio",
            "template_options": {
                "label": '',
                "required": False,
                "options": [
                    {"value": "nonVerbal", "label": "Non-verbal"},
                    {"value": "singleWords", "label": "Single Words"},
                    {"value": "phraseSpeech", "label": "Phrase Speech"},
                    {"value": "fluentErrors", "label": "Fluent Speech with grammatical errors"},
                    {"value": "fluent", "label": "Fluent Speech"},
                ]
            },
            "expression_properties": {
                "template_options.label": '(formState.preferredName || "Your child") + "\'s current '
                                          'verbal ability:"'
            },
        }
    )
    concerning_behaviors = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 2,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "label": '',
                "required": False,
                "options": [
                    {"value": "aggression", "label": "Aggression"},
                    {"value": "anxiety", "label": "Anxiety"},
                    {"value": "destruction", "label": "Destruction of property"},
                    {"value": "hoarding", "label": "Collecting or hoarding objects"},
                    {"value": "elopement", "label": "Elopement (running away or leaving supervision without an adult)"},
                    {"value": "insistRoutine", "label": "Insistence on routines"},
                    {"value": "irritability", "label": "Irritability"},
                    {"value": "pica", "label": "Pica (eating inedible objects)"},
                    {"value": "rectalDig", "label": "Rectal digging"},
                    {"value": "repetitiveWords", "label": "Repetitive words, sounds, or sentences"},
                    {"value": "restrictEating", "label": "Restricted/picky eating"},
                    {"value": "selfInjury", "label": "Self-injury"},
                    {"value": "soiling", "label": "Soiling property (through urination or fecal smearing)"},
                    {"value": "spitting", "label": "Spitting"},
                    {"value": "screaming", "label": "Screaming"},
                    {"value": "stealing", "label": "Stealing"},
                    {"value": "verbalAggression", "label": "Verbal aggression (profanity or verbal threats)"},
                    {"value": "tantrums", "label": "Tantrums"},
                    {"value": "noDisclose", "label": "I choose not to disclose"},
                    {"value": "concerningOther", "label": "Other"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"Does " + (formState.preferredName || "your child") + '
                                          '" currently engage in the following behaviors of concern?"'
            },
        },
    )
    concerning_behaviors_other = db.Column(
        db.String,
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {
                "label": "Enter concerning behavior",
                "appearance": "standard"
            },
            "hide_expression": '!(model.concerning_behaviors && model.concerning_behaviors.includes("concerningOther"))',
        },
    )

    def get_field_groups(self):
        return super().get_field_groups()


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
        ordered = True
