from flask_marshmallow.sqla import ModelSchema
from marshmallow import fields, Schema, post_load
from marshmallow_enum import EnumField
from sqlalchemy import func


from app import ma, db
from app.model.admin_note import AdminNote
from app.model.category import Category
from app.model.participant import Participant, Relationship
from app.model.investigator import Investigator
from app.model.email_log import EmailLog
from app.model.event import Event
from app.model.location import Location
from app.model.resource import Resource
from app.model.resource_category import ResourceCategory
from app.model.resource_change_log import ResourceChangeLog
from app.model.role import Role
from app.model.search import Search, Sort
from app.model.step_log import StepLog
from app.model.study import Study, Status
from app.model.study_category import StudyCategory
from app.model.study_investigator import StudyInvestigator
from app.model.study_user import StudyUser, StudyUserStatus
from app.model.user import User
from app.model.user_favorite import UserFavorite
from app.model.event_user import EventUser
from app.model.zip_code import ZipCode

# Import the questionnaires and their related models in order to include them when auto-generating migrations (and to
# ensure that the tables don't get accidentally dropped!)
# Models:
import app.model.questionnaires.assistive_device
import app.model.questionnaires.housemate
import app.model.questionnaires.medication
import app.model.questionnaires.therapy
# Questionnaires:
import app.model.questionnaires.contact_questionnaire
import app.model.questionnaires.clinical_diagnoses_questionnaire
import app.model.questionnaires.current_behaviors_dependent_questionnaire
import app.model.questionnaires.current_behaviors_self_questionnaire
import app.model.questionnaires.demographics_questionnaire
import app.model.questionnaires.developmental_questionnaire
import app.model.questionnaires.education_dependent_questionnaire
import app.model.questionnaires.education_self_questionnaire
import app.model.questionnaires.employment_questionnaire
import app.model.questionnaires.evaluation_history_dependent_questionnaire
import app.model.questionnaires.evaluation_history_self_questionnaire
import app.model.questionnaires.home_dependent_questionnaire
import app.model.questionnaires.home_self_questionnaire
import app.model.questionnaires.identification_questionnaire
import app.model.questionnaires.professional_profile_questionnaire
import app.model.questionnaires.supports_questionnaire
import app.model.questionnaires.registration_questionnaire







class InvestigatorSchema(ModelSchema):
    class Meta:
        model = Investigator
        fields = ('id', 'last_updated', 'name', 'title', 'organization_name', 'bio_link',
                  '_links')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.investigatorendpoint', id='<id>'),
        'collection': ma.URLFor('api.investigatorlistendpoint'),
    })


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


class ChildCategoryInSearchSchema(ModelSchema):
    """Children within a category have hit counts when returned as a part of a search."""
    class Meta:
        model = Category
        fields = ('id', 'name', '_links', 'hit_count')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.categoryendpoint', id='<id>'),
        'collection': ma.URLFor('api.categorylistendpoint')
    })


class CategoryInSearchSchema(ModelSchema):
    """streamlined category representation for inclusion in search results to provide faceted search"""
    class Meta:
        model = Category
        fields = ('id', 'name', 'children', 'parent_id', 'parent', 'level')
    parent_id = fields.Number(required=False, allow_none=True)
    parent = fields.Nested(ParentCategorySchema, dump_only=True, required=False, allow_none=True)
    children = fields.Nested(ChildCategoryInSearchSchema, many=True, dump_only=True)
    level = fields.Function(lambda obj: obj.calculate_level(), dump_only=True)


