from flask_marshmallow.fields import Hyperlinks, URLFor
from marshmallow import Schema, post_load, missing, pre_load
from marshmallow.fields import (
    Boolean,
    DateTime,
    Enum,
    Float,
    Function,
    Integer,
    List,
    Method,
    Nested,
    Number,
    Str,
    String,
)
from marshmallow.utils import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import func

from app.database import session
from app.enums import Relationship, Status, Role
from app.models import (
    AdminNote,
    Category,
    EmailLog,
    Resource,
    Location,
    Event,
    Search,
    Study,
    StudyInvestigator,
    StudyCategory,
    EventUser,
    Investigator,
    Participant,
    ResourceCategory,
    Sort,
    Geopoint,
    Geobox,
    StepLog,
    StudyUserStatus,
    StudyUser,
    User,
    UserFavorite,
    UserMeta,
    ZipCode,
    ChainStep,
    ExportInfo,
    AlternativeAugmentative,
    AssistiveDevice,
    ChainSession,
    ChallengingBehavior,
    ChainSessionStep,
    ChainQuestionnaire,
    ClinicalDiagnosesQuestionnaire,
    ContactQuestionnaire,
    CurrentBehaviorsDependentQuestionnaire,
    CurrentBehaviorsSelfQuestionnaire,
    DemographicsQuestionnaire,
    DevelopmentalQuestionnaire,
    EducationDependentQuestionnaire,
    EducationSelfQuestionnaire,
    EmploymentQuestionnaire,
    EvaluationHistoryDependentQuestionnaire,
    EvaluationHistorySelfQuestionnaire,
    HomeSelfQuestionnaire,
    HomeDependentQuestionnaire,
    IdentificationQuestionnaire,
    ProfessionalProfileQuestionnaire,
    RegistrationQuestionnaire,
    SupportsQuestionnaire,
    Therapy,
    Housemate,
    ResourceChangeLog,
    Medication,
    DataTransferLog,
    DataTransferLogDetail,
)

_category_list_url = lambda: URLFor("api.categorylistendpoint")
_category_self_url = lambda: URLFor("api.categoryendpoint", values={"id": "<id>"})
_category_url = lambda: URLFor("api.categoryendpoint", values={"id": "<category_id>"})
_event_category_self_url = lambda: URLFor("api.eventcategoryendpoint", values={"id": "<id>"})
_event_url = lambda: URLFor("api.eventendpoint", values={"id": "<resource_id>"})
_investigator_url = lambda: URLFor("api.investigatorendpoint", values={"id": "<investigator_id>"})
_location_category_self_url = lambda: URLFor("api.locationcategoryendpoint", values={"id": "<id>"})
_location_url = lambda: URLFor("api.locationendpoint", values={"id": "<resource_id>"})
_participant_self_url = lambda: URLFor("api.participantendpoint", values={"id": "<id>"})
_resource_category_self_url = lambda: URLFor("api.resourcecategoryendpoint", values={"id": "<id>"})
_resource_url = lambda: URLFor("api.resourceendpoint", values={"id": "<resource_id>"})
_study_category_self_url = lambda: URLFor("api.studycategoryendpoint", values={"id": "<id>"})
_study_investigator_self_url = lambda: URLFor("api.studyinvestigatorendpoint", values={"id": "<id>"})
_study_url = lambda: URLFor("api.studyendpoint", values={"id": "<study_id>"})
_study_user_self_url = lambda: URLFor("api.studyuserendpoint", values={"id": "<id>"})
_user_url = lambda: URLFor("api.userendpoint", values={"id": "<user_id>"})


def _questionnaire_url(name):
    return URLFor("api.questionnaireendpoint", values={"name": f"{name}", "id": "<id>"})


class ModelSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = session
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        include_fk = True
        ordered = True


class InvestigatorSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Investigator
        fields = ("id", "last_updated", "name", "title", "organization_name", "bio_link", "_links")

    _links = Hyperlinks(
        {
            "self": URLFor("api.investigatorendpoint", values={"id": "<id>"}),
            "collection": URLFor("api.investigatorlistendpoint"),
        }
    )


class ParentCategorySchema(ModelSchema):
    """Provides a view of the parent category, all the way to the top, but ignores children"""

    class Meta(ModelSchema.Meta):
        model = Category
        fields = ("id", "name", "parent", "level", "_links", "display_order")

    parent = Nested(lambda: ParentCategorySchema(), dump_only=True)
    level = Function(lambda obj: obj.calculate_level() if isinstance(obj, Category) else 0)
    _links = Hyperlinks(
        {
            "self": _category_self_url(),
            "collection": _category_list_url(),
        }
    )


class ChildCategoryInSearchSchema(ModelSchema):
    """Children within a category have hit counts when returned as a part of a search."""

    class Meta(ModelSchema.Meta):
        model = Category
        fields = ("id", "name", "_links", "hit_count", "display_order")

    _links = Hyperlinks(
        {
            "self": _category_self_url(),
            "collection": _category_list_url(),
        }
    )


