import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class Therapy(db.Model):
    __tablename__ = 'therapy'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    supports_questionnaire_id = db.Column(
        'supports_questionnaire_id',
        db.Integer,
        db.ForeignKey('supports_questionnaire.id')
    )
    type = db.Column(
        db.String,
        info={
            'display_order': 1,
            'type': 'select',
            'template_options': {
                'required': False,
                'options': [
                    {'value': 'speechLanguage', 'label': 'Speech/Language Therapy'},
                    {'value': 'occupational', 'label': 'Occupational Therapy'},
                    {'value': 'physical', 'label': 'Physical Therapy'},
                    {'value': 'behavioral', 'label': 'Behavioral Therapy (ABA, Lovaas, Discrete Trial Training, Pivotal'
                                                     ' response training, early start Denver model, etc.)'},
                    {'value': 'developmental', 'label': 'Developmental or relationship-based Therapy (DIR/Floortime)'},
                    {'value': 'family', 'label': 'Family Therapy and/or counseling'},
                    {'value': 'behavioralParent', 'label': 'Behavioral parent training (non ASD specific)'},
                    {'value': 'individual', 'label': 'Individual counseling or therapy'},
                    {'value': 'medication', 'label': 'Medication management/Psychiatry'},
                    {'value': 'socialSkills', 'label': 'Social skills training'},
                    {'value': 'parentEducation', 'label': 'Parent education workshops'},
                    {'value': 'alternativeTreatments', 'label': 'Complementary or alternative treatments (e.g., '
                                                          'vitamin/nutrient supplements, special diet, food restrictions)'},
                    {'value': 'other', 'label': 'Others (please specify)'}
                ]
            }
        }
    )
    type_other = db.Column(
        db.String,
        info={
            'display_order': 1.2,
            'type': 'textarea',
            'template_options': {
                'placeholder': 'Enter therapy or service',
                'required': False,
            },
            'hide_expression': '!(model.type && (model.type === "other"))',
        }
    )
    description = db.Column(
        db.String,
        info={
            'display_order': 2,
            'type': 'textarea',
            'template_options': {
                'label': 'Description',
                'required': False,
            },
        }
    )
    timeframe = db.Column(
        db.String,
        info={
            'display_order': 3,
            'type': 'radio',
            'default_value': True,
            'template_options': {
                'label': '',
                'required': False,
                'options': [
                    {'value': 'current', 'label': 'Currently receiving'},
                    {'value': 'past', 'label': 'Received in the past'},
                    {'value': 'futureInterest', 'label': 'Interested in receiving'}
                ]
            }
        }
    )
    notes = db.Column(
        db.String,
        info={
            'display_order': 4,
            'type': 'textarea',
            'template_options': {
                'label': 'Notes on use and/or issues with therapy or service',
                'required': False,
            },
        }
    )

    def get_meta(self):
        info = {
            'table': {
                'sensitive': False,
                'label': 'Therapy or Service'
            },
            'field_groups': {
                'type': {
                    'fields': [
                        'type',
                        'type_other'
                    ],
                    'display_order': 1,
                    'wrappers': ['card'],
                    'template_options': {
                        'label': 'Type of therapy or service'
                    }
                }
            }
        }
        for c in self.metadata.tables['therapy'].columns:
            if c.info:
                info[c.name] = c.info
        return info


class TherapySchema(ModelSchema):
    class Meta:
        model = Therapy
        fields = ('id', 'last_updated', 'supports_questionnaire_id', 'type', 'type_other', 'description', 'timeframe', 'notes')


class TherapyMetaSchema(ModelSchema):
    class Meta:
        model = Therapy
        fields = ('get_meta',)
