from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import func

from app import db, ma
from app.export_service import ExportService


class EmploymentQuestionnaire(db.Model):
    __tablename__ = 'employment_questionnaire'
    __label__ = "Employment"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 2

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column(
        'participant_id',
        db.Integer,
        db.ForeignKey('stardrive_participant.id')
    )
    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('stardrive_user.id')
    )
    is_currently_employed = db.Column(
        db.Boolean,
        info={
            'display_order': 1.1,
            'type': 'radio',
            'template_options': {
                'label': 'Are you currently employed?',
                'required': False,
                'options': [
                    {'value': True, 'label': 'Yes'},
                    {'value': False, 'label': 'No'}
                ]
            }
        }
    )
    employment_capacity = db.Column(
        db.String,
        info={
            'display_order': 1.2,
            'type': 'radio',
            'default_value': 'n/a',
            'template_options': {
                'label': 'In what capacity?',
                'required': False,
                'options': [
                    {'value': 'fullTime', 'label': 'Full time (> 35 hours per week)'},
                    {'value': 'partTime', 'label': 'Part time'}
                ]
            },
            'hide_expression': '!(model.is_currently_employed)',
        }
    )
    has_employment_support = db.Column(
        db.String,
        info={
            'display_order': 2,
            'type': 'radio',
            'template_options': {
                'label': 'Receiving Support?',
                'description': 'Do you currently receive supports to help you work successfully, such as job coaching '
                         'or vocational training?',
                'required': False,
                'options': [
                    {'value': 'yes', 'label': 'Yes'},
                    {'value': 'interested', 'label': 'No, but I am interested'},
                    {'value': 'no', 'label': 'No'}
                ]
            }
        }
    )

    def get_field_groups(self):
        return {}


class EmploymentQuestionnaireSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmploymentQuestionnaire
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        ordered = True
        include_fk = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.questionnaireendpoint', name='employment_questionnaire', id='<id>'),
    })