class CategorySchema(ModelSchema):
    """Provides detailed information about a category, including all the children"""
    class Meta:
        model = Category
        fields = ('id', 'name', 'children', 'parent_id', 'parent', 'level', 'event_count', 'location_count',
                  'resource_count', 'all_resource_count', 'study_count', '_links')
    id = fields.Integer(required=False, allow_none=True)
    parent_id = fields.Integer(required=False, allow_none=True)
    children = fields.Nested('self', many=True, dump_only=True, exclude=('parent', 'color'))
    parent = fields.Nested(ParentCategorySchema, dump_only=True)
    level = fields.Function(lambda obj: obj.calculate_level(), dump_only=True)
    event_count = fields.Method('get_event_count', dump_only=True)
    location_count = fields.Method('get_location_count', dump_only=True)
    resource_count = fields.Method('get_resource_count', dump_only=True)
    all_resource_count = fields.Method('get_all_resource_count', dump_only=True)
    study_count = fields.Method('get_study_count', dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.categoryendpoint', id='<id>'),
        'collection': ma.URLFor('api.categorylistendpoint')
    })

    def get_event_count(self, obj):
        query = db.session.query(ResourceCategory).filter(ResourceCategory.type == 'event')\
            .filter(ResourceCategory.category_id == obj.id)
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        return query.session.execute(count_q).scalar()

    def get_location_count(self, obj):
        query = db.session.query(ResourceCategory).filter(ResourceCategory.type == 'location')\
            .filter(ResourceCategory.category_id == obj.id)
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        return query.session.execute(count_q).scalar()

    def get_resource_count(self, obj):
        query = db.session.query(ResourceCategory).filter(ResourceCategory.type == 'resource')\
            .filter(ResourceCategory.category_id == obj.id)
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        return query.session.execute(count_q).scalar()

    def get_all_resource_count(self, obj):
        query = db.session.query(ResourceCategory).join(ResourceCategory.resource)\
            .filter(ResourceCategory.category_id == obj.id)
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        return query.session.execute(count_q).scalar()

    def get_study_count(self, obj):
        query = db.session.query(StudyCategory).join(StudyCategory.study)\
            .filter(StudyCategory.category_id == obj.id)
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        return query.session.execute(count_q).scalar()


class CategoriesOnEventSchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id', 'category')
    category = fields.Nested(ParentCategorySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.eventcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'event': ma.URLFor('api.eventendpoint', id='<resource_id>')
    })


class CategoriesOnLocationSchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id', 'category')
    category = fields.Nested(ParentCategorySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.locationcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'location': ma.URLFor('api.locationendpoint', id='<resource_id>')
    })


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


class InvestigatorsOnStudySchema(ModelSchema):
    class Meta:
        model = StudyInvestigator
        fields = ('id', '_links', 'study_id', 'investigator_id', 'investigator')
    investigator = fields.Nested(InvestigatorSchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studyinvestigatorendpoint', id='<id>'),
        'investigator': ma.URLFor('api.investigatorendpoint', id='<investigator_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
    })


class ResourceSchema(ModelSchema):
    class Meta:
        model = Resource
        fields = ('id', 'type', 'title', 'last_updated', 'description', 'organization_name', 'phone', 'website',
                  'contact_email', 'video_code', 'is_uva_education_content', 'resource_categories',
                  'is_draft', 'ages', 'insurance', 'phone_extension', 'languages', 'covid19_categories', '_links')
    resource_categories = fields.Nested(CategoriesOnResourceSchema(), many=True, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.resourceendpoint', id='<id>'),
        'collection': ma.URLFor('api.resourcelistendpoint'),
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
    resource = fields.Nested(ResourceSchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.resourcecategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'resource': ma.URLFor('api.resourceendpoint', id='<resource_id>')
    })


class ResourceCategorySchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id', 'type')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.resourcecategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'resource': ma.URLFor('api.resourceendpoint', id='<resource_id>')
    })


class EventUserSchema(ModelSchema):
    class Meta:
        model = EventUser
        fields = ('id', 'last_updated', 'event_id', 'event', 'user_id', 'user')
    event_id = fields.Integer(required=False, allow_none=True)
    user_id = fields.Integer(required=False, allow_none=True)
    event = fields.Nested(ResourceSchema, dump_only=True)
    user = fields.Nested(CategorySchema, dump_only=True)


