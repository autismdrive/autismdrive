from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import func

from app import db, ma
from app.export_service import ExportService
from app.model.event import Event


class RegistrationQuestionnaire(db.Model):
    __tablename__ = "registration_questionnaire"
    __label__ = "Registration"
    __question_type__ = ExportService.TYPE_IDENTIFYING
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
    event_id = db.Column(db.Integer, db.ForeignKey(Event.id), nullable=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    zip_code = db.Column(db.Integer)
    relationship_to_autism = db.Column(db.ARRAY(db.String), default=[])
    relationship_other = db.Column(db.String)
    marketing_channel = db.Column(db.ARRAY(db.String), default=[])
    marketing_other = db.Column(db.String)
    newsletter_consent = db.Column(db.Boolean)

    def get_field_groups(self):
        return {}


class RegistrationQuestionnaireSchema(ModelSchema):
    class Meta:
        model = RegistrationQuestionnaire
        ordered = True
        include_fk = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.questionnaireendpoint', name='registration_questionnaire', id='<id>'),
    })