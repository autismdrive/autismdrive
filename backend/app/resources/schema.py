from flask_marshmallow.sqla import ModelSchema
from marshmallow import fields
from app.model.resource import StarResource
from app.model.study import Study
from app.model.training import Training
from app.model.user import User


class StarResourceSchema(ModelSchema):
    class Meta:
        model = StarResource
        fields = ('id', 'title', 'last_updated', 'description', 'image', 'image_caption', 'organization',
                  'street_address1', 'street_address2', 'city', 'state', 'zip', 'county', 'phone', 'website')


class StudySchema(ModelSchema):
    class Meta:
        model = Study
        fields = ('id', 'title', 'last_updated', 'description', 'researcher_description', 'participant_description',
                  'outcomes', 'enrollment_date', 'current_enrolled', 'total_participants', 'study_start', 'study_end')


class TrainingSchema(ModelSchema):
    class Meta:
        model = Training
        fields = ('id', 'title', 'last_updated', 'description', 'outcomes', 'image', 'image_caption')


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'last_updated', 'first_name', 'last_name', 'email', 'password', 'role')
    password = fields.String(load_only=True)
    id = fields.Integer(required=False, allow_none=True)