class EventSchema(ModelSchema):
    class Meta:
        model = Event
        fields = ('id', 'type', 'title', 'last_updated', 'description', 'date', 'time', 'ticket_cost',
                  'primary_contact', 'location_name', 'street_address1', 'street_address2', 'city', 'state', 'zip',
                  'phone', 'website', 'contact_email', 'video_code', 'is_uva_education_content', 'is_draft',
                  'organization_name', 'resource_categories', 'latitude', 'longitude',  'ages', 'insurance',
                  'phone_extension', 'languages', 'covid19_categories', 'includes_registration', 'webinar_link',
                  'post_survey_link', 'max_users', 'registered_users', '_links')
    id = fields.Integer(required=False, allow_none=True)
    resource_categories = fields.Nested(CategoriesOnEventSchema(), many=True, dump_only=True)
    registered_users = fields.Nested(EventUserSchema(), many=True, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.eventendpoint', id='<id>'),
        'collection': ma.URLFor('api.eventlistendpoint'),
        'categories': ma.UrlFor('api.categorybyeventendpoint', event_id='<id>')
    })


class EventCategoriesSchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id', 'category')
    category = fields.Nested(CategorySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.eventcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'event': ma.URLFor('api.eventendpoint', id='<resource_id>')
    })


class CategoryEventsSchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id', 'resource')
    resource = fields.Nested(EventSchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.eventcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'event': ma.URLFor('api.eventendpoint', id='<resource_id>')
    })


class EventCategorySchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.eventcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'event': ma.URLFor('api.eventendpoint', id='<resource_id>')
    })


class LocationSchema(ModelSchema):
    class Meta:
        model = Location
        fields = ('id', 'type', 'title', 'last_updated', 'description', 'primary_contact',
                  'street_address1', 'street_address2', 'city', 'state', 'zip', 'phone', 'email', 'website',
                  'contact_email', 'video_code', 'is_uva_education_content', 'organization_name', 'resource_categories',
                  'latitude', 'longitude', '_links', 'ages', 'insurance', 'phone_extension', 'languages',
                  'covid19_categories', 'is_draft')
    id = fields.Integer(required=False, allow_none=True)
    resource_categories = fields.Nested(CategoriesOnLocationSchema(), many=True, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.locationendpoint', id='<id>'),
        'collection': ma.URLFor('api.locationlistendpoint'),
    })


class LocationCategoriesSchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id', 'category')
    category = fields.Nested(CategorySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.locationcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'location': ma.URLFor('api.locationendpoint', id='<resource_id>')
    })


class CategoryLocationsSchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id', 'resource')
    resource = fields.Nested(LocationSchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.locationcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'location': ma.URLFor('api.locationendpoint', id='<resource_id>')
    })


class LocationCategorySchema(ModelSchema):
    class Meta:
        model = ResourceCategory
        fields = ('id', '_links', 'resource_id', 'category_id')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.locationcategoryendpoint', id='<id>'),
        'category': ma.URLFor('api.categoryendpoint', id='<category_id>'),
        'location': ma.URLFor('api.locationendpoint', id='<resource_id>')
    })


class ParticipantSchema(ModelSchema):
    class Meta:
        model = Participant
        fields = ('id', '_links', 'last_updated', 'name', 'relationship', 'user_id', 'avatar_icon', 'avatar_color',
                  'has_consented', 'contact', 'percent_complete')
    id = fields.Integer(required=False, allow_none=True)
    name = fields.Function(lambda obj: obj.get_name())
    relationship = EnumField(Relationship)
    user_id = fields.Integer(required=False, allow_none=True)
    percent_complete = fields.Function(lambda obj: obj.get_percent_complete())
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.participantendpoint', id='<id>'),
        'user': ma.URLFor('api.userendpoint', id='<user_id>')
    })