class CategoryInSearchSchema(ModelSchema):
    """streamlined category representation for inclusion in search results to provide faceted search"""

    class Meta(ModelSchema.Meta):
        model = Category
        fields = ("id", "name", "children", "parent_id", "parent", "level", "display_order")

    parent_id = Number(required=False, allow_none=True)
    parent = Nested(lambda: ParentCategorySchema(), dump_only=True, required=False, allow_none=True)
    children = Nested(lambda: ChildCategoryInSearchSchema(), many=True, dump_only=True)
    level = Function(lambda obj: obj.calculate_level() if isinstance(obj, Category) else 0, dump_only=True)


class CategorySchema(ModelSchema):
    """Provides detailed information about a category, including all the children"""

    class Meta(ModelSchema.Meta):
        model = Category
        fields = (
            "id",
            "name",
            "children",
            "parent_id",
            "parent",
            "level",
            "event_count",
            "location_count",
            "resource_count",
            "all_resource_count",
            "study_count",
            "color",
            "_links",
            "last_updated",
            "display_order",
        )

    id = Integer(required=False, allow_none=True)
    parent_id = Integer(required=False, allow_none=True)
    children = Nested(lambda: CategorySchema(), many=True, dump_only=True, exclude=("parent", "color"))
    parent = Nested(lambda: ParentCategorySchema(), dump_only=True)
    level = Function(lambda obj: obj.calculate_level() if isinstance(obj, Category) else 0, dump_only=True)
    event_count = Method("get_event_count", dump_only=True)
    location_count = Method("get_location_count", dump_only=True)
    resource_count = Method("get_resource_count", dump_only=True)
    all_resource_count = Method("get_all_resource_count", dump_only=True)
    study_count = Method("get_study_count", dump_only=True)
    _links = Hyperlinks(
        {
            "self": _category_self_url(),
            "collection": _category_list_url(),
        }
    )

    def get_event_count(self, obj):
        if obj is None:
            return missing
        query = (
            session.query(ResourceCategory)
            .filter(ResourceCategory.type == "event")
            .filter(ResourceCategory.category_id == obj.id)
        )
        count_q = query.statement.with_only_columns(func.count()).order_by(None)
        return query.session.execute(count_q).scalar()

    def get_location_count(self, obj):
        if obj is None:
            return missing
        query = (
            session.query(ResourceCategory)
            .filter(ResourceCategory.type == "location")
            .filter(ResourceCategory.category_id == obj.id)
        )
        count_q = query.statement.with_only_columns(func.count()).order_by(None)
        return query.session.execute(count_q).scalar()

    def get_resource_count(self, obj):
        if obj is None:
            return missing
        query = (
            session.query(ResourceCategory)
            .filter(ResourceCategory.type == "resource")
            .filter(ResourceCategory.category_id == obj.id)
        )
        count_q = query.statement.with_only_columns(func.count()).order_by(None)
        return query.session.execute(count_q).scalar()

    def get_all_resource_count(self, obj):
        if obj is None:
            return missing
        query = (
            session.query(ResourceCategory)
            .join(ResourceCategory.resource)
            .filter(ResourceCategory.category_id == obj.id)
        )
        count_q = query.statement.with_only_columns(func.count()).order_by(None)
        return query.session.execute(count_q).scalar()

    def get_study_count(self, obj):
        if obj is None:
            return missing
        query = session.query(StudyCategory).join(StudyCategory.study).filter(StudyCategory.category_id == obj.id)
        count_q = query.statement.with_only_columns(func.count()).order_by(None)
        return query.session.execute(count_q).scalar()


class CategoryUpdateSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Category
        fields = ("id", "name", "parent_id", "display_order", "hit_count")

    # id = Integer(required=True, allow_none=False)
    # parent_id = Integer(required=False, allow_none=True)
    # display_order = Integer(required=False)
    # name = String(required=False, allow_none=False)
    # hit_count = Integer(required=False)


class CategoriesOnEventSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id", "category")

    category = Nested(lambda: ParentCategorySchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _event_category_self_url(),
            "category": _category_url(),
            "event": _event_url(),
        }
    )


class CategoriesOnLocationSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id", "category")

    category = Nested(lambda: ParentCategorySchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _location_category_self_url(),
            "category": _category_url(),
            "location": _location_url(),
        }
    )


class CategoriesOnResourceSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id", "category")

    category = Nested(lambda: ParentCategorySchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _resource_category_self_url(),
            "category": _category_url(),
            "resource": _resource_url(),
        }
    )


class CategoriesOnStudySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyCategory
        fields = ("id", "_links", "study_id", "category_id", "category")

    category = Nested(lambda: ParentCategorySchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _study_category_self_url(),
            "category": _category_url(),
            "study": _study_url(),
        }
    )


class InvestigatorsOnStudySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyInvestigator
        fields = ("id", "_links", "study_id", "investigator_id", "investigator")

    investigator = Nested(lambda: InvestigatorSchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _study_investigator_self_url(),
            "investigator": _investigator_url(),
            "study": _study_url(),
        }
    )


class ResourceSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Resource
        fields = (
            "id",
            "type",
            "title",
            "last_updated",
            "description",
            "organization_name",
            "phone",
            "website",
            "contact_email",
            "video_code",
            "is_uva_education_content",
            "resource_categories",
            "is_draft",
            "ages",
            "insurance",
            "phone_extension",
            "languages",
            "covid19_categories",
            "should_hide_related_resources",
            "_links",
        )

    resource_categories = Nested(lambda: CategoriesOnResourceSchema(), many=True, dump_only=True)
    _links = Hyperlinks(
        {
            "self": URLFor("api.resourceendpoint", values={"id": "<id>"}),
            "collection": URLFor("api.resourcelistendpoint"),
            "categories": URLFor("api.categorybyresourceendpoint", values={"resource_id": "<id>"}),
        }
    )


class ResourceCategoriesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id", "category")

    category = Nested(lambda: CategorySchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _resource_category_self_url(),
            "category": _category_url(),
            "resource": _resource_url(),
        }
    )


class CategoryResourcesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id", "resource")

    resource = Nested(lambda: ResourceSchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _resource_category_self_url(),
            "category": _category_url(),
            "resource": _resource_url(),
        }
    )


class ResourceCategorySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id", "type")

    _links = Hyperlinks(
        {
            "self": _resource_category_self_url(),
            "category": _category_url(),
            "resource": _resource_url(),
        }
    )


class EventUserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EventUser
        fields = ("id", "last_updated", "event_id", "event", "user_id", "user")

    event_id = Integer(required=False, allow_none=True)
    user_id = Integer(required=False, allow_none=True)
    event = Nested(lambda: ResourceSchema(), dump_only=True)
    user = Nested(lambda: CategorySchema(), dump_only=True)


class EventSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Event
        fields = (
            "id",
            "type",
            "title",
            "last_updated",
            "description",
            "date",
            "time",
            "ticket_cost",
            "primary_contact",
            "location_name",
            "street_address1",
            "street_address2",
            "city",
            "state",
            "zip",
            "phone",
            "website",
            "contact_email",
            "video_code",
            "is_uva_education_content",
            "is_draft",
            "organization_name",
            "resource_categories",
            "latitude",
            "longitude",
            "ages",
            "insurance",
            "phone_extension",
            "languages",
            "covid19_categories",
            "includes_registration",
            "webinar_link",
            "post_survey_link",
            "max_users",
            "registered_users",
            "image_url",
            "registration_url",
            "should_hide_related_resources",
            "post_event_description",
            "_links",
        )

    id = Integer(required=False, allow_none=True)
    resource_categories = Nested(lambda: CategoriesOnEventSchema(), many=True, dump_only=True)
    registered_users = Nested(lambda: EventUserSchema(), many=True, dump_only=True)
    _links = Hyperlinks(
        {
            "self": URLFor("api.eventendpoint", values={"id": "<id>"}),
            "collection": URLFor("api.eventlistendpoint"),
            "categories": URLFor("api.categorybyeventendpoint", values={"event_id": "<id>"}),
        }
    )


class EventCategoriesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id", "category")

    category = Nested(lambda: CategorySchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _event_category_self_url(),
            "category": _category_url(),
            "event": _event_url(),
        }
    )


class CategoryEventsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id", "resource")

    resource = Nested(lambda: EventSchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _event_category_self_url(),
            "category": _category_url(),
            "event": _event_url(),
        }
    )


class EventCategorySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id")

    _links = Hyperlinks(
        {
            "self": _event_category_self_url(),
            "category": _category_url(),
            "event": _event_url(),
        }
    )


class LocationSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Location
        fields = (
            "id",
            "type",
            "title",
            "last_updated",
            "description",
            "primary_contact",
            "street_address1",
            "street_address2",
            "city",
            "state",
            "zip",
            "phone",
            "email",
            "website",
            "contact_email",
            "video_code",
            "is_uva_education_content",
            "organization_name",
            "resource_categories",
            "latitude",
            "longitude",
            "_links",
            "ages",
            "insurance",
            "phone_extension",
            "languages",
            "covid19_categories",
            "is_draft",
            "should_hide_related_resources",
        )

    id = Integer(required=False, allow_none=True)
    resource_categories = Nested(lambda: CategoriesOnLocationSchema(), many=True, dump_only=True)
    _links = Hyperlinks(
        {
            "self": URLFor("api.locationendpoint", values={"id": "<id>"}),
            "collection": URLFor("api.locationlistendpoint"),
        }
    )


class LocationCategoriesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id", "category")

    category = Nested(lambda: CategorySchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _location_category_self_url(),
            "category": _category_url(),
            "location": _location_url(),
        }
    )


class CategoryLocationsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id", "resource")

    resource = Nested(lambda: LocationSchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _location_category_self_url(),
            "category": _category_url(),
            "location": _location_url(),
        }
    )


class LocationCategorySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceCategory
        fields = ("id", "_links", "resource_id", "category_id")

    _links = Hyperlinks(
        {
            "self": _location_category_self_url(),
            "category": _category_url(),
            "location": _location_url(),
        }
    )


class ParticipantSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Participant
        fields = (
            "id",
            "_links",
            "last_updated",
            "name",
            "relationship",
            "user_id",
            "avatar_icon",
            "avatar_color",
            "has_consented",
            "contact",
            "identification",
            "percent_complete",
        )

    id = Integer(required=False, allow_none=True)
    name = Function(lambda obj: missing if obj is None else obj.get_name())
    relationship = Enum(Relationship)
    user_id = Integer(required=False, allow_none=True)
    percent_complete = Function(lambda obj: missing if obj is None else obj.get_percent_complete())
    contact = Nested(lambda: ContactQuestionnaireSchema(), dump_only=True)
    identification = Nested(lambda: IdentificationQuestionnaireSchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _participant_self_url(),
            "user": _user_url(),
        }
    )


class UserFavoriteSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = UserFavorite
        fields = (
            "id",
            "last_updated",
            "type",
            "user_id",
            "resource_id",
            "resource",
            "category_id",
            "category",
            "age_range",
            "language",
            "covid19_category",
        )

    resource_id = Integer(required=False, allow_none=True)
    category_id = Integer(required=False, allow_none=True)
    resource = Nested(lambda: ResourceSchema(), dump_only=True)
    category = Nested(lambda: CategorySchema(), dump_only=True)


class UserMetaSchema(ModelSchema):
    self_relationship = Function(lambda obj: obj.get_relationship(), allow_none=True)

    class Meta(ModelSchema.Meta):
        model = UserMeta
        # load_instance = True
        # sqla_session = session
        fields = (
            "id",
            "last_updated",
            "self_participant",
            "self_has_guardian",
            "professional",
            "interested",
            "guardian",
            "guardian_has_dependent",
            "self_relationship",
        )

    self_participant = Boolean(required=False, allow_none=True)
    self_has_guardian = Boolean(required=False, allow_none=True)
    professional = Boolean(required=False, allow_none=True)
    interested = Boolean(required=False, allow_none=True)
    guardian = Boolean(required=False, allow_none=True)
    guardian_has_dependent = Boolean(required=False, allow_none=True)


class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        fields = (
            "id",
            "last_updated",
            "registration_date",
            "last_login",
            "email",
            "password",
            "role",
            "permissions",
            "participants",
            "token",
            "token_url",
            "user_favorites",
            "user_meta",
            "participant_count",
            "created_password",
            "identity",
            "percent_self_registration_complete",
            "email_verified",
        )

    password = String(load_only=True)
    participants = Nested(lambda: ParticipantSchema(), dump_only=True, many=True)
    participant_count = Integer(required=False, allow_none=True)
    user_favorites = Nested(lambda: UserFavoriteSchema(), dump_only=True, many=True)
    user_meta = Nested(lambda: UserMetaSchema(), dump_only=True)
    id = Integer(required=False, allow_none=True)
    role = Enum(Role)
    permissions = Method("get_permissions", dump_only=True)
    percent_self_registration_complete = Function(
        lambda obj: missing if obj is None else obj.percent_self_registration_complete(), dump_only=True
    )
    created_password = Function(lambda obj: missing if obj is None else obj.created_password(), dump_only=True)
    identity = Function(lambda obj: missing if obj is None else obj.identity(), dump_only=True)

    def get_permissions(self, obj):
        if obj is None:
            return missing
        permissions = []
        for p in obj.role.permissions():
            permissions.append(p.name)
        return permissions


class UsersOnStudySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyUser
        fields = ("id", "_links", "status", "study_id", "user_id", "user")

    user = Nested(lambda: UserSchema(), dump_only=True)
    status = Enum(StudyUserStatus, allow_none=True)
    _links = Hyperlinks(
        {
            "self": _study_user_self_url(),
            "user": _user_url(),
            "study": _study_url(),
        }
    )


class StudyUsersSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyUser
        fields = ("id", "_links", "status", "study_id", "user_id", "user")

    user = Nested(lambda: UserSchema(), dump_only=True)
    status = Enum(StudyUserStatus, allow_none=True)
    _links = Hyperlinks(
        {
            "self": _study_user_self_url(),
            "user": _user_url(),
            "study": _study_url(),
        }
    )


class StudyUserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyUser
        fields = ("id", "_links", "status", "study_id", "user_id")

    status = Enum(StudyUserStatus, allow_none=True)
    _links = Hyperlinks(
        {
            "self": _study_user_self_url(),
            "user": _user_url(),
            "study": _study_url(),
        }
    )


class StudySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Study
        fields = (
            "id",
            "title",
            "short_title",
            "short_description",
            "image_url",
            "last_updated",
            "description",
            "participant_description",
            "benefit_description",
            "coordinator_email",
            "organization_name",
            "location",
            "status",
            "study_categories",
            "study_investigators",
            "eligibility_url",
            "survey_url",
            "results_url",
            "ages",
            "languages",
            "num_visits",
            "_links",
        )

    status = Enum(Status)
    study_categories = Nested(lambda: CategoriesOnStudySchema(), many=True, dump_only=True)
    study_investigators = Nested(lambda: InvestigatorsOnStudySchema(), many=True, dump_only=True)
    _links = Hyperlinks(
        {
            "self": URLFor("api.studyendpoint", values={"id": "<id>"}),
            "collection": URLFor("api.studylistendpoint"),
            "categories": URLFor("api.categorybystudyendpoint", values={"study_id": "<id>"}),
        }
    )


class UserStudiesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyUser
        fields = ("id", "_links", "status", "study_id", "user_id", "study")

    study = Nested(lambda: StudySchema(), dump_only=True)
    status = Enum(StudyUserStatus, allow_none=True)
    _links = Hyperlinks(
        {
            "self": _study_user_self_url(),
            "user": _user_url(),
            "study": _study_url(),
        }
    )


class StudyCategoriesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyCategory
        fields = ("id", "_links", "study_id", "category_id", "category")

    category = Nested(lambda: CategorySchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _study_category_self_url(),
            "category": _category_url(),
            "study": _study_url(),
        }
    )


class CategoryStudiesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyCategory
        fields = ("id", "_links", "study_id", "category_id", "study")

    study = Nested(lambda: StudySchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _study_category_self_url(),
            "category": _category_url(),
            "study": _study_url(),
        }
    )


class StudyCategorySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyCategory
        fields = ("id", "_links", "study_id", "category_id")

    _links = Hyperlinks(
        {
            "self": _study_category_self_url(),
            "category": _category_url(),
            "study": _study_url(),
        }
    )


class StudyInvestigatorsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyInvestigator
        fields = ("id", "_links", "study_id", "investigator_id", "investigator")

    investigator = Nested(lambda: InvestigatorSchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _study_investigator_self_url(),
            "investigator": _investigator_url(),
            "study": _study_url(),
        }
    )


class InvestigatorStudiesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyInvestigator
        fields = ("id", "_links", "study_id", "investigator_id", "study")

    study = Nested(lambda: StudySchema(), dump_only=True)
    _links = Hyperlinks(
        {
            "self": _study_investigator_self_url(),
            "investigator": _investigator_url(),
            "study": _study_url(),
        }
    )


class StudyInvestigatorSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StudyInvestigator
        fields = ("id", "_links", "study_id", "investigator_id")

    _links = Hyperlinks(
        {
            "self": _study_investigator_self_url(),
            "investigator": _investigator_url(),
            "study": _study_url(),
        }
    )


class GeopointSchema(Schema):
    lat = Float(missing=None)
    lon = Float(missing=None)

    @post_load
    def make_geo_point(self, data, **kwargs):
        return Geopoint(**data)


class SearchSchema(Schema):
    class Meta(ModelSchema.Meta):
        unknown = EXCLUDE

    class HitSchema(Schema):
        id = Integer()
        content = Str(missing=None)
        description = Str(missing=None)
        post_event_description = Str(missing=None)
        title = Str(missing=None)
        type = Str()
        label = Str(missing=None)
        last_updated = DateTime(missing=None)
        highlights = Str(missing=None)
        latitude = Float()
        longitude = Float()
        date = DateTime(missing=None)
        status = Str(missing=None)
        no_address = Boolean(missing=None)
        is_draft = Boolean(missing=None)

    class SortSchema(Schema):
        field = Str(allow_null=True)
        latitude = Float(missing=None)
        longitude = Float(missing=None)
        order = Str(missing="asc")
        unit = Str(missing="mi")

        @post_load
        def make_sort(self, data, **kwargs):
            return Sort(**data)

    class AggCountSchema(Schema):
        value = String()
        count = Integer()
        is_selected = Boolean()

    class GeoboxSchema(Schema):
        top_left = Nested(lambda: GeopointSchema())
        bottom_right = Nested(lambda: GeopointSchema())

        @post_load
        def make_geo_box(self, data, **kwargs):
            return Geobox(**data)

    words = Str()
    start = Integer()
    size = Integer()
    sort = Nested(lambda: SearchSchema.SortSchema(), allow_none=True, default=None)
    types = List(Str())
    ages = List(Str())
    languages = List(Str())
    age_counts = List(Nested(lambda: SearchSchema.AggCountSchema()), dump_only=True)
    language_counts = List(Nested(lambda: SearchSchema.AggCountSchema()), dump_only=True)
    type_counts = List(Nested(lambda: SearchSchema.AggCountSchema()), dump_only=True)
    total = Integer(dump_only=True)
    hits = Nested(lambda: SearchSchema.HitSchema(), many=True, dump_only=True)
    category = Nested(lambda: CategoryInSearchSchema())
    ordered = True
    date = DateTime(allow_none=True)
    map_data_only = Boolean()
    geo_box = Nested(lambda: SearchSchema.GeoboxSchema(), allow_none=True, default=None)

    @post_load
    def make_search(self, data, **kwargs):
        return Search(**data)


class UserSearchSchema(Schema):
    pages = Integer()
    total = Integer()
    items = List(Nested(lambda: UserSchema()))


