import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class IdentificationQuestionnaire(db.Model):
    __tablename__ = 'identification_questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
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
    relationship_to_participant = db.Column(
        db.String,
        info={
            'display_order': 1.1,
            'type': 'radio',
            'default': 'self',
            'template_options': {
                'required': False,
                'label': '',
                'options': [
                    {'value': 'bioMother', 'label': 'Biological mother'},
                    {'value': 'bioFather', 'label': 'Biological father'},
                    {'value': 'adoptMother', 'label': 'Adoptive mother'},
                    {'value': 'adoptFather', 'label': 'Adoptive father'},
                    {'value': 'other', 'label': 'Other'}
                ]
            },
            'hideExpression': '(model.is_self))',
        }
    )
    relationship_to_participant_other = db.Column(
        db.String,
        info={
            'display_order': 1.2,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter your relationship to your child or the person with autism on whom '
                               'you are providing information'
            },
            'hideExpression': '(model.is_self) || !(model.relationship_to_child && '
                              '(model.relationship_to_child === "other"))',
        }
    )
    first_name = db.Column(
        db.String,
        info={
            'display_order': 2,
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
            'display_order': 3,
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
            'display_order': 4,
            'type': 'input',
            'template_options': {
                'label': 'Last name',
                'required': True
            }
        }
    )
    is_first_name_preferred = db.Column(
        db.Boolean,
        info={
            'display_order': 5,
            'type': 'radio',
            'default_value': True,
            'template_options': {
                'required': False,
                'label': 'Is this the preferred name?',
                'options': [
                    {'value': True, 'label': 'Yes'},
                    {'value': False, 'label': 'No'}
                ]
            },
            'expression_properties': {
                'template_options.label': '"Is this your " + (!model.is_self ? "child\'s " : "") + "preferred name?"'
            }
        }
    )
    nickname = db.Column(
        db.String,
        info={
            'display_order': 6,
            'type': 'input',
            'template_options': {
                'label': 'Nickname',
                'required': False
            },
            'hide_expression': 'model.is_first_name_preferred'
        }
    )
    birthdate = db.Column(
        db.Date,
        info={
            'display_order': 7,
            'type': 'datepicker',
            'template_options': {
                'required': True,
                'label': 'Date of birth'
            },
            'expression_properties': {
                'template_options.label': '(model.is_self ? "Your" : (model.nickname || model.first_name || "Your child") + "\'s") + " date of birth"'
            }
        }
    )
    birth_city = db.Column(
        db.String,
        info={
            'display_order': 8,
            'type': 'input',
            'template_options': {
                'required': True,
                'label': 'City/municipality of birth'
            },
            'expression_properties': {
                'template_options.label': '(model.is_self ? "Your" : (model.nickname || model.first_name || "Your child") + "\'s") + " city/municipality of birth"'
            }
        }
    )
    birth_state = db.Column(
        db.String,
        info={
            'display_order': 9,
            'type': 'input',
            'template_options': {
                'required': True
            },
            'expression_properties': {
                'template_options.label': '(model.is_self ? "Your" : (model.nickname || model.first_name || "Your child") + "\'s") + " state of birth"'
            }
        }
    )
    is_english_primary = db.Column(
        db.Boolean,
        info={
            'display_order': 10,
            'type': 'radio',
            'default': True,
            'template_options': {
                'required': False,
                'label': 'Is the primary language English?',
                'options': [
                    {'value': 'true', 'label': 'True'},
                    {'value': 'false', 'label': 'False'}
                ]
            },
            'expression_properties': {
                'template_options.label': '"Is " + (model.is_self ? "your" : (model.nickname || model.first_name || "your child") + "\'s") + " primary language English?"'
            }

        }
    )

    def get_meta(self):
        info = {
            'table': {
                'sensitive': False,
                'label': 'Identification',
                'description': '',
            },
            'field_groups': {
                'intro': {
                    'fields': [],
                    'display_order': 0,
                    'wrappers': ['help'],
                    'template_options': {
                        'description': ''
                    },
                    'expression_properties': {
                        'template_options.description': '"Please answer the following questions about " + '
                        '(model.is_self ? "yourself" : "your child or the person with autism on whom '
                        'you are providing information") + " (* indicates required response):"'
                    }
                },
                'relationship': {
                    'fields': [
                        'relationship_to_participant',
                        'relationship_to_participant_other'
                    ],
                    'display_order': 1,
                    'wrappers': ['card'],
                    'template_options': {
                        'label': 'Your relationship to your child or the person with autism on whom '
                        'you are providing information:'
                    }
                }
            }
        }
        for c in self.metadata.tables['identification_questionnaire'].columns:
            if c.info:
                info[c.name] = c.info
        return info


class IdentificationQuestionnaireSchema(ModelSchema):
    class Meta:
        model = IdentificationQuestionnaire
        fields = ('id', 'last_updated', 'participant_id', 'user_id', 'first_name', 'middle_name', 'last_name',
                  'nickname', 'is_first_name_preferred', 'birthdate', 'birth_city', 'birth_state', 'is_english_primary')


class IdentificationQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = IdentificationQuestionnaire
        fields = ('get_meta',)

