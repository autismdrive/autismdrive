import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class DemographicsQuestionnaire(db.Model):
    __tablename__ = 'demographics_questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    participant_id = db.Column(
        'participant_id',
        db.Integer,
        db.ForeignKey('stardrive_user.id')
    )
    guardian_id = db.Column(
        'guardian_id',
        db.Integer,
        db.ForeignKey('stardrive_user.id')
    )
    first_name = db.Column(
        db.String,
        info={
            'display_order': 1,
            'type': 'input',
            'template_options': {
                'label': 'First name',
                'required': True
            }
        }
    )
    middle_name = db.Column(
        db.String,
        info={
            'display_order': 2,
            'type': 'input',
            'template_options': {
                'label': 'Middle name',
                'required': False
            }
        }
    )
    last_name = db.Column(
        db.String,
        info={
            'display_order': 3,
            'type': 'input',
            'template_options': {
                'label': 'Last name*',
                'required': True
            }
        }
    )
    is_first_name_preferred = db.Column(
        db.Boolean,
        info={
            'display_order': 4,
            'type': 'radio',
            'template_options': {
                'required': False,
                'label': '"Is this your " + (!model.is_self ? "child\'s ") + "preferred name?"'
            }
        }
    )
    nickname = db.Column(
        db.String,
        info={
            'display_order': 5,
            'type': 'input',
            'template_options': {
                'label': 'Preferred name or nickname',
                'required': False
            },
            'hide_expression': '!model.is_first_name_preferred',
            'hide_label': 'Enter nickname'
        }
    )
    birthdate = db.Column(
        db.Date,
        info={
            'display_order': 6,
            'type': 'datepicker',
            'template_options': {
                'required': True,
                'label': '(model.is_self ? "Your" : model.first_name + "\'s") + " Date of Birth*"'
            }
        }
    )
    birth_city = db.Column(
        db.String,
        info={
            'display_order': 7,
            'type': 'input',
            'template_options': {
                'required': True,
                'label': '(model.is_self ? "Your" : model.first_name + "\'s") + " City/municipality of birth*"'
            }
        }
    )
    birth_state = db.Column(
        db.String,
        info={
            'display_order': 8,
            'type': 'input',
            'template_options': {
                'required': True,
                'label': '(model.is_self ? "Your" : model.first_name + "\'s") + " state of birth*"'
            },
        }
    )
    birth_sex = db.Column(
        db.String,
        info={
            'display_order': 9,
            'type': 'radio',
            'template_options': {
                'required': True,
                'label': '(model.is_self ? "Your" : model.first_name + "\'s") + " sex at birth*"',
                'options': [
                    {'value': 'male', 'label': 'Male'},
                    {'value': 'female', 'label': 'Female'},
                    {'value': 'intersex', 'label': 'Intersex'}
                ]
            }
        }
    )
    gender_identity = db.Column(
        db.String,
        info={
            'display_order': 10,
            'type': 'radio',
            'template_options': {
                'required': True,
                'label': '(model.is_self ? "Your" : model.first_name + "\'s") + " current gender identity '
                         '(how " + (model.is_self ? "you describe yourself)*:" : model.first_name + '
                         '" describes themselves)*:"',
                'options': [
                    {'value': 'male', 'label': 'Male'},
                    {'value': 'female', 'label': 'Female'},
                    {'value': 'intersex', 'label': 'Intersex'},
                    {'value': 'transgender', 'label': 'Transgender'},
                    {'value': 'other', 'label': 'Other'},
                    {'value': 'no_answer', 'label': 'Choose not to answer'}
                ]
            }
            }
    )

    gender_identity_other = db.Column(
        db.String,
        info={
            'display_order': 11,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter gender identity'
            },
            'hideExpression': '!(model.gender_identity && (model.gender_identity === "other"))',
        }
    )

    race_ethnicity = db.Column(
        db.String,
        info={
            'display_order': 12,
            'type': 'radio',
            'template_options': {
                'required': True,
                'label': '"What is " + (model.is_self ? "your" : model.first_name + "\'s" ) + " race/ethnicity? '
                         '(select all that apply)*"',
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
            'display_order': 13,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter race/ethnicity'
            },
            'hideExpression': '!(model.race_ethnicity && (model.race_ethnicity === "other"))',
        }
    )

    is_english_primary = db.Column(
        db.Boolean,
        info={
            'display_order': 14,
            'type': 'radio',
            'default': True,
            'template_options': {
                'required': False,
                'label': '"Is " + (model.is_self ? "your" : model.first_name + "\'s") + " primary language English?"',
                'options': [
                    {'value': 'true', 'label': 'True'},
                    {'value': 'false', 'label': 'False'}
                ]
            }
        }
    )

    def get_meta(self):
        info = {'table': {'sensitive': False,
                          'label': 'Demographics',
                          'description': '"Please answer the following questions about " + '
                                         '(model.is_self ? "yourself" : "your child or the person with autism on whom '
                                         'you are providing information") + " (* indicates required response):"'
                          }
                }
        for c in self.metadata.tables['demographics_questionnaire'].columns:
            info[c.name] = c.info
        return info


class DemographicsQuestionnaireSchema(ModelSchema):
    class Meta:
        model = DemographicsQuestionnaire
        fields = ('id', 'last_updated', 'participant_id', 'guardian_id','first_name', 'middle_name', 'last_name',
                  'nickname', 'is_first_name_preferred', 'birthdate', 'birth_city', 'birth_state', 'birth_sex',
                  'gender_identity', 'race_ethnicity', 'is_english_primary')


class DemographicsQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = DemographicsQuestionnaire
        fields = ('get_meta',)