class UserFavoriteSchema(ModelSchema):
    class Meta:
        model = UserFavorite
        fields = ('id', 'last_updated', 'type', 'user_id', 'resource_id', 'resource', 'category_id', 'category',
                  'age_range', 'language', 'covid19_category')
    resource_id = fields.Integer(required=False, allow_none=True)
    category_id = fields.Integer(required=False, allow_none=True)
    resource = fields.Nested(ResourceSchema, dump_only=True)
    category = fields.Nested(CategorySchema, dump_only=True)


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'last_updated', 'registration_date', 'last_login', 'email', 'password', 'role',
                  'permissions', 'participants', 'token', 'token_url', 'user_favorites', 'participant_count')
    password = fields.String(load_only=True)
    participants = fields.Nested(ParticipantSchema, dump_only=True, many=True)
    participant_count = fields.Integer(required=False, allow_none=True)
    user_favorites = fields.Nested(UserFavoriteSchema, dump_only=True, many=True)
    id = fields.Integer(required=False, allow_none=True)
    role = EnumField(Role)
    permissions = fields.Method('get_permissions', dump_only=True)

    def get_permissions(self, obj):
        permissions = []
        for p in obj.role.permissions():
            permissions.append(p.name)
        return permissions


class UsersOnStudySchema(ModelSchema):
    class Meta:
        model = StudyUser
        fields = ('id', '_links', 'status', 'study_id', 'user_id', 'user')

    user = fields.Nested(UserSchema, dump_only=True)
    status = EnumField(StudyUserStatus, allow_none=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studyuserendpoint', id='<id>'),
        'user': ma.URLFor('api.userendpoint', id='<user_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
    })


class StudyUsersSchema(ModelSchema):
    class Meta:
        model = StudyUser
        fields = ('id', '_links', 'status', 'study_id', 'user_id', 'user')

    user = fields.Nested(UserSchema, dump_only=True)
    status = EnumField(StudyUserStatus, allow_none=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studyuserendpoint', id='<id>'),
        'user': ma.URLFor('api.userendpoint', id='<user_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
    })


class StudyUserSchema(ModelSchema):
    class Meta:
        model = StudyUser
        fields = ('id', '_links', 'status', 'study_id', 'user_id')

    status = EnumField(StudyUserStatus, allow_none=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studyuserendpoint', id='<id>'),
        'user': ma.URLFor('api.userendpoint', id='<user_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
    })


class StudySchema(ModelSchema):
    class Meta:
        model = Study
        fields = ('id', 'title', 'short_title', 'short_description', 'image_url', 'last_updated', 'description',
                  'participant_description', 'benefit_description', 'coordinator_email', 'organization_name',
                  'location', 'status', 'study_categories', 'study_investigators', 'study_users',
                  'eligibility_url', 'survey_url', 'results_url', 'ages', 'languages', 'num_visits', '_links')
    status = EnumField(Status)
    study_categories = fields.Nested(CategoriesOnStudySchema(), many=True, dump_only=True)
    study_investigators = fields.Nested(InvestigatorsOnStudySchema(), many=True, dump_only=True)
    study_users = fields.Nested(UsersOnStudySchema(), many=True, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studyendpoint', id='<id>'),
        'collection': ma.URLFor('api.studylistendpoint'),
        'categories': ma.UrlFor('api.categorybystudyendpoint', study_id='<id>')
    })


class UserStudiesSchema(ModelSchema):
    class Meta:
        model = StudyUser
        fields = ('id', '_links', 'status', 'study_id', 'user_id', 'study')
    study = fields.Nested(StudySchema, dump_only=True)
    status = EnumField(StudyUserStatus, allow_none=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studyuserendpoint', id='<id>'),
        'user': ma.URLFor('api.userendpoint', id='<user_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
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


class StudyInvestigatorsSchema(ModelSchema):
    class Meta:
        model = StudyInvestigator
        fields = ('id', '_links', 'study_id', 'investigator_id', 'investigator')
    investigator = fields.Nested(InvestigatorSchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studyinvestigatorendpoint', id='<id>'),
        'investigator': ma.URLFor('api.investigatorendpoint', id='<investigator_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
    })


class InvestigatorStudiesSchema(ModelSchema):
    class Meta:
        model = StudyInvestigator
        fields = ('id', '_links', 'study_id', 'investigator_id', 'study')
    study = fields.Nested(StudySchema, dump_only=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studyinvestigatorendpoint', id='<id>'),
        'investigator': ma.URLFor('api.investigatorendpoint', id='<investigator_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
    })


class StudyInvestigatorSchema(ModelSchema):
    class Meta:
        model = StudyInvestigator
        fields = ('id', '_links', 'study_id', 'investigator_id')
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.studyinvestigatorendpoint', id='<id>'),
        'investigator': ma.URLFor('api.investigatorendpoint', id='<investigator_id>'),
        'study': ma.URLFor('api.studyendpoint', id='<study_id>')
    })


