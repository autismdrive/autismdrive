from flask_marshmallow.sqla import ModelSchema
from marshmallow import fields

from app import ma
from app.model.category import Category
from app.model.organization import Organization
from app.model.resource import StarResource
from app.model.study import Study
from app.model.training import Training
from app.model.user import User


class OrganizationSchema(ModelSchema):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'last_updated', 'description', 'resources', 'studies', 'trainings')


class ParentCategorySchema(ModelSchema):
    """Provides a view of the parent category, all the way to the top, but ignores children"""
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'level', '_links')
    parent = fields.Nested('self', dump_only=True)
    level = fields.Function(lambda obj: obj.calculate_level())
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.categoryendpoint', id='<id>'),
        'collection': ma.URLFor('api.categorylistendpoint')
    })


class CategorySchema(ModelSchema):
    """Provides detailed information about a category, including all the children"""
    class Meta:
        model = Category
        fields = ('id', 'name', 'children', 'parent_id', 'parent', '_links')
    id = fields.Integer(required=False, allow_none=True)
    parent_id = fields.Integer(required=False, allow_none=True)
    children = fields.Nested('self', many=True, dump_only=True, exclude=('parent', 'color'))
    parent = fields.Nested(ParentCategorySchema, dump_only=True)
    level = fields.Function(lambda obj: obj.calculate_level(), dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.categoryendpoint', id='<id>'),
        'collection': ma.URLFor('api.categorylistendpoint')
    })


class StarResourceSchema(ModelSchema):
    class Meta:
        model = StarResource
        fields = ('id', 'title', 'last_updated', 'description', 'image_url', 'image_caption', 'organization_id',
                  'street_address1', 'street_address2', 'city', 'state', 'zip', 'county', 'phone', 'website',
                  'organization')
    organization_id = fields.Integer(required=False, allow_none=True)
    organization = fields.Nested(OrganizationSchema(), dump_only=True, allow_none=True)


class StudySchema(ModelSchema):
    class Meta:
        model = Study
        fields = ('id', 'title', 'last_updated', 'description', 'researcher_description', 'participant_description',
                  'outcomes_description', 'enrollment_start_date', 'enrollment_end_date', 'current_num_participants',
                  'max_num_participants', 'start_date', 'end_date', 'website', 'organization_id', 'organization')
    organization_id = fields.Integer(required=False, allow_none=True)
    organization = fields.Nested(OrganizationSchema(), dump_only=True, allow_none=True)


class TrainingSchema(ModelSchema):
    class Meta:
        model = Training
        fields = ('id', 'title', 'last_updated', 'description', 'outcomes_description', 'image_url', 'image_caption',
                  'website', 'organization_id', 'organization')
    organization_id = fields.Integer(required=False, allow_none=True)
    organization = fields.Nested(OrganizationSchema(), dump_only=True, allow_none=True)


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'last_updated', 'first_name', 'last_name', 'email', 'password', 'role')
    password = fields.String(load_only=True)
    id = fields.Integer(required=False, allow_none=True)
