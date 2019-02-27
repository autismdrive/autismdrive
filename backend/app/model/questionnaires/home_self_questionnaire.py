from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.housemate import Housemate
from app.model.questionnaires.home_mixin import HomeMixin


class HomeSelfQuestionnaire(db.Model, HomeMixin):
    __tablename__ = "home_self_questionnaire"

    self_living_situation = db.Column(
        db.String,
        info={
            "display_order": 1.1,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "required": True,
                "label": "Where do you currently live? (select all that apply)",
                "options": [
                    {"value": "alone", "label": "On my own"},
                    {"value": "spouse", "label": "With a spouse or significant other"},
                    {"value": "family", "label": "With my family"},
                    {"value": "roommates", "label": "With roommates"},
                    {"value": "caregiver", "label": "With a paid caregiver"},
                    {"value": "livingOther", "label": "Other"},
                ],
            },
        },
    )
    self_living_other = db.Column(
        db.String,
        info={
            "display_order": 1.2,
            "type": "input",
            "template_options": {
                "placeholder": "Describe your current living situation"
            },
            "hide_expression": '!(model.self_living_situation && model.self_living_situation.livingOther)',
        },
    )

    def get_meta(self):
        info = {}

        info.update(HomeMixin.info)

        info["field_groups"]["self_living"] = {
                    "fields": ["self_living_situation", "self_living_other"],
                    "display_order": 1,
                    "wrappers": ["card"],
                    "template_options": {"label": "Current Living Situation"},
                }

        info["field_groups"]["housemates"]["template_options"]["label"] = "Who else lives with you?"

        for c in self.metadata.tables["home_self_questionnaire"].columns:
            if c.info:
                info[c.name] = c.info

        info["struggle_to_afford"]["template_options"]["label"] = \
            "Do you ever struggle with being able to afford to pay for household needs, food, or security?"

        info["housemates"] = Housemate().get_meta()

        return info


class HomeSelfQuestionnaireSchema(ModelSchema):
    class Meta:
        model = HomeSelfQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "self_living_situation",
            "self_living_other",
            "housemates",
            "struggle_to_afford",
        )


class HomeSelfQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = HomeSelfQuestionnaire
        fields = ("get_meta",)
