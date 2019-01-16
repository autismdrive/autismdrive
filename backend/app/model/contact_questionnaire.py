import datetime

from app import db


class ContactQuestionnaire(db.Model):
    __tablename__ = 'contact_questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    participant_id = db.Column('participant_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    is_first_name_preferred = db.Column(db.Boolean)
    nickname = db.Column(db.String)
    phone = db.Column(db.String)
    phone_type = db.Column(db.String)
    can_leave_voicemail = db.Column(db.Boolean)
    contact_times = db.Column(db.String)
    email = db.Column(db.String)
    street_address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.Integer)
    marketing_channel = db.Column(db.String)

    info = {'table': {'sensitive': 'false', 'label': 'Research Registrant Contact Information',
            'description': 'Please answer the following questions about YOURSELF (* indicates required response):'},
            'first_name': {'key': 'firstname', 'type': 'input', 'template_label': 'First name', 'required': 'true'},
            'last_name': {'key': 'lastname', 'type': 'input', 'template_label': 'Last name', 'required': 'true'},
            'is_first_name_preferred': {'key': 'firstNamePreferred', 'type': 'radio',
                                        'template_label': 'Is this your preferred name/nick name?', 'required': 'false'},
            'nickname': {'key': 'nickname', 'type': 'input', 'template_label': 'Preferred name or nickname', 'required': 'false'},
            'phone': {'wrapper_key': 'phone', 'wrapper_label': 'Phone', 'key': 'phone', 'type': 'input',
                      'template_type': 'tel', 'required': 'true',
                      'template_label': 'Preferred phone number (including area code)', 'validation': 'phone'},
            'phone_type': {'wrapper_key': 'phone', 'wrapper_label': 'Phone', 'key': 'phoneType', 'type': 'radio',
                           'template_type': 'tel', 'required': 'true', 'template_label': '',
                           'options': [{'value': 'home', 'label': 'Home'}, {'value': 'cell', 'label': 'Cell'}]},
            'can_leave_voicemail': {'wrapper_key': 'phone', 'wrapper_label': 'Phone', 'key': 'canLeaveVoicemail',
                                    'type': 'radio', 'default_value': 'true',
                                    'template_label': 'Is it okay to leave a voicemail message at this number?',
                                    'required': 'false'},
            'contact_times': {'wrapper_key': 'phone', 'wrapper_label': 'Phone', 'key': 'contactTimes', 'type': 'textarea',
                              'template_label': 'Some research studies might involve a phone call. If that’s the case, '
                                                'when would be the best times of day to call you?', 'required': 'false'},
            'email': {'key': 'email', 'type': 'input', 'template_label': 'Email', 'required': 'true', 'validation': 'email'},
            'street_address': {'wrapper_key': 'address', 'wrapper_label': 'Address', 'key': 'streetAddress',
                               'type': 'input', 'template_label': 'Street Address', 'required': 'true'},
            'city': {'wrapper_key': 'address', 'wrapper_label': 'Address', 'key': 'city', 'type': 'input',
                     'template_label': 'Town/City', 'required': 'false'},
            'state': {'wrapper_key': 'address', 'wrapper_label': 'Address', 'key': 'state', 'type': 'input',
                      'template_label': 'State', 'required': 'false'},
            'zip': {'wrapper_key': 'address', 'wrapper_label': 'Address', 'key': 'zip', 'type': 'input',
                    'template_type': 'number', 'template_label': 'Zip', 'max': 99999, 'min': 0, 'pattern': '\\d{5}',
                    'required': 'true'},
            'marketing_channel': {'wrapper_key': 'marketing', 'wrapper_label': 'How did you hear about us?',
                                  'type': 'radio', 'class_name': 'vertical-radio-group', 'template_type': 'number',
                                  'required': 'true',
                                  'options': [{'value': '1', 'label': 'Internet'},
                                              {'value': '2', 'label': 'Health care provider (doctor, speech therapist, etc)'},
                                              {'value': '3', 'label': 'Teacher or school'},
                                              {'value': '4', 'label': 'Word of mouth (friend, family member, etc)'},
                                              {'value': '5', 'label': 'Community event (autism walk, resource fair, etc.)'},
                                              {'value': '6', 'label': 'Television or radio (CNN, NPR, local news, etc.)'},
                                              {'value': '7', 'label': 'While participating in a research study'},
                                              {'value': '8', 'label': 'Other'},
                                             ]
                                  }
            }