class SearchSchema(ma.Schema):

    class HitSchema(ma.Schema):
        id = fields.Integer()
        content = fields.Str(missing=None)
        description = fields.Str(missing=None)
        title = fields.Str(missing=None)
        type = fields.Str()
        label = fields.Str(missing=None)
        last_updated = fields.Date(missing=None)
        highlights = fields.Str(missing=None)
        latitude = fields.Float()
        longitude = fields.Float()
        date = fields.Date(missing=None)
        status = fields.Str(missing=None)
        no_address = fields.Boolean(missing=None)
        is_draft = fields.Boolean(missing=None)

    class SortSchema(ma.Schema):
        field = fields.Str(allow_null=True)
        latitude = fields.Float(missing=None)
        longitude = fields.Float(missing=None)
        order = fields.Str(missing='asc')
        unit = fields.Str(missing='mi')

        @post_load
        def make_sort(self, data):
            return Sort(**data)

    class AggCountSchema(ma.Schema):
        value = fields.String()
        count = fields.Integer()
        is_selected = fields.Boolean()

    words = fields.Str()
    start = fields.Integer()
    size = fields.Integer()
    sort = ma.Nested(SortSchema, allow_none=True, default=None)
    types = fields.List(fields.Str())
    ages = fields.List(fields.Str())
    languages = fields.List(fields.Str())
    age_counts = fields.List(ma.Nested(AggCountSchema), dump_only=True)
    language_counts = fields.List(ma.Nested(AggCountSchema), dump_only=True)
    type_counts = fields.List(ma.Nested(AggCountSchema), dump_only=True)
    total = fields.Integer(dump_only=True)
    hits = fields.Nested(HitSchema(), many=True, dump_only=True)
    category = ma.Nested(CategoryInSearchSchema)
    ordered = True
    date = fields.Date(allow_none=True)
    map_data_only = fields.Boolean()

    @post_load
    def make_search(self, data):
        return Search(**data)


class UserSearchSchema(ma.Schema):
    pages = fields.Integer()
    total = fields.Integer()
    items = ma.List(ma.Nested(UserSchema))


class StepSchema(Schema):
    name = fields.Str()
    type = fields.Str()
    label = fields.Str()
    status = fields.Str()
    date_completed = fields.Date()
    questionnaire_id = fields.Integer()


class FlowSchema(Schema):
    name = fields.Str()
    steps = fields.Nested(StepSchema(), many=True)


class EmailLogSchema(ModelSchema):
    class Meta:
        model = EmailLog
        include_fk = True


class ResourceChangeLogSchema(ModelSchema):
    class Meta:
        model = ResourceChangeLog
        include_fk = True


class AdminNoteSchema(ModelSchema):
    class Meta:
        model = AdminNote
        fields = ('id', 'resource_id', 'user_id', 'resource', 'user', 'last_updated', 'note')
    user = fields.Nested(UserSchema, dump_only=True)
    resource = fields.Nested(ResourceSchema, dump_only=True)


class StepLogSchema(ModelSchema):
    class Meta:
        model = StepLog
        include_fk = True


class ZipCodeSchema(ModelSchema):
    class Meta:
        model = ZipCode
        fields = ["id", "latitude", "longitude"]
