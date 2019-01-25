from flask_marshmallow.sqla import ModelSchema
from marshmallow import fields
from sqlalchemy import func


from app import ma, db
from app.model.category import Category
from app.model.questionnaires.contact_questionnaire import ContactQuestionnaire
from app.model.questionnaires.demographics_questionnaire import DemographicsQuestionnaire
from app.model.questionnaires.guardian_demographics_questionnaire import GuardianDemographicsQuestionnaire
from app.model.organization import Organization
from app.model.resource import StarResource
from app.model.resource_category import ResourceCategory
from app.model.study import Study
from app.model.study_category import StudyCategory
from app.model.training import Training
from app.model.training_category import TrainingCategory
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
        fields = ('id', 'name', 'children', 'parent_id', 'parent', 'level', 'resource_count', 'study_count', 'training_count',
                  '_links')
    id = fields.Integer(required=False, allow_none=True)
    parent_id = fields.Integer(required=False, allow_none=True)
    children = fields.Nested('self', many=True, dump_only=True, exclude=('parent', 'color'))
    parent = fields.Nested(ParentCategorySchema, dump_only=True)
    level = fields.Function(lambda obj: obj.calculate_level(), dump_only=True)
    resource_count = fields.Method('get_resource_count')
    study_count = fields.Method('get_study_count')
    training_count = fields.Method('get_training_count')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.categoryendpoint', id='<id>'),
        'collection': ma.URLFor('api.categorylistendpoint')
    })

    def get_resource_count(self, obj):
        query = db.session.query(ResourceCategory).join(ResourceCategory.resource)\
            .filter(ResourceCategory.category_id == obj.id)
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        return query.session.execute(count_q).scalar()

    def get_study_count(self, obj):
        query = db.session.query(StudyCategory).join(StudyCategory.study)\
            .filter(StudyCategory.category_id == obj.id)
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        return query.session.execute(count_q).scalar()

    def get_training_count(self, obj):
        query = db.session.query(TrainingCategory).join(TrainingCategory.training)\
            .filter(TrainingCategory.category_id == obj.id)
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        return query.session.execute(count_q).scalar()


class CategoriesOnResourceSchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id', 'category')
    category = fields.Nested(ParentCategorySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.resourcecategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'resource': ma.URLFor('api.resourceendpoint', id='<resource_id>')
    })


class CategoriesOnStudySchema(ModelSchema):
    class Meta:
        model = StudyCategory
        fields = ('id', '_links', 'study_id', 'category_id', 'category')
    category = fields.Nested(ParentCategorySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studycategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
    })


class CategoriesOnTrainingSchema(ModelSchema):
    class Meta:
        model = TrainingCategory
        fields = ('id', '_links', 'training_id', 'category_id', 'category')
    category = fields.Nested(ParentCategorySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.trainingcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'training': ma.URLFor('api.trainingendpoint', id='<training_id>')
    })


class StarResourceSchema(ModelSchema):
    class Meta:
        model = StarResource
        fields = ('id', 'title', 'last_updated', 'description', 'image_url', 'image_caption', 'organization_id',
                  'street_address1', 'street_address2', 'city', 'state', 'zip', 'county', 'phone', 'website',
                  'organization', 'resource_categories', '_links')
    organization_id = fields.Integer(required=False, allow_none=True)
    organization = fields.Nested(OrganizationSchema(), dump_only=True, allow_none=True)
    resource_categories = fields.Nested(CategoriesOnResourceSchema(), many=True, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.resourceendpoint', id='<id>'),
        'collection': ma.URLFor('api.resourcelistendpoint'),
        'organization': ma.UrlFor('api.organizationendpoint', id='<organization_id>'),
        'categories': ma.UrlFor('api.categorybyresourceendpoint', resource_id='<id>')
    })


class ResourceCategoriesSchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id', 'category')
    category = fields.Nested(CategorySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.resourcecategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'resource': ma.URLFor('api.resourceendpoint', id='<resource_id>')
    })


class CategoryResourcesSchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id', 'resource')
    resource = fields.Nested(StarResourceSchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.resourcecategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'resource': ma.URLFor('api.resourceendpoint', id='<resource_id>')
    })


class ResourceCategorySchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.resourcecategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'resource': ma.URLFor('api.resourceendpoint', id='<resource_id>')
    })


class StudySchema(ModelSchema):
    class Meta:
        model = Study
        fields = ('id', 'title', 'last_updated', 'description', 'researcher_description', 'participant_description',
                  'outcomes_description', 'enrollment_start_date', 'enrollment_end_date', 'current_num_participants',
                  'max_num_participants', 'start_date', 'end_date', 'website', 'organization_id', 'organization',
                  'study_categories', '_links')
    organization_id = fields.Integer(required=False, allow_none=True)
    organization = fields.Nested(OrganizationSchema(), dump_only=True, allow_none=True)
    study_categories = fields.Nested(CategoriesOnStudySchema(), many=True, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studyendpoint', id='<id>'),
        'collection': ma.URLFor('api.studylistendpoint'),
        'organization': ma.UrlFor('api.organizationendpoint', id='<organization_id>'),
        'categories': ma.UrlFor('api.categorybystudyendpoint', study_id='<id>')
    })


class StudyCategoriesSchema(ModelSchema):
    class Meta:
        model = StudyCategory
        fields = ('id', '_links', 'study_id', 'category_id', 'category')
    category = fields.Nested(CategorySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studycategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
    })


class CategoryStudiesSchema(ModelSchema):
    class Meta:
        model = StudyCategory
        fields = ('id', '_links', 'study_id', 'category_id', 'study')
    study = fields.Nested(StudySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studycategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
    })


class StudyCategorySchema(ModelSchema):
    class Meta:
        model = StudyCategory
        fields = ('id', '_links', 'study_id', 'category_id')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studycategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
    })


class TrainingSchema(ModelSchema):
    class Meta:
        model = Training
        fields = ('id', 'title', 'last_updated', 'description', 'outcomes_description', 'image_url', 'image_caption',
                  'website', 'organization_id', 'organization', 'training_categories', '_links')
    organization_id = fields.Integer(required=False, allow_none=True)
    organization = fields.Nested(OrganizationSchema(), dump_only=True, allow_none=True)
    training_categories = fields.Nested(CategoriesOnTrainingSchema(), many=True, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.trainingendpoint', id='<id>'),
        'collection': ma.URLFor('api.traininglistendpoint'),
        'organization': ma.UrlFor('api.organizationendpoint', id='<organization_id>'),
        'categories': ma.UrlFor('api.categorybytrainingendpoint', training_id='<id>')
    })


class TrainingCategoriesSchema(ModelSchema):
    class Meta:
        model = TrainingCategory
        fields = ('id', '_links', 'training_id', 'category_id', 'category')
    category = fields.Nested(CategorySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.trainingcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'training': ma.URLFor('api.trainingendpoint', id='<training_id>')
    })


class CategoryTrainingsSchema(ModelSchema):
    class Meta:
        model = TrainingCategory
        fields = ('id', '_links', 'training_id', 'category_id', 'training')
    training = fields.Nested(TrainingSchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.trainingcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'training': ma.URLFor('api.trainingendpoint', id='<training_id>')
    })


class TrainingCategorySchema(ModelSchema):
    class Meta:
        model = TrainingCategory
        fields = ('id', '_links', 'training_id', 'category_id')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.trainingcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'training': ma.URLFor('api.trainingendpoint', id='<training_id>')
    })


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'last_updated', 'first_name', 'last_name', 'email', 'password', 'role')
    password = fields.String(load_only=True)
    id = fields.Integer(required=False, allow_none=True)




