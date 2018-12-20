from flask_marshmallow.sqla import ModelSchema
from marshmallow import fields
from app.model.organization import Organization
from app.model.resource import StarResource
from app.model.study import Study
from app.model.training import Training
from app.model.user import User


class StarResourceSchema(ModelSchema):
    class Meta:
        model = StarResource
        fields = ('id', 'title', 'last_updated', 'description', 'image_url', 'image_caption', 'organization_id',
                  'street_address1', 'street_address2', 'city', 'state', 'zip', 'county', 'phone', 'website')
    organization_id = fields.Integer(required=False, allow_none=True)


class StudySchema(ModelSchema):
    class Meta:
        model = Study
        fields = ('id', 'title', 'last_updated', 'description', 'researcher_description', 'participant_description',
                  'outcomes_description', 'enrollment_start_date', 'enrollment_end_date', 'current_num_participants',
                  'max_num_participants', 'start_date', 'end_date', 'website', 'organization_id')
    organization_id = fields.Integer(required=False, allow_none=True)


class TrainingSchema(ModelSchema):
    class Meta:
        model = Training
        fields = ('id', 'title', 'last_updated', 'description', 'outcomes_description', 'image_url', 'image_caption',
                  'website', 'organization_id')
    organization_id = fields.Integer(required=False, allow_none=True)


class OrganizationSchema(ModelSchema):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'last_updated', 'description', 'resources', 'studies', 'trainings')
    resources = fields.Nested(StarResourceSchema(), dump_only=True, allow_none=True)
    studies = fields.Nested(StudySchema(), dump_only=True, allow_none=True)
    trainings = fields.Nested(TrainingSchema(), dump_only=True, allow_none=True)


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'last_updated', 'first_name', 'last_name', 'email', 'password', 'role')
    password = fields.String(load_only=True)
    id = fields.Integer(required=False, allow_none=True)