class StepSchema(Schema):
    name = Str()
    type = Str()
    label = Str()
    status = Str()
    date_completed = DateTime()
    questionnaire_id = Integer()


class FlowSchema(Schema):
    name = Str()
    steps = Nested(lambda: StepSchema(), many=True)


# class EmailLogSchema(ModelSchema):
#     class Meta(ModelSchema.Meta):
#         model = EmailLog


class ResourceChangeLogSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ResourceChangeLog


class AdminNoteSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = AdminNote
        fields = ("id", "resource_id", "user_id", "resource", "user", "last_updated", "note")

    user = Nested(lambda: UserSchema(), dump_only=True)
    resource = Nested(lambda: ResourceSchema(), dump_only=True)


class StepLogSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = StepLog


class ZipCodeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ZipCode
        fields = ["id", "latitude", "longitude"]


class ChainStepSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ChainStep
        fields = ["id", "name", "instruction", "last_updated"]


class ExportSchemas:
    """
    Provides specialized schemas to use during export and import to
    a mirrored system.  Define classes here as XXXExportSchema and they will be
    picked up by the ExportService and used automatically. If not defined here,
    the Export Service will first fall back to using a schema XXXSchema defined in
    the same module as the class to be marshaled. If this does not exist, it will
    check for a schema elsewhere in this file.
    """

    class UserExportSchema(ModelSchema):
        """Used exclusively for data export, removes identifying information"""

        class Meta(ModelSchema.Meta):
            model = User
            fields = ("id", "last_updated", "role", "email_verified", "email", "_links")

        role = Enum(Role)
        email = Function(lambda obj: missing if obj is None else str(obj.id))
        _links = Hyperlinks(
            {
                "self": URLFor("api.userendpoint", values={"id": "<id>"}),
            }
        )

    class AdminExportSchema(ModelSchema):
        """Allows the full details of an admin account to be exported, so that administrators
        can continue to log into the secondary private server with their normal credentials."""

        class Meta(ModelSchema.Meta):
            model = User
            fields = ("id", "last_updated", "email", "_password", "role", "participants", "token", "email_verified")

        role = Enum(Role)

    class ParticipantExportSchema(ModelSchema):
        """Used exclusively for data export, removes identifying information"""

        class Meta(ModelSchema.Meta):
            model = Participant
            fields = ("id", "last_updated", "user_id", "relationship", "avatar_icon", "avatar_color", "_links")

        relationship = Enum(Relationship)
        _links = Hyperlinks(
            {
                "self": _participant_self_url(),
            }
        )


class EmailLogSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EmailLog


class ExportInfoSchema(Schema):
    class Meta:
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        include_fk = True
        ordered = True
        fields = ["table_name", "class_name", "display_name", "size", "url", "question_type", "sub_tables"]

    sub_tables = Nested(lambda: ExportInfoSchema(), default=None, many=True, dump_only=True)
    display_name = String(dump_only=True)

    @post_load
    def make_info(self, data, **kwargs):
        return ExportInfo(**data)


class FrontendConfigSchema(Schema):
    class Meta:
        ordered = True
        fields = ["development", "testing", "mirroring", "production", "apiUrl", "apiKey", "googleAnalyticsKey"]


class AlternativeAugmentativeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = AlternativeAugmentative
        fields = (
            "id",
            "last_updated",
            "supports_questionnaire_id",
            "type",
            "type_other",
            "timeframe",
            "notes",
            "participant_id",
            "user_id",
        )

    participant_id = Method("get_participant_id", dump_only=True)
    user_id = Method("get_user_id", dump_only=True)

    def get_participant_id(self, obj):
        if obj is None:
            return missing
        return obj.supports_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing
        return obj.supports_questionnaire.user_id


class AssistiveDeviceSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = AssistiveDevice
        fields = (
            "id",
            "last_updated",
            "supports_questionnaire_id",
            "type_group",
            "type",
            "type_other",
            "timeframe",
            "notes",
            "participant_id",
            "user_id",
        )

    participant_id = Method("get_participant_id", dump_only=True)
    user_id = Method("get_user_id", dump_only=True)

    def get_participant_id(self, obj):
        if obj is None:
            return missing
        return obj.supports_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing
        return obj.supports_questionnaire.user_id


class ChainSessionSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields["step_attempts"].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = ChainSession
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "date",
            "completed",
            "session_type",
            "session_number",
            "chain_questionnaire_id",
            "step_attempts",
        )

    step_attempts = Nested(lambda: ChainSessionStepSchema(), many=True)
    participant_id = Method("get_participant_id", dump_only=True)
    user_id = Method("get_user_id", dump_only=True)
    session_number = Method("get_session_number", dump_only=True)

    def get_participant_id(self, obj):
        if obj is None:
            return missing

        return obj.chain_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing

        return obj.chain_questionnaire.user_id

    def get_session_number(self, obj):
        if obj is None:
            return missing

        # Sort sessions by date
        sorted_sessions = sorted(obj.chain_questionnaire.sessions, key=lambda k: k.date)

        # Find this session and return its index, incremented.
        for i, session in enumerate(sorted_sessions):
            if obj.id == session.id:
                return i + 1

        # Session not found.
        return -1


class ChallengingBehaviorSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ChallengingBehavior
        fields = ("id", "last_updated", "chain_session_step_id", "time")


class ChainSessionStepSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ChainSessionStep
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "chain_session_id",
            "chain_step_id",
            "date",
            "session_type",
            "was_focus_step",
            "target_prompt_level",
            "status",
            "completed",
            "was_prompted",
            "prompt_level",
            "had_challenging_behavior",
            "reason_step_incomplete",
            "session_number",
            "num_stars",
            "challenging_behaviors",
            "chain_step",
        )

    participant_id = Method("get_participant_id", dump_only=True)
    user_id = Method("get_user_id", dump_only=True)
    challenging_behaviors = Nested(lambda: ChallengingBehaviorSchema(), many=True)
    chain_step = Method("get_chain_step", dump_only=True)
    session_type = Method("get_session_type", dump_only=True)
    session_number = Method("get_session_number", dump_only=True)

    def get_chain_step(self, obj):
        if obj is None:
            return missing

        db_chain_step = session.query(ChainStep).filter_by(id=obj.chain_step_id).first()
        return ChainStepSchema().dump(db_chain_step)

    def get_session_type(self, obj):
        if obj is None:
            return missing

        return obj.chain_session.session_type

    def get_session_number(self, obj):
        if obj is None:
            return missing

        # Sort sessions by date
        sorted_sessions = sorted(obj.chain_session.chain_questionnaire.sessions, key=lambda k: k.date)

        # Find this session and return its index, incremented.
        for i, session in enumerate(sorted_sessions):
            if obj.chain_session.id == session.id:
                return i + 1

        # Session not found.
        return -1

    def get_participant_id(self, obj):
        if obj is None:
            return missing

        return obj.chain_session.chain_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing

        return obj.chain_session.chain_questionnaire.user_id


class ChainQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields["sessions"].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = ChainQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "sessions",
        )

    sessions = Nested(lambda: ChainSessionSchema(), many=True)


class ClinicalDiagnosesQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ClinicalDiagnosesQuestionnaire

        include_fk = True

    _links = Hyperlinks({"self": _questionnaire_url("clinical_diagnoses_questionnaire")})


class ContactQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ContactQuestionnaire

    _links = Hyperlinks({"self": _questionnaire_url("contact_questionnaire")})


class CurrentBehaviorsDependentQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CurrentBehaviorsDependentQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "dependent_verbal_ability",
            "concerning_behaviors",
            "concerning_behaviors_other",
            "has_academic_difficulties",
            "academic_difficulty_areas",
            "academic_difficulty_other",
            "_links",
        )

    _links = Hyperlinks(
        {
            "self": _questionnaire_url("current_behaviors_dependent_questionnaire"),
        }
    )


class CurrentBehaviorsSelfQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CurrentBehaviorsSelfQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "self_verbal_ability",
            "has_academic_difficulties",
            "academic_difficulty_areas",
            "academic_difficulty_other",
            "_links",
        )

    _links = Hyperlinks(
        {
            "self": _questionnaire_url("current_behaviors_dependent_questionnaire"),
        }
    )


class DemographicsQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = DemographicsQuestionnaire

    _links = Hyperlinks({"self": _questionnaire_url("demographics_questionnaire")})


class DevelopmentalQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = DevelopmentalQuestionnaire

    _links = Hyperlinks(
        {
            "self": _questionnaire_url("developmental_questionnaire"),
        }
    )


class EducationDependentQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EducationDependentQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "attends_school",
            "school_name",
            "school_type",
            "dependent_placement",
            "placement_other",
            "current_grade",
            "school_services",
            "school_services_other",
        )


class EducationSelfQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EducationSelfQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "attends_school",
            "school_name",
            "school_type",
            "self_placement",
            "placement_other",
            "current_grade",
            "school_services",
            "school_services_other",
        )


class EmploymentQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EmploymentQuestionnaire

    _links = Hyperlinks(
        {
            "self": _questionnaire_url("employment_questionnaire"),
        }
    )


class EvaluationHistoryDependentQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EvaluationHistoryDependentQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "self_identifies_autistic",
            "has_autism_diagnosis",
            "years_old_at_first_diagnosis",
            "who_diagnosed",
            "who_diagnosed_other",
            "where_diagnosed",
            "where_diagnosed_other",
            "partner_centers_evaluation",
            "gives_permission_to_link_evaluation_data",
            "has_iq_test",
            "recent_iq_score",
            "_links",
        )

    _links = Hyperlinks(
        {
            "self": _questionnaire_url("evaluation_history_dependent_questionnaire"),
        }
    )


class EvaluationHistorySelfQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EvaluationHistorySelfQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "self_identifies_autistic",
            "has_autism_diagnosis",
            "years_old_at_first_diagnosis",
            "who_diagnosed",
            "who_diagnosed_other",
            "where_diagnosed",
            "where_diagnosed_other",
            "partner_centers_evaluation",
            "gives_permission_to_link_evaluation_data",
            "has_iq_test",
            "recent_iq_score",
            "_links",
        )

    _links = Hyperlinks(
        {
            "self": _questionnaire_url("evaluation_history_self_questionnaire"),
        }
    )


class HomeSelfQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields["housemates"].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = HomeSelfQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "self_living_situation",
            "self_living_other",
            "housemates",
            "struggle_to_afford",
        )

    housemates = Nested(lambda: HousemateSchema(), many=True)


class HomeDependentQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields["housemates"].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = HomeDependentQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "dependent_living_situation",
            "dependent_living_other",
            "housemates",
            "struggle_to_afford",
        )

    housemates = Nested(lambda: HousemateSchema(), many=True)


class IdentificationQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = IdentificationQuestionnaire

    _links = Hyperlinks({"self": _questionnaire_url("identification_questionnaire")})


class ProfessionalProfileQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ProfessionalProfileQuestionnaire

    _links = Hyperlinks(
        {
            "self": _questionnaire_url("professional_profile_questionnaire"),
        }
    )


class RegistrationQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = RegistrationQuestionnaire
        ordered = True
        include_fk = True

    _links = Hyperlinks(
        {
            "self": _questionnaire_url("registration_questionnaire"),
        }
    )


class SupportsQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields["medications"].schema.session = self.session
        self.fields["therapies"].schema.session = self.session
        self.fields["alternative_augmentative"].schema.session = self.session
        self.fields["assistive_devices"].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = SupportsQuestionnaire
        fields = (
            "id",
            "last_updated",
            "time_on_task_ms",
            "participant_id",
            "user_id",
            "medications",
            "therapies",
            "assistive_devices",
            "alternative_augmentative",
            "_links",
        )

    medications = Nested(lambda: MedicationSchema(), many=True)
    therapies = Nested(lambda: TherapySchema(), many=True)
    assistive_devices = Nested(lambda: AssistiveDeviceSchema(), many=True)
    alternative_augmentative = Nested(lambda: AlternativeAugmentativeSchema(), many=True)
    _links = Hyperlinks(
        {
            "self": _questionnaire_url("supports_questionnaire"),
        }
    )


class TherapySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Therapy
        fields = (
            "id",
            "last_updated",
            "supports_questionnaire_id",
            "type",
            "type_other",
            "timeframe",
            "notes",
            "participant_id",
            "user_id",
        )

    participant_id = Method("get_participant_id", dump_only=True)
    user_id = Method("get_user_id", dump_only=True)

    def get_participant_id(self, obj):
        if obj is None:
            return missing
        return obj.supports_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing
        return obj.supports_questionnaire.user_id


class HousemateSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Housemate
        fields = (
            "id",
            "last_updated",
            "home_dependent_questionnaire_id",
            "home_self_questionnaire_id",
            "name",
            "relationship",
            "relationship_other",
            "age",
            "has_autism",
            "participant_id",
            "user_id",
        )

    participant_id = Method("get_participant_id")
    user_id = Method("get_user_id")
    home_dependent_questionnaire_id = Integer(required=False, allow_none=True)
    home_self_questionnaire_id = Integer(required=False, allow_none=True)
    home_dependent_questionnaire = Nested(lambda: HomeDependentQuestionnaireSchema(), required=False, allow_none=True)
    home_self_questionnaire = Nested(lambda: HomeSelfQuestionnaireSchema(), required=False, allow_none=True)

    def get_participant_id(self, obj):
        if obj is None:
            return missing
        elif obj.home_dependent_questionnaire is not None:
            return obj.home_dependent_questionnaire.participant_id
        elif obj.home_self_questionnaire is not None:
            return obj.home_self_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing
        elif obj.home_dependent_questionnaire is not None:
            return obj.home_dependent_questionnaire.user_id
        elif obj.home_self_questionnaire is not None:
            return obj.home_self_questionnaire.user_id


class MedicationSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Medication
        fields = (
            "id",
            "last_updated",
            "supports_questionnaire_id",
            "symptom",
            "symptom_other",
            "name",
            "notes",
            "participant_id",
            "user_id",
        )

    participant_id = Method("get_participant_id", dump_only=True)
    user_id = Method("get_user_id", dump_only=True)

    def get_participant_id(self, obj):
        if obj is None:
            return missing
        return obj.supports_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing
        return obj.supports_questionnaire.user_id


class DataTransferLogDetailSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = DataTransferLogDetail


class DataTransferLogSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = DataTransferLog
        fields = ("id", "type", "date_started", "last_updated", "total_records", "alerts_sent", "details", "_links")

    details = Nested(lambda: DataTransferLogDetailSchema(), dump_only=True, many=True)
    _links = Hyperlinks({"self": URLFor("api.datatransferlogendpoint", values={"id": "<id>"})})


class DataTransferLogPageSchema(Schema):
    pages = Integer()
    total = Integer()
    items = List(Nested(lambda: DataTransferLogSchema()))
