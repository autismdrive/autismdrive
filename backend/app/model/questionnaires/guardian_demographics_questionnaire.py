import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class GuardianDemographicsQuestionnaire(db.Model):
    __tablename__ = 'guardian_demographics_questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    guardian_id = db.Column(
        'guardian_id',
        db.Integer,
        db.ForeignKey('stardrive_user.id')
    )

    birthdate = db.Column(
        db.Date,
        info={
            'display_order': 1,
            'type': 'datepicker',
            'template_options': {
                'required': True,
                'label': 'Your date of birth*'
            }
        }
    )

    sex = db.Column(
        db.String,
        info={
            'display_order': 2,
            'type': 'radio',
            'template_options': {
                'required': True,
                'label': 'Your biological sex*:',
                'options': [
                    {'value': 'male', 'label': 'Male'},
                    {'value': 'female', 'label': 'Female'},
                    {'value': 'intersex', 'label': 'Intersex'},
                    {'value': 'no_answer', 'label': 'Prefer not to answer'}
                ]
            }
        }
    )

    gender_identity = db.Column(
        db.String,
        info={
            'display_order': 3.1,
            'type': 'radio',
            'class_name': 'vertical-radio-group',
            'template_options': {
                'required': True,
                'options': [
                    {'value': 'male', 'label': 'Male'},
                    {'value': 'female', 'label': 'Female'},
                    {'value': 'intersex', 'label': 'Intersex'},
                    {'value': 'transgender', 'label': 'Transgender'},
                    {'value': 'genderOther', 'label': 'Other'},
                    {'value': 'no_answer', 'label': 'Prefer not to answer'}
                ]
            }
        }
    )

    gender_identity_other = db.Column(
        db.String,
        info={
            'display_order': 3.2,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter gender identity'
            },
            'hide_expression': '!(model.gender_identity && (model.gender_identity === "genderOther"))',
        }
    )

    race_ethnicity = db.Column(
        db.String,
        info={
            'display_order': 4.1,
            'type': 'radio',
            'template_options': {
                'required': True,
                'label': 'Your race/ethnicity (select all that apply)',
                'options': [
                    {'value': 'raceBlack', 'label': 'Black / African / African American'},
                    {'value': 'raceAsian', 'label': 'Asian / Asian American'},
                    {'value': 'raceWhite', 'label': 'White / Caucasian'},
                    {'value': 'raceHispanic', 'label': 'Hispanic / Latin(o / a)'},
                    {'value': 'raceNative', 'label': 'Native American / Alaskan Native'},
                    {'value': 'racePacific', 'label': 'Pacific Islander'},
                    {'value': 'raceNoAnswer', 'label': 'Prefer not to answer'},
                    {'value': 'raceOther', 'label': 'Other'}
                ]
            }
        }
    )

    race_ethnicity_other = db.Column(
        db.String,
        info={
            'display_order': 4.2,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter race/ethnicity'
            },
            'hideExpression': '!(model.race_ethnicity && (model.race_ethnicity === "raceOther"))',
        }
    )

    is_english_primary = db.Column(
        db.Boolean,
        info={
            'display_order': 5,
            'type': 'radio',
            'default': True,
            'template_options': {
                'required': True,
                'label': 'Is your primary language English*?',
                'options': [
                    {'value': 'true', 'label': 'True'},
                    {'value': 'false', 'label': 'False'}
                ]
            }
        }
    )

    relationship_to_child = db.Column(
        db.String,
        info={
            'display_order': 6.1,
            'type': 'radio',
            'default': True,
            'template_options': {
                'required': True,
                'label': '',
                'options': [
                    {'value': 'bioMother', 'label': 'Biological mother'},
                    {'value': 'bioFather', 'label': 'Biological father'},
                    {'value': 'adoptMother', 'label': 'Adoptive mother'},
                    {'value': 'adoptFather', 'label': 'Adoptive father'},
                    {'value': 'other', 'label': 'Other'}
                ]
            }
        }
    )

    relationship_to_child_other = db.Column(
        db.String,
        info={
            'display_order': 6.2,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter your relationship to your child'
            },
            'hideExpression': '!(model.relationship_to_child && (model.relationship_to_child === "other"))',
        }
    )

    def get_meta(self):
        info = {
            'table': {
                'sensitive': False,
                'label': 'Other Guardian’s Demographics'
            },
            'field_groups': {
                'gender': {
                    'fields': [
                        'gender_identity',
                        'gender_identity_other'
                    ],
                    'display_order': 3,
                    'wrappers': ['card'],
                    'template_options': {
                        'label': 'Gender identity'
                    }
                },
                'race': {
                    'fields': [
                        'race_ethnicity',
                        'race_ethnicity_other'
                    ],
                    'display_order': 4,
                    'wrappers': ['card'],
                    'template_options': {
                        'label': 'Your race/ethnicity (select all that apply):'
                    }
                },
                'relationship': {
                    'fields': [
                        'relationship_to_child',
                        'relationship_to_child_other'
                    ],
                    'display_order': 6,
                    'wrappers': ['card'],
                    'template_options': {
                        'label': 'Your relationship to your child:'
                    }
                }
            }
        }
        for c in self.metadata.tables['guardian_demographics_questionnaire'].columns:
            info[c.name] = c.info
        return info


class GuardianDemographicsQuestionnaireSchema(ModelSchema):
    class Meta:
        model = GuardianDemographicsQuestionnaire
        fields = ('id', 'last_updated', 'guardian_id', 'birthdate', 'sex', 'race_ethnicity', 'is_english_primary',
                  'relationship_to_child')


class GuardianDemographicsQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = GuardianDemographicsQuestionnaire
        fields = ('get_meta',)
