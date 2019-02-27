from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.current_behaviors_mixin import CurrentBehaviorsMixin


class CurrentBehaviorsSelfQuestionnaire(db.Model, CurrentBehaviorsMixin):
    __tablename__ = "current_behaviors_self_questionnaire"

    self_verbal_ability = db.Column(
        db.String,
        info={
            "display_order": 1,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "label": "How do you best communicate?",
                "required": False,
                "options": [
                    {"value": "verbal", "label": "Verbally"},
                    {"value": "nonVerbal", "label": "Non-verbally"},
                    {
                        "value": "AACsystem",
                        "label": "An alternative and augmentative communication (AAC) system "
                        "(e.g., Picture exchange, sign language, ipad, etc)",
                    },
                ],
            },
        },
    )

    def get_meta(self):
        info = {}

        info.update(CurrentBehaviorsMixin.info)

        for c in self.metadata.tables["current_behaviors_self_questionnaire"].columns:
            if c.info:
                info[c.name] = c.info

        info["has_academic_difficulties"]["template_options"]["label"] = "Do you have any difficulties with academics?"
        info["academic_difficulty_areas"]["template_options"]["label"] = "What areas of academics are difficult for you?"

        return info


class CurrentBehaviorsSelfQuestionnaireSchema(ModelSchema):
    class Meta:
        model = CurrentBehaviorsSelfQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "self_verbal_ability",
            "has_academic_difficulties",
            "academic_difficulty_areas",
            "academic_difficulty_other",
        )
