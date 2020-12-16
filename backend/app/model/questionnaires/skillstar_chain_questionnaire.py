from marshmallow import pre_load
from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

from app import db, ma
from app.model.questionnaires.chain_session import ChainSessionSchema, ChainSession
from app.model.questionnaires.chain_mixin import ChainMixin
from app.schema.model_schema import ModelSchema


class SkillstarChainQuestionnaire(db.Model, ChainMixin):
    __tablename__ = "skillstar_chain_questionnaire"
    __label__ = "SkillSTAR Chain Questionnaire"

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    @declared_attr
    def participant_id(cls):
        return db.Column("participant_id", db.Integer, db.ForeignKey("stardrive_participant.id"))

    @declared_attr
    def user_id(cls):
        return db.Column("user_id", db.Integer, db.ForeignKey("stardrive_user.id"))

    @declared_attr
    def sessions(cls):
        return db.relationship(
            "ChainSession",
            backref=db.backref(cls.__tablename__, lazy=True),
            cascade="all, delete-orphan",
            passive_deletes=True
        )

    def get_field_groups(self):
        field_groups = {
                "sessions": {
                    "type": "repeat",
                    "display_order": 3,
                    "wrappers": ["card"],
                    "repeat_class": ChainSession,
                    "template_options": {
                        "label": "Chain Session",
                        "description": "Add a session",
                    },
                    "expression_properties": {},
                },
            }
        return field_groups


class SkillstarChainQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields['sessions'].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = SkillstarChainQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "sessions",
        )
    sessions = ma.Nested(ChainSessionSchema, many=True)
