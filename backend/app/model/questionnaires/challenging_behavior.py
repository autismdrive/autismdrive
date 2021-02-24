from sqlalchemy import func

from app import db
from app.schema.model_schema import ModelSchema


class ChallengingBehavior(db.Model):
    __tablename__ = "challenging_behavior"
    __label__ = "ChallengingBehavior"
    __no_export__ = True  # This will be transferred as a part of a parent class

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    chain_session_step_id = db.Column(
        "chain_session_step_id",
        db.Integer,
        db.ForeignKey("chain_session_step.id")
    )
    time = db.Column(
        db.DateTime,
        info={
            "display_order": 1,
            "type": "datepicker",
            "template_options": {
                "label": "Time challenging behavior occurred",
            },
        }
    )

    def get_field_groups(self):
        info = {
        }
        return info


class ChallengingBehaviorSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ChallengingBehavior
        fields = ("id", "last_updated", "chain_session_step_id", "time")
