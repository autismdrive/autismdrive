import copy
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Literal, Union, TypedDict

import googlemaps
import jwt
from sqlalchemy import ForeignKey, TEXT, func, ARRAY, select, Integer, Boolean, String, cast
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref, column_property, declared_attr, joinedload

from app.auth import bcrypt, password_requirements
from app.database import Base, session, random_integer, get_class
from app.enums import Relationship, Status, Role, StudyUserStatus
from app.export_service import ExportService
from app.utils import pascal_case_it
from config.load import settings


class QuestionnaireMixin(object):
    """Basically a hack to quickly get all the questionnaires in the system"""

    pass


class GeoPointType(TypedDict):
    lat: float
    lon: float


class GeoBoxType(TypedDict):
    top_left: GeoPointType
    bottom_right: GeoPointType


class AdminNote(Base):
    __tablename__ = "admin_note"
    id: Mapped[int] = mapped_column(primary_key=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resource.id"))
    resource: Mapped["Resource"] = relationship(back_populates="admin_notes", lazy="joined")
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    user: Mapped["User"] = relationship(back_populates="admin_notes", lazy="joined")
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    note: Mapped[str]


class AgeRange:
    """
    This class gives us a single location to define the order of age ranges
    and provides utilities for converting some of the bad data from CSV files
    around Ages into something consistent.
    """

    ages = ["pre-k", "school", "transition", "adult", "aging"]

    age_map = {
        "pre-k (0 - 5 years)": ["pre-k"],
        "school age (6 - 13 years)": ["school"],
        "transition age(14 - 22 years)": ["transition"],
        "transition age (14 - 22 years)": ["transition"],
        "adulthood (23 - 64)": ["adult"],
        "aging(65 +)": ["aging"],
        "aging (65+)": ["aging"],
        "pre-k": ["pre-k"],
        "school": ["school"],
        "transition": ["transition"],
        "adult": ["adult"],
        "aging": ["aging"],
        "childhood(0 - 13 years)": ["pre-k", "school"],
        "childhood (0 - 13 years)": ["pre-k", "school"],
        "all ages": ages,
    }

    @staticmethod
    def get_age_range_for_csv_data(bad_age):
        clean_age = bad_age.lower().strip()
        if clean_age in AgeRange.age_map.keys():
            return AgeRange.age_map[clean_age]
        else:
            raise Exception('Unknown age range:"' + bad_age + '" see Age Range Class to fix it.')


class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    display_order: Mapped[Optional[int]]
    parent: Mapped["Category"] = relationship(back_populates="children", remote_side=[id])
    children: Mapped[list["Category"]] = relationship(
        back_populates="parent", order_by="Category.display_order,Category.name"
    )
    hit_count: Mapped[Optional[int]] = mapped_column(default=0)  # when returning categories in the context of a search.
    resources: Mapped[list["Resource"]] = relationship(
        secondary="resource_category", back_populates="categories", viewonly=True
    )
    category_resources: Mapped[list["ResourceCategory"]] = relationship(back_populates="category")
    studies: Mapped[list["Study"]] = relationship(
        secondary="study_category", back_populates="categories", viewonly=True
    )
    category_studies: Mapped[list["StudyCategory"]] = relationship(back_populates="category")

    def calculate_level(self):
        """Provide the depth of the category"""
        level = 0
        cat = self
        while cat.parent and isinstance(cat, Category):
            level = level + 1
            cat = cat.parent
        return level

    # Returns an array of paths that should be used to search for
    # this category. , for instance "animals,cats,smelly-cats" would return
    # an array of three paths: ["animal", "animal,cats" and "animal,cats,smelly-cats"
    # but using the id of the category, not the name.
    def all_search_paths(self):
        cat = self
        paths = [cat.search_path()]
        while cat.parent:
            cat = cat.parent
            paths.append(cat.search_path())
        return paths

    def search_path(self) -> str:
        cat = self
        path = str(cat.id)
        while cat.parent and cat.parent.id:
            cat = cat.parent
            path = str(cat.id) + "," + path
        return path


class ChainStep(Base):
    __tablename__ = "chain_step"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    instruction: Mapped[str]
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


DataTransferLogType = Literal["importing", "exporting"]


class DataTransferLog(Base):
    """Records the action of a data transfer - So long as the number of records to be
    transferred is 0, this log is updated with a last_attempt rather than creating a new log."""

    __tablename__ = "data_transfer_log"
    __no_export__ = True  # Don't export this logging information.
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[DataTransferLogType] = mapped_column(default="exporting")  # Either importing or exporting
    date_started: Mapped[datetime] = mapped_column(default=func.now())
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now())
    total_records: Mapped[int] = mapped_column(default=0)
    alerts_sent: Mapped[int] = mapped_column(default=0)
    details: Mapped[list["DataTransferLogDetail"]] = relationship(back_populates="data_transfer_log")

    def successful(self):
        return next((x for x in self.details if not x.successful), None) is None


class DataTransferLogDetail(Base):
    """
    When data is successfully transferred, it is recorded in the detail log,
    which contains one record per class that is transferred.
    """

    __tablename__ = "data_transfer_log_detail"
    __no_export__ = True  # Don't export this logging information.
    id: Mapped[int] = mapped_column(primary_key=True)
    data_transfer_log_id: Mapped[int] = mapped_column(ForeignKey("data_transfer_log.id"))
    date_started: Mapped[datetime] = mapped_column(default=func.now())
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    class_name: Mapped[str] = mapped_column(default="")
    successful: Mapped[bool] = mapped_column(default=False)
    success_count: Mapped[int] = mapped_column(default=0)
    failure_count: Mapped[int] = mapped_column(default=0)
    errors = mapped_column(TEXT, default="")
    data_transfer_log: Mapped["DataTransferLog"] = relationship(back_populates="details")

    def handle_failure(self, error):
        if not self.errors:
            self.errors = ""
        self.errors += str(error)
        self.failure_count += 1
        self.successful = False

    def handle_success(self):
        self.success_count += 1


class EmailLog(Base):
    __tablename__ = "email_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    type: Mapped[str]
    tracking_code: Mapped[str]
    viewed: Mapped[bool] = mapped_column(default=False)
    date_viewed: Mapped[datetime] = mapped_column(default=func.now())
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


def _category_names(obj: Union["Resource", "Study"]):
    cat_text = ""
    for cat in obj.categories:
        cat_text = cat_text + " " + cat.name

    fields = ["ages", "languages", "covid19_categories"]

    for field in fields:
        if hasattr(obj, field):
            value = getattr(obj, field)
            if value is not None and len(value) > 0:
                cat_text += " " + " ".join(value)

    return cat_text


class Resource(Base):
    __tablename__ = "resource"
    __label__ = "Online Information"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(default="resource")
    title: Mapped[str]
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    description: Mapped[str]
    insurance: Mapped[Optional[str]]
    organization_name: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    phone_extension: Mapped[Optional[str]]
    website: Mapped[str]
    contact_email: Mapped[Optional[str]]
    video_code: Mapped[Optional[str]]
    is_uva_education_content: Mapped[Optional[bool]]
    is_draft: Mapped[bool]
    ages: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    languages: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    covid19_categories: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    should_hide_related_resources: Mapped[bool] = mapped_column(default=False)

    __mapper_args__ = {"polymorphic_identity": "resource", "polymorphic_on": "type"}

    categories: Mapped[list["Category"]] = relationship(
        secondary="resource_category", back_populates="resources", viewonly=True
    )
    resource_categories: Mapped[list["ResourceCategory"]] = relationship(back_populates="resource")
    admin_notes: Mapped[list["AdminNote"]] = relationship(back_populates="resource")

    def indexable_content(self):
        return " ".join(
            filter(
                None,
                (
                    self.title,
                    self.description,
                    self.insurance,
                    self.category_names(),
                ),
            )
        )

    def category_names(self):
        return _category_names(self)


class ResourceCategory(Base):
    __tablename__ = "resource_category"
    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    type: Mapped[str] = mapped_column(default="resource")
    resource_id: Mapped[int] = mapped_column(ForeignKey("resource.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    resource: Mapped["Resource"] = relationship(back_populates="resource_categories")
    category: Mapped["Category"] = relationship(back_populates="category_resources")


class Location(Resource):
    __tablename__ = "location"
    __label__ = "Local Services"
    id: Mapped[int] = mapped_column(ForeignKey("resource.id"), primary_key=True)
    l_type: Mapped[str] = mapped_column("type", default="location")
    primary_contact: Mapped[Optional[str]]
    street_address1: Mapped[str]
    street_address2: Mapped[Optional[str]]
    city: Mapped[str]
    state: Mapped[str]
    zip: Mapped[str]
    email: Mapped[Optional[str]]
    latitude: Mapped[Optional[float]]
    longitude: Mapped[Optional[float]]

    __mapper_args__ = {
        "polymorphic_identity": "location",
    }


class Event(Location):
    __tablename__ = "event"
    __label__ = "Events and Training"
    id: Mapped[int] = mapped_column(ForeignKey("location.id"), primary_key=True)
    e_type: Mapped[str] = mapped_column("type", default="event")
    date: Mapped[datetime] = mapped_column(default=func.now())
    time: Mapped[Optional[str]]
    ticket_cost: Mapped[Optional[str]]
    location_name: Mapped[Optional[str]]
    includes_registration: Mapped[Optional[bool]]
    webinar_link: Mapped[Optional[str]]
    post_survey_link: Mapped[Optional[str]]
    max_users: Mapped[Optional[int]]
    registration_url: Mapped[Optional[str]]
    image_url: Mapped[Optional[str]]
    post_event_description: Mapped[Optional[str]]
    users: Mapped[list["User"]] = relationship(secondary="event_user", back_populates="events", viewonly=True)
    registered_users: Mapped[list["EventUser"]] = relationship(back_populates="event")

    __mapper_args__ = {
        "polymorphic_identity": "event",
    }

    def indexable_content(self):
        return " ".join(
            filter(
                None,
                (
                    self.title,
                    self.description,
                    self.post_event_description,
                    self.insurance,
                    self.category_names(),
                ),
            )
        )


class EventUser(Base):
    __tablename__ = "event_user"
    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    event: Mapped["Event"] = relationship(back_populates="registered_users")
    user: Mapped["User"] = relationship(back_populates="user_events")


@dataclass
class ExportInfo:
    table_name: str
    class_name: str
    size: Optional[int] = 0
    url: Optional[str] = ""
    question_type: Optional[str] = ""
    exportable: Optional[bool] = True
    json_data: dict | list[dict] = field(default_factory=dict)
    sub_tables: Optional[list["ExportInfo"]] = field(default_factory=list)

    @property
    def display_name(self):
        # Capitalizes, removes '_', drops 'Questionnaire' and limits to 30 chars.
        title = self.class_name
        title = re.sub("(.)([A-Z][a-z]+)", r"\1 \2", title)
        title = re.sub("([a-z0-9])([A-Z])", r"\1 \2", title)
        return title.replace("Questionnaire", "").strip()[:30]


class Step:
    STATUS_COMPLETE = "COMPLETE"
    STATUS_INCOMPLETE = "INCOMPLETE"

    def __init__(self, name, question_type, label):
        self.name = name
        self.type = question_type
        self.label = label
        self.status = self.STATUS_INCOMPLETE
        self.date_completed = None
        self.questionnaire_id = None


class StepLog(Base):
    __tablename__ = "step_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    questionnaire_name: Mapped[str]
    questionnaire_id: Mapped[int]
    flow: Mapped[str]
    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    date_completed: Mapped[datetime] = mapped_column(default=func.now())
    time_on_task_ms: Mapped[int]
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class Flow:
    steps: list[Step]

    def __init__(self, name):
        self.name = name
        self.steps = []
        self.relationship = ""

    def has_step(self, questionnaire_name):
        for q in self.steps:
            if q.name == questionnaire_name:
                return True
        return False

    def update_step_progress(self, step_log: StepLog) -> list[Step]:
        updated_steps = copy.deepcopy(self.steps)
        for step in updated_steps:
            if step.name == step_log.questionnaire_name:
                step.status = step.STATUS_COMPLETE
                step.date_completed = step_log.date_completed
                step.questionnaire_id = step_log.questionnaire_id

        self.steps = updated_steps
        return self.steps

    def add_step(self, questionnaire_name):
        if not self.has_step(questionnaire_name):
            class_name = pascal_case_it(questionnaire_name)
            cls = get_class(class_name)
            q = cls()
            step = Step(questionnaire_name, q.__question_type__, q.__label__)
            self.steps.append(step)


class Flows:

    # WIP Method
    @staticmethod
    def parse_form():
        return ""

    @staticmethod
    def get_self_intake_flow() -> Flow:
        flow = Flow(name="self_intake")
        flow.relationship = Relationship.self_participant
        flow.add_step("identification_questionnaire")
        flow.add_step("contact_questionnaire")
        flow.add_step("demographics_questionnaire")
        flow.add_step("home_self_questionnaire")
        flow.add_step("evaluation_history_self_questionnaire")
        flow.add_step("clinical_diagnoses_questionnaire")
        flow.add_step("current_behaviors_self_questionnaire")
        flow.add_step("education_self_questionnaire")
        flow.add_step("employment_questionnaire")
        flow.add_step("supports_questionnaire")
        return flow

    @staticmethod
    def get_dependent_intake_flow() -> Flow:
        flow = Flow(name="dependent_intake")
        flow.relationship = Relationship.dependent
        flow.add_step("identification_questionnaire")
        flow.add_step("demographics_questionnaire")
        flow.add_step("home_dependent_questionnaire")
        flow.add_step("evaluation_history_dependent_questionnaire")
        flow.add_step("clinical_diagnoses_questionnaire")
        flow.add_step("developmental_questionnaire")
        flow.add_step("current_behaviors_dependent_questionnaire")
        flow.add_step("education_dependent_questionnaire")
        flow.add_step("supports_questionnaire")
        return flow

    @staticmethod
    def get_guardian_intake_flow() -> Flow:
        flow = Flow(name="guardian_intake")
        flow.relationship = Relationship.self_guardian
        flow.add_step("identification_questionnaire")
        flow.add_step("contact_questionnaire")
        flow.add_step("demographics_questionnaire")
        return flow

    @staticmethod
    def get_professional_intake_flow() -> Flow:
        flow = Flow(name="professional_intake")
        flow.relationship = Relationship.self_professional
        flow.add_step("identification_questionnaire")
        flow.add_step("contact_questionnaire")
        flow.add_step("demographics_questionnaire")
        flow.add_step("professional_profile_questionnaire")
        return flow

    @staticmethod
    def get_interested_intake_flow() -> Flow:
        flow = Flow(name="interested_intake")
        flow.relationship = Relationship.self_interested
        flow.add_step("identification_questionnaire")
        flow.add_step("contact_questionnaire")
        return flow

    @staticmethod
    def get_registration_flow() -> Flow:
        flow = Flow(name="registration")
        flow.add_step("registration_questionnaire")
        return flow

    # SkillStar Flows
    @staticmethod
    def get_skillstar_flow() -> Flow:
        flow = Flow(name="skillstar")
        flow.relationship = Relationship.self_professional
        flow.add_step("chain_questionnaire")
        return flow

    @staticmethod
    def get_skillstar_flows() -> list[Flow]:
        flows = [
            Flows.get_skillstar_flow(),
        ]
        return flows

    @staticmethod
    def get_all_flows() -> list[Flow]:
        flows = [
            Flows.get_self_intake_flow(),
            Flows.get_dependent_intake_flow(),
            Flows.get_guardian_intake_flow(),
            Flows.get_professional_intake_flow(),
            Flows.get_interested_intake_flow(),
            Flows.get_registration_flow(),
            Flows.get_skillstar_flow(),
        ]
        return flows

    @staticmethod
    def get_flow_by_name(name) -> Flow:
        if name == "self_intake":
            return Flows.get_self_intake_flow()
        if name == "dependent_intake":
            return Flows.get_dependent_intake_flow()
        if name == "guardian_intake":
            return Flows.get_guardian_intake_flow()
        if name == "professional_intake":
            return Flows.get_professional_intake_flow()
        if name == "interested_intake":
            return Flows.get_interested_intake_flow()
        if name == "registration":
            return Flows.get_registration_flow()
        if name == "skillstar":
            return Flows.get_skillstar_flow()

    @staticmethod
    def get_flow_by_relationship(name) -> Flow:
        if name == Relationship.self_participant:
            return Flows.get_self_intake_flow()
        if name == Relationship.dependent:
            return Flows.get_dependent_intake_flow()
        if name == Relationship.self_guardian:
            return Flows.get_guardian_intake_flow()
        if name == Relationship.self_professional:
            return Flows.get_professional_intake_flow()
        if name == Relationship.self_interested:
            return Flows.get_interested_intake_flow()


class FrontendConfig:
    """Provides general information about the backend service, what mode it is running in, could also use it for
    health checks etc..."""

    development = settings.DEVELOPMENT
    testing = settings.TESTING
    mirroring = settings.MIRRORING
    production = settings.PRODUCTION
    apiUrl = settings.API_URL
    apiKey = settings.GOOGLE_MAPS_API_KEY
    googleAnalyticsKey = settings.GOOGLE_ANALYTICS_API_KEY


class Geocode:
    @staticmethod
    def get_geocode(address_dict):

        if settings.TESTING:
            z = session.query(ZipCode).order_by(func.random()).first()
            print("TEST:  Pretending to get the geocode and setting lat/lng to  %s - %s" % (z.latitude, z.longitude))
            return {"lat": z.latitude, "lng": z.longitude}

        else:
            api_key = settings.GOOGLE_MAPS_API_KEY
            gmaps = googlemaps.Client(key=api_key)
            lat = None
            lng = None

            # Check that location has at least a zip code
            if address_dict["zip"]:

                # Look up the latitude and longitude using Google Maps API
                address = ""
                for value in address_dict:
                    if address_dict[value] is not None:
                        address = address + " " + address_dict[value]
                geocode_result = gmaps.geocode(address)

                if geocode_result is not None:
                    if geocode_result[0] is not None:
                        loc = geocode_result[0]["geometry"]["location"]
                        lat = loc["lat"]
                        lng = loc["lng"]
                        print(address_dict, loc)

            return {"lat": lat, "lng": lng}


class Investigator(Base):
    __tablename__ = "investigator"
    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    name: Mapped[str]
    title: Mapped[str]
    organization_name: Mapped[Optional[str]]
    bio_link: Mapped[Optional[str]]
    studies: Mapped[list["Study"]] = relationship(
        secondary="study_investigator", back_populates="investigators", viewonly=True
    )
    investigator_studies: Mapped[list["StudyInvestigator"]] = relationship(back_populates="investigator")


class IdentificationQuestionnaire(Base, QuestionnaireMixin):
    __tablename__ = "identification_questionnaire"
    __label__ = "Identification"
    __question_type__ = ExportService.TYPE_IDENTIFYING
    __estimated_duration_minutes__ = 5
    relationship_to_participant_other_hide_expression = (
        '!(model.relationship_to_participant && (model.relationship_to_participant === "other"))'
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    relationship_to_participant: Mapped[Optional[str]] = mapped_column(
        info={
            "RELATIONSHIP_REQUIRED": ["dependent"],
            "display_order": 1.1,
            "type": "radio",
            "template_options": {
                "required": False,
                "label": "",
                "options": [
                    {"value": "bioMother", "label": "Biological mother"},
                    {"value": "bioFather", "label": "Biological father"},
                    {"value": "adoptMother", "label": "Adoptive mother"},
                    {"value": "adoptFather", "label": "Adoptive father"},
                    {"value": "other", "label": "Other"},
                ],
            },
        },
    )
    relationship_to_participant_other: Mapped[Optional[str]] = mapped_column(
        info={
            "RELATIONSHIP_REQUIRED": ["dependent"],
            "display_order": 1.2,
            "type": "input",
            "template_options": {
                "label": "Enter your relationship",
                "required": True,
            },
            "hide_expression": relationship_to_participant_other_hide_expression,
            "expression_properties": {
                "template_options.required": "!" + relationship_to_participant_other_hide_expression
            },
        },
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2,
            "type": "input",
            "template_options": {"label": "First name", "required": True},
        },
    )
    middle_name: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3,
            "type": "input",
            "template_options": {"label": "Middle name"},
            "hide_expression": "model.no_middle_name",
            "expression_properties": {"template_options.required": "!model.no_middle_name"},
        },
    )
    no_middle_name: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 3.5,
            "type": "checkbox",
            "defaultValue": False,
            "template_options": {
                "label": "If NO Middle Name click here",
                "required": False,
            },
        },
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4,
            "type": "input",
            "template_options": {"label": "Last name", "required": True},
        },
    )
    is_first_name_preferred: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 5,
            "type": "radio",
            "template_options": {
                "required": False,
                "label": {
                    "RELATIONSHIP_SPECIFIC": {
                        "self_participant": "Is this your preferred name?",
                        "self_guardian": "Is this your preferred name?",
                        "self_professional": "Is this your preferred name?",
                        "self_interested": "Is this your preferred name?",
                        "dependent": "Is this your child's preferred name?",
                    }
                },
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    nickname: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 6,
            "type": "input",
            "template_options": {
                "label": "Nickname",
                "required": False,
            },
            "hide_expression": "model.is_first_name_preferred",
        },
    )
    birthdate: Mapped[datetime] = mapped_column(
        default=func.now(),
        info={
            "display_order": 7,
            "type": "datepicker",
            "template_options": {
                "required": True,
                "label": {
                    "RELATIONSHIP_SPECIFIC": {
                        "self_participant": "Your date of birth",
                        "self_guardian": "Your date of birth",
                        "self_professional": "Your date of birth",
                        "self_interested": "Your date of birth",
                        "dependent": "Your child's date of birth",
                    }
                },
            },
        },
    )
    birth_city: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 8,
            "type": "input",
            "template_options": {
                "required": True,
                "label": {
                    "RELATIONSHIP_SPECIFIC": {
                        "self_participant": "Your city/municipality of birth",
                        "self_guardian": "Your city/municipality of birth",
                        "self_professional": "Your city/municipality of birth",
                        "self_interested": "Your city/municipality of birth",
                        "dependent": "Your child's city/municipality of birth",
                    }
                },
            },
        },
    )
    birth_state: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 9,
            "type": "input",
            "template_options": {
                "required": True,
                "label": {
                    "RELATIONSHIP_SPECIFIC": {
                        "self_participant": "Your state of birth",
                        "self_guardian": "Your state of birth",
                        "self_professional": "Your state of birth",
                        "self_interested": "Your state of birth",
                        "dependent": "Your child's state of birth",
                    }
                },
            },
        },
    )
    is_english_primary: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 10,
            "type": "radio",
            "template_options": {
                "required": False,
                "label": {
                    "RELATIONSHIP_SPECIFIC": {
                        "self_participant": "Is your primary language English?",
                        "self_guardian": "Is your primary language English?",
                        "self_professional": "Is your primary language English?",
                        "self_interested": "Is your primary language English?",
                        "dependent": "Is your child's primary language English?",
                    }
                },
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    def get_name(self):
        if not self.is_first_name_preferred:
            return self.nickname
        else:
            return self.first_name

    def get_field_groups(self):
        return {
            "relationship": {
                "RELATIONSHIP_REQUIRED": ["dependent"],
                "fields": [
                    "relationship_to_participant",
                    "relationship_to_participant_other",
                ],
                "display_order": 0,
                "wrappers": ["card"],
                "template_options": {
                    "label": "Your relationship to your child or the person with autism on whom you are providing information:"
                },
            },
            "intro": {
                "fields": [],
                "display_order": 1,
                "wrappers": ["help"],
                "template_options": {
                    "description": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": "Please answer the following questions about yourself (* indicates required response):",
                            "self_guardian": "Please answer the following questions about yourself (* indicates required response):",
                            "self_professional": "Please answer the following questions about yourself (* indicates required response):",
                            "dependent": "Please answer the following questions about your child or the person with autism on whom you are providing information",
                        }
                    }
                },
            },
        }


class ContactQuestionnaire(Base, QuestionnaireMixin):
    __tablename__ = "contact_questionnaire"
    __label__ = "Contact Information"
    __question_type__ = ExportService.TYPE_IDENTIFYING
    __estimated_duration_minutes__ = 5
    marketing_other_hide_expression = '!(model.marketing_channel && (model.marketing_channel === "other"))'

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)

    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    participant: Mapped["Participant"] = relationship(back_populates="contact")
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    user: Mapped["User"] = relationship()
    phone: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.1,
            "type": "input",
            "template_options": {
                "required": True,
                "type": "tel",
                "label": "Preferred number",
                "description": "(including area code)",
                "placeholder": "555-555-5555",
            },
            "validators": {"validation": ["phone"]},
        },
    )
    phone_type: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.2,
            "type": "radio",
            "template_options": {
                "label": "Type",
                "placeholder": "",
                "description": "",
                "required": True,
                "options": [
                    {"value": "home", "label": "Home"},
                    {"value": "cell", "label": "Cell"},
                ],
            },
        },
    )
    can_leave_voicemail: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 1.3,
            "type": "radio",
            "template_options": {
                "label": "Leave voicemail?",
                "description": "Is it okay to leave a voicemail message at this number?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    contact_times: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.4,
            "type": "textarea",
            "template_options": {
                "label": "Best times to call",
                "description": "Some research studies might involve a phone call. "
                "If that’s the case, when would be the best times "
                "of day to call you?",
                "required": False,
            },
        },
    )
    email: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2,
            "type": "input",
            "template_options": {
                "label": "Email",
                "type": "email",
                "required": True,
            },
            "validators": {"validation": ["email"]},
        },
    )
    street_address: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3.1,
            "type": "input",
            "template_options": {"label": "Street Address", "required": True},
        },
    )
    city: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3.2,
            "type": "input",
            "template_options": {"label": "Town/City", "required": False},
        },
    )
    state: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3.3,
            "type": "input",
            "template_options": {"label": "State", "required": False},
        },
    )
    zip: Mapped[Optional[int]] = mapped_column(
        info={
            "display_order": 3.4,
            "type": "input",
            "template_options": {
                "type": "number",
                "label": "Zip",
                "max": 99999,
                "min": 0,
                "pattern": "\\d{5}",
                "required": True,
            },
        },
    )
    marketing_channel: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4.1,
            "type": "select",
            "template_options": {
                "label": "",
                "placeholder": "Please select how you heard about us",
                "description": "",
                "required": True,
                "options": [
                    {"value": "internet", "label": "Internet"},
                    {"value": "health_care_provider", "label": "Health care provider (doctor, speech therapist, etc)"},
                    {"value": "school", "label": "Teacher or school"},
                    {"value": "word_of_mouth", "label": "Word of mouth (friend, family member, etc)"},
                    {"value": "community_event", "label": "Community event (autism walk, resource fair, etc.)"},
                    {"value": "media", "label": "Television or radio (CNN, NPR, local news, etc.)"},
                    {"value": "research_study", "label": "While participating in a research study"},
                    {"value": "other", "label": "Other"},
                ],
            },
        },
    )
    marketing_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4.2,
            "type": "input",
            "template_options": {
                "label": "Please specify how you heard about us",
                "required": True,
            },
            "hide_expression": marketing_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + marketing_other_hide_expression},
        },
    )

    def get_field_groups(self):
        return {
            "phone_group": {
                "fields": [
                    "phone",
                    "phone_type",
                    "can_leave_voicemail",
                    "contact_times",
                ],
                "display_order": 1,
                "wrappers": ["card"],
                "template_options": {"label": "Phone"},
            },
            "address": {
                "fields": ["street_address", "city", "state", "zip"],
                "display_order": 3,
                "wrappers": ["card"],
                "template_options": {"label": "Address"},
            },
            "email": {
                "fields": ["email"],
                "display_order": 4,
                "wrappers": ["card"],
                "template_options": {"label": "Email"},
            },
            "marketing": {
                "fields": ["marketing_channel", "marketing_other"],
                "display_order": 5,
                "wrappers": ["card"],
                "template_options": {"label": "How did you hear about us?"},
            },
        }


class Participant(Base):
    # The participant model is used to track enrollment and participation in studies. Participants are associated
    # with a user account; sometimes that of themselves and sometimes that of their guardian.
    __tablename__ = "stardrive_participant"
    id: Mapped[int] = mapped_column(primary_key=True, default=random_integer)
    # last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    last_updated: Mapped[datetime] = mapped_column(default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    user: Mapped["User"] = relationship(back_populates="participants")
    identification: Mapped["IdentificationQuestionnaire"] = relationship()
    contact: Mapped["ContactQuestionnaire"] = relationship()
    relationship: Mapped["Relationship"]
    avatar_icon: Mapped[Optional[str]]
    avatar_color: Mapped[Optional[str]]
    has_consented: Mapped[Optional[bool]]

    def get_name(self):
        db_self = session.execute(select(Participant).filter(Participant.id == self.id)).unique().scalar_one()
        name = db_self.identification.get_name() if db_self.identification else ""
        session.close()
        return name

    def get_percent_complete(self):
        flow = Flows.get_flow_by_relationship(self.relationship)
        num_steps = len(flow.steps)
        step_logs = (
            session.execute(
                select(StepLog)
                .filter(StepLog.participant_id == cast(self.id, Integer))
                .filter(StepLog.flow == flow.name)
            )
            .unique()
            .scalars()
            .all()
        )
        session.close()

        complete_steps = 0
        for log in step_logs:
            flow.update_step_progress(log)

        for step in flow.steps:
            if step.status == step.STATUS_COMPLETE:
                complete_steps += 1

        return complete_steps / num_steps


class AggCount:
    value = ""
    count = 0
    is_selected = False

    def __init__(self, value, count, is_selected):
        self.value = value
        self.count = count
        self.is_selected = is_selected


@dataclass(kw_only=True)
class Hit:
    ages: Optional[list[str]] = field(default_factory=list)
    category: Optional[list[str]] = field(default_factory=list)
    content: Optional[str] = ""
    date: Optional[str | datetime] = None
    description: Optional[str] = ""
    geo_point: Optional[GeoPointType] = None
    highlights: Optional[str] = ""
    id: Optional[str] = ""
    is_draft: Optional[bool] = True
    label: Optional[str] = ""
    languages: Optional[list[str]] = field(default_factory=list)
    last_updated: Optional[str | datetime] = None
    latitude: Optional[float] = None
    location: Optional[str] = ""
    longitude: Optional[float] = None
    no_address: Optional[bool] = True
    organization_name: Optional[str] = ""
    post_event_description: Optional[str] = ""
    status: Optional[str] = ""
    title: Optional[str] = ""
    type: Optional[str] = ""
    website: Optional[str] = ""


@dataclass(kw_only=True)
class MapHit:
    id: Optional[int] = None
    latitude: Optional[int] = None
    longitude: Optional[int] = None
    no_address: Optional[bool] = True
    type: Optional[str] = ""


@dataclass
class Search:
    words: str = ""
    total: int = 0
    hits: list[Hit] = field(default_factory=list)
    types: list[AggCount] = field(default_factory=list)
    ages: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    start: int = 0
    size: int = 10
    type_counts: list[AggCount] = field(default_factory=list)
    age_counts: list[AggCount] = field(default_factory=lambda: Search.known_age_counts())
    language_counts: list[AggCount] = field(default_factory=lambda: Search.known_language_counts())
    sort: Optional[str] = None
    category: Optional[any] = None
    date: Optional[datetime] = None
    map_data_only: bool = False  # When we should return a limited set of details just for mapping.
    geo_box: Optional[GeoBoxType] = None
    geo_point: Optional[GeoPointType] = None

    # Creates a pre ordered list of aggregation counts based on order in Age Range class.
    @staticmethod
    def known_age_counts():
        return list(map(lambda age_name: (AggCount(age_name, 0, False)), AgeRange.ages))

    @staticmethod
    def known_language_counts():
        return list(
            map(
                lambda age_name: (AggCount(age_name, 0, False)),
                ["english", "spanish", "chinese", "korean", "vietnamese", "arabic", "tagalog"],
            )
        )

    # Method called when updating a search with fresh results.
    # This should zero-out any existing data that should be overwritten.
    def reset(self):
        self.type_counts = []
        self.age_counts = Search.known_age_counts()
        self.language_counts = Search.known_language_counts()
        self.hits = []
        self.total = 0

    def add_aggregation(self, field, value, count, is_selected):
        if field == "ages":
            try:
                ac = next(ac for ac in self.age_counts if ac.value == value)
                ac.count = count
                ac.is_selected = is_selected
            except StopIteration:  # Go ahead and add it so it shows up, but this is bad data..
                self.age_counts.append(AggCount(value, count, is_selected))
        if field == "languages":
            try:
                lc = next(lc for lc in self.language_counts if lc.value == value)
                lc.count = count
                lc.is_selected = is_selected
            except StopIteration:  # Go ahead and add it so it shows up, but this is bad data..
                self.language_counts.append(AggCount(value, count, is_selected))
        if field == "types":
            self.type_counts.append(AggCount(value, count, is_selected))

    # can be used to verify that a given age range is supported.
    @staticmethod
    def has_age_range():
        return next((ac for ac in Search.known_age_counts() if ac.value == "value"), None) is not None

    # can be used to verify that a given language is supported.
    @staticmethod
    def has_language():
        return next((ac for ac in Search.known_language_counts() if ac.value == "value"), None) is not None


class Geopoint:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


class Geobox:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right


class Sort:
    def __init__(self, field, latitude, longitude, order, unit):
        self.field = field
        self.latitude = latitude
        self.longitude = longitude
        self.order = order
        self.unit = unit

    def translate(self):
        if None not in (self.latitude, self.latitude):
            return {
                "_geo_distance": {
                    self.field: {"lat": self.latitude, "lon": self.longitude},
                    "order": self.order,
                    "unit": self.unit,
                }
            }
        else:
            return {self.field: {"order": self.order}}


class Study(Base):
    __tablename__ = "study"
    __label__ = "Research Studies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    short_title: Mapped[Optional[str]]
    short_description: Mapped[Optional[str]]
    image_url: Mapped[Optional[str]]
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    description: Mapped[str]
    participant_description: Mapped[str]
    benefit_description: Mapped[str]
    coordinator_email: Mapped[str]
    eligibility_url: Mapped[Optional[str]]
    survey_url: Mapped[Optional[str]]
    results_url: Mapped[Optional[str]]
    organization_name: Mapped[Optional[str]]
    location: Mapped[Optional[str]]
    num_visits: Mapped[Optional[int]]
    status: Mapped[Status]
    ages: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    languages: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    categories: Mapped[list["Category"]] = relationship(
        secondary="study_category", back_populates="studies", viewonly=True
    )
    study_categories: Mapped[list["StudyCategory"]] = relationship(back_populates="study")
    investigators: Mapped[list["Investigator"]] = relationship(
        secondary="study_investigator", back_populates="studies", viewonly=True
    )
    study_investigators: Mapped[list["StudyInvestigator"]] = relationship(back_populates="study")
    study_users: Mapped[list["StudyUser"]] = relationship(back_populates="study")
    users: Mapped[list["User"]] = relationship(secondary="study_user", back_populates="studies", viewonly=True)

    def indexable_content(self):
        return " ".join(
            filter(
                None,
                (
                    self.category_names(),
                    self.title,
                    self.short_title,
                    self.short_description,
                    self.description,
                    self.participant_description,
                    self.benefit_description,
                    self.location,
                ),
            )
        )

    def category_names(self):
        return _category_names(self)


class StudyInvestigator(Base):
    __tablename__ = "study_investigator"
    id: Mapped[int] = mapped_column(primary_key=True)
    study_id: Mapped[int] = mapped_column(ForeignKey("study.id"))
    investigator_id: Mapped[int] = mapped_column(ForeignKey("investigator.id"))
    study: Mapped["Study"] = relationship(back_populates="study_investigators")
    investigator: Mapped["Investigator"] = relationship(back_populates="investigator_studies")
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class StudyCategory(Base):
    __tablename__ = "study_category"
    id: Mapped[int] = mapped_column(primary_key=True)
    study_id: Mapped[int] = mapped_column(ForeignKey("study.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    study: Mapped["Study"] = relationship(back_populates="study_categories")
    category: Mapped["Category"] = relationship(back_populates="category_studies")
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class StudyUser(Base):
    __tablename__ = "study_user"
    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    status: Mapped[Optional["StudyUserStatus"]]
    study_id: Mapped[int] = mapped_column(ForeignKey("study.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    study: Mapped["Study"] = relationship(back_populates="study_users")
    user: Mapped["User"] = relationship(back_populates="user_studies")


class User(Base):
    """
    The user model is used to manage interaction with the StarDrive system, including sign-in and access levels. Users
    can be Admins, people with autism and/or their guardians wishing to manage their care and participate in studies,
    as well professionals in the field of autism research and care. Anyone who wishes to use the system will have a
    user account. Please note that there is a separate participant model for tracking enrollment and participation in
    studies.
    """

    __tablename__ = "stardrive_user"
    id: Mapped[int] = mapped_column(primary_key=True, default=random_integer)
    # last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    last_updated: Mapped[datetime] = mapped_column(default=func.now())
    registration_date: Mapped[datetime] = mapped_column(default=func.now())
    last_login: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    role: Mapped[Role]
    participants: Mapped[list["Participant"]] = relationship(back_populates="user")
    participant_count = column_property(
        select(func.count(Participant.id))
        .where(Participant.user_id == id)
        .correlate_except(Participant)
        .scalar_subquery()
    )
    email_verified: Mapped[Optional[bool]] = mapped_column(default=False)
    _password: Mapped[Optional[bytes]] = mapped_column("password")
    token: Mapped[str] = mapped_column(default="")
    token_url: Mapped[str] = mapped_column(default="")
    events: Mapped[list["Event"]] = relationship(secondary="event_user", back_populates="users", viewonly=True)
    user_events: Mapped[list["EventUser"]] = relationship(back_populates="user")
    admin_notes: Mapped[list["AdminNote"]] = relationship(back_populates="user")
    studies: Mapped[list["Study"]] = relationship(secondary="study_user", back_populates="users", viewonly=True)
    user_studies: Mapped[list["StudyUser"]] = relationship(back_populates="user")

    def related_to_participant(self, participant_id):
        db_self = (
            session.execute(select(User).options(joinedload(User.participants)).filter(User.id == self.id))
            .unique()
            .scalar_one()
        )
        for p in db_self.participants:
            if participant_id == p.id:
                return True

    def self_participant(self):
        db_self = (
            session.execute(select(User).options(joinedload(User.participants)).filter_by(id=self.id))
            .unique()
            .scalar_one()
        )
        participants = db_self.participants
        session.close()

        if len(participants) > 0:
            for p in participants:
                p_id = p.id
                db_p = (
                    session.execute(
                        select(Participant)
                        .options(
                            joinedload(Participant.identification),
                            joinedload(Participant.contact),
                            joinedload(Participant.user),
                        )
                        .filter(Participant.id == p_id)
                    )
                    .unique()
                    .scalar()
                )
                session.close()
                if "self" in db_p.relationship.name:
                    return db_p

    def self_registration_complete(self):
        self_participant = self.self_participant()
        if self_participant is not None:
            return self_participant.get_percent_complete() == 1

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        from app.rest_exception import RestException

        role_name = self.role_name()
        if self.password_meets_requirements(role_name, plaintext):
            self._password = bcrypt.generate_password_hash(plaintext)
        else:
            message = "Please enter a valid password. " + password_requirements[role_name]["instructions"]
            raise RestException(RestException.INVALID_INPUT, details=message)

        session.close()

    def role_name(self):
        return self.role if isinstance(self.role, str) else self.role.name

    @classmethod
    def password_meets_requirements(cls, role_name, plaintext):
        reqs = password_requirements[role_name]
        regex = re.compile(reqs["regex"])

        if plaintext and isinstance(plaintext, str):
            match = regex.match(plaintext)
            return bool(match)
        else:
            return False

    @classmethod
    def is_correct_password(cls, user_id: int, plaintext: str) -> bool:
        from app.rest_exception import RestException
        from app.database import session

        db_user = (
            session.execute(select(User).options(joinedload(User.participants)).filter_by(id=user_id))
            .unique()
            .scalar_one()
        )

        if not db_user._password:
            raise RestException(RestException.LOGIN_FAILURE)
        is_correct = bcrypt.check_password_hash(db_user._password, plaintext)

        session.close()
        return is_correct

    @classmethod
    def encode_auth_token(cls, user_id: int):
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(hours=2, minutes=0, seconds=0),
                "iat": datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        except Exception as e:
            return e

    @classmethod
    def decode_auth_token(cls, auth_token: str) -> int:
        from app.rest_exception import RestException

        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms="HS256")
            return int(payload["sub"])
        except jwt.ExpiredSignatureError:
            raise RestException(RestException.TOKEN_EXPIRED)
        except jwt.InvalidTokenError:
            raise RestException(RestException.TOKEN_INVALID)

    def get_contact(self):
        for p in self.participants:
            if p.contact:
                return {"name": p.get_name(), "relationship": p.relationship.name, "contact": p.contact}

    def created_password(self):
        return self._password is not None

    def identity(self):
        self_participant = self.self_participant()
        return "Not set" if self_participant is None else self_participant.relationship.name

    def percent_self_registration_complete(self):
        self_participant = self.self_participant()
        return 0 if self_participant is None else self_participant.get_percent_complete()


class UserFavorite(Base):
    __tablename__ = "user_favorite"
    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    type: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    resource_id: Mapped[Optional[int]] = mapped_column(ForeignKey("resource.id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))
    age_range: Mapped[Optional[str]]
    language: Mapped[Optional[str]]
    covid19_category: Mapped[Optional[str]]
    user = relationship(User, backref=backref("user_favorites", lazy="joined"))
    resource = relationship(Resource, backref=backref("user_favorites", lazy="joined"))
    category = relationship(Category, backref=backref("user_favorites", lazy="joined"))


class UserMeta(Base):
    __tablename__ = "usermeta"
    __label__ = "User Meta Info"
    id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"), primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    self_participant: Mapped[Optional[bool]]
    self_has_guardian: Mapped[Optional[bool]]
    guardian: Mapped[Optional[bool]]
    guardian_has_dependent: Mapped[Optional[bool]]
    professional: Mapped[Optional[bool]]
    interested: Mapped[Optional[bool]]

    def get_relationship(self):
        if self.self_participant:
            return None if self.self_has_guardian else Relationship.self_participant.name
        if self.guardian and self.guardian_has_dependent:
            return Relationship.self_guardian.name
        if self.professional:
            return Relationship.self_professional.name
        # Lower Precedence Relationships
        if self.guardian and not self.guardian_has_dependent:
            return Relationship.self_interested.name
        if self.interested:
            return Relationship.self_interested.name
        return ""


class ZipCode(Base):
    __tablename__ = "zip_code"
    id: Mapped[int] = mapped_column(primary_key=True)
    latitude: Mapped[float]
    longitude: Mapped[float]
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class AlternativeAugmentative(Base, QuestionnaireMixin):
    __tablename__ = "alternative_augmentative"
    __label__ = "Alternative and Augmentative Communication"
    __no_export__ = True  # This will be transferred as a part of a parent class
    type_other_hide_expression = '!(model.type && (model.type === "other"))'
    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    supports_questionnaire_id: Mapped[int] = mapped_column(ForeignKey("supports_questionnaire.id", ondelete="CASCADE"))
    type: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.1,
            "type": "radio",
            "default": "self",
            "class_name": "vertical-radio-group",
            "template_options": {
                "required": True,
                "label": "Select device",
                "placeholder": "Please select",
                "options": [
                    {
                        "value": "noTechAAC",
                        "label": "No-Tech AAC: facial expressions, body posture, head nods, reaching/pointing, gestures, or signs",
                    },
                    {
                        "value": "lowTechAAC",
                        "label": "Low-Tech AAC: pen and paper, pictures/symbols, communication boards/books",
                    },
                    {
                        "value": "midTechAAC",
                        "label": "Mid -Tech AAC: battery operated or simple electronic devices",
                    },
                    {
                        "value": "highTechAAC",
                        "label": "High-Tech AAC: computerized devices (e.g., tablets, ipads) displaying letters, words, pictures, or symbols",
                    },
                ],
            },
        },
    )
    type_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Enter alternative and augmentative communication system",
                "required": True,
            },
            "hide_expression": type_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + type_other_hide_expression},
        },
    )
    timeframe: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "current", "label": "Currently using"},
                    {"value": "past", "label": "Used in the past"},
                    {"value": "futureInterest", "label": "Interested in using"},
                ],
            },
        },
    )
    notes: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4,
            "type": "textarea",
            "template_options": {
                "label": "Notes on use and/or issues with alternative and augmentative communication system",
                "required": False,
            },
        },
    )

    def get_field_groups(self):
        return {
            "type": {
                "fields": ["type", "type_other"],
                "display_order": 1,
                "wrappers": ["card"],
                "template_options": {"label": "Type of alternative and augmentative communication system"},
            }
        }


class AssistiveDevice(Base, QuestionnaireMixin):
    __tablename__ = "assistive_device"
    __label__ = "Assistive Device"
    __no_export__ = True  # This will be transferred as a part of a parent class
    type_other_hide_expression = (
        '!((model.type_group && (model.type_group === "other")) || (model.type && (model.type === "other")))'
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    supports_questionnaire_id: Mapped[int] = mapped_column(ForeignKey("supports_questionnaire.id", ondelete="CASCADE"))
    type_group: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.1,
            "type": "select",
            "template_options": {
                "required": True,
                "label": "Select category of device",
                "placeholder": "Please select",
                "options": [
                    {
                        "value": "mobility",
                        "label": "Mobility aids",
                    },
                    {
                        "value": "hearing",
                        "label": "Hearing assistance",
                    },
                    {
                        "value": "computer",
                        "label": "Computer software and hardware",
                    },
                    {
                        "value": "building",
                        "label": "ADA Building Modifications",
                    },
                    {
                        "value": "other",
                        "label": "Others",
                    },
                ],
            },
        },
    )
    type: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.2,
            "type": "select",
            "template_options": {
                "required": True,
                "label": "Select device",
                "placeholder": "Please select",
                "all_options": [
                    {
                        "value": "cane",
                        "label": "Canes",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "crutches",
                        "label": "Crutches",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "orthotic",
                        "label": "Orthotic devices",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "prosthetic",
                        "label": "Prosthetic devices",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "scooter",
                        "label": "Scooters",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "walker",
                        "label": "Walkers",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "wheelchair",
                        "label": "Wheelchairs",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "captioning",
                        "label": "Closed captioning",
                        "groupValue": "hearing",
                    },
                    {
                        "value": "hearingAid",
                        "label": "Hearing aids",
                        "groupValue": "hearing",
                    },
                    {
                        "value": "alarmLight",
                        "label": "Indicator/alarm lights",
                        "groupValue": "hearing",
                    },
                    {
                        "value": "cognitiveAids",
                        "label": "Cognitive aids",
                        "groupValue": "computer",
                    },
                    {
                        "value": "screenEnlarge",
                        "label": "Screen enlargement applications",
                        "groupValue": "computer",
                    },
                    {
                        "value": "screenReader",
                        "label": "Screen readers",
                        "groupValue": "computer",
                    },
                    {
                        "value": "voiceRecognition",
                        "label": "Voice recognition programs",
                        "groupValue": "computer",
                    },
                    {
                        "value": "adaptSwitch",
                        "label": "Adaptive switches",
                        "groupValue": "building",
                    },
                    {
                        "value": "grabBar",
                        "label": "Grab bars",
                        "groupValue": "building",
                    },
                    {
                        "value": "ramp",
                        "label": "Ramps",
                        "groupValue": "building",
                    },
                    {
                        "value": "wideDoor",
                        "label": "Wider doorways",
                        "groupValue": "building",
                    },
                    {
                        "value": "other",
                        "label": "Other assistive device",
                        "groupValue": "other",
                    },
                ],
            },
            "expression_properties": {
                "template_options.options": 'field.templateOptions.allOptions.filter(t => t.groupValue === "other" || t.groupValue === model.type_group)',
                "model.type": 'model.type_group === "other" ? "other" : (field.templateOptions.options.find(o => o.value === model.type) ? model.type : null)',
            },
        },
    )
    type_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Enter assistive device",
                "required": True,
            },
            "hide_expression": type_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + type_other_hide_expression},
        },
    )
    timeframe: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "current", "label": "Currently using"},
                    {"value": "past", "label": "Used in the past"},
                    {"value": "futureInterest", "label": "Interested in using"},
                ],
            },
        },
    )
    notes: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4,
            "type": "textarea",
            "template_options": {
                "label": "Notes on use and/or issues with assistive device",
                "required": False,
            },
        },
    )

    def get_field_groups(self):
        return {
            "type": {
                "fields": ["type_group", "type", "type_other"],
                "display_order": 1,
                "wrappers": ["card"],
                "template_options": {"label": "Type of assistive device"},
            }
        }


class ChainQuestionnaire(Base, QuestionnaireMixin):
    __tablename__ = "chain_questionnaire"
    __label__ = "SkillSTAR Chain Questionnaire"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    sessions: Mapped[list["ChainSession"]] = relationship(
        back_populates="chain_questionnaire", cascade="all, delete-orphan"
    )


class ChainSession(Base, QuestionnaireMixin):
    """
    SkillStar: Chain Session
    """

    __tablename__ = "chain_session"
    __label__ = "SkillSTAR Chain Session"
    __no_export__ = True  # This will be transferred as a part of a parent class
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)
    chain_questionnaire_id: Mapped[int] = mapped_column(ForeignKey("chain_questionnaire.id", ondelete="CASCADE"))
    chain_questionnaire: Mapped["ChainQuestionnaire"] = relationship(back_populates="sessions")
    step_attempts: Mapped[list["ChainSessionStep"]] = relationship(
        "ChainSessionStep",
        backref=backref("chain_session", lazy="joined"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    date: Mapped[datetime] = mapped_column(
        default=func.now(),
        info={
            "display_order": 1,
            "type": "datepicker",
            "template_options": {
                "required": True,
                "label": "Session Date",
            },
        },
    )

    completed: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 2,
            "type": "radio",
            "template_options": {
                "required": True,
                "label": "Session Complete?",
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    session_type: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2,
            "type": "radio",
            "template_options": {
                "required": True,
                "label": "Session Type",
                "options": [
                    {"value": "training", "label": "Training"},
                    {"value": "probe", "label": "Probe"},
                    {"value": "booster", "label": "Booster"},
                ],
            },
        },
    )


class ChallengingBehavior(Base, QuestionnaireMixin):
    __tablename__ = "challenging_behavior"
    __label__ = "ChallengingBehavior"
    __no_export__ = True  # This will be transferred as a part of a parent class

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    chain_session_step_id: Mapped[int] = mapped_column(ForeignKey("chain_session_step.id", ondelete="CASCADE"))
    time: Mapped[datetime] = mapped_column(
        default=func.now(),
        info={
            "display_order": 1,
            "type": "datepicker",
            "template_options": {
                "label": "Time challenging behavior occurred",
            },
        },
    )

    def get_field_groups(self):
        info = {}
        return info


class ChainSessionStep(Base, QuestionnaireMixin):
    __tablename__ = "chain_session_step"
    __label__ = "ChainSessionStep"
    __no_export__ = True  # This will be transferred as a part of a parent class
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 1
    training_session_hide_expression = '!(model.session_type && (model.session_type === "training"))'
    focus_step_hide_expression = "!model.was_focus_step"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    chain_session_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chain_session.id", ondelete="CASCADE"))
    chain_step_id: Mapped[int] = mapped_column(
        ForeignKey("chain_step.id", ondelete="CASCADE"),
        info={
            "display_order": 1,
            "type": "select",
            "template_options": {
                "required": True,
                "label": "Task",
                "options": [],
            },
        },
    )

    # @declared_attr
    # def chain_step_id(self) -> Mapped[int]:
    #     options = []
    #     try:
    #         chain_steps = session.query(ChainStep).all()
    #         sorted_steps = sorted(chain_steps, key=lambda chain_step: chain_step.id)
    #         options = [{"value": s.id, "label": s.instruction} for s in sorted_steps]
    #     except:
    #         pass
    #
    #     return mapped_column(
    #         "chain_step_id",
    #         Integer,
    #         ForeignKey("chain_step.id"),
    #         info={
    #             "display_order": 1,
    #             "type": "select",
    #             "template_options": {
    #                 "required": True,
    #                 "label": "Task",
    #                 "options": options,
    #             },
    #         },
    #     )

    date: Mapped[datetime] = mapped_column(
        default=func.now(),
        info={
            "display_order": 2,
            "type": "datepicker",
            "template_options": {
                "required": True,
                "label": "Step Date",
            },
        },
    )

    was_focus_step: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Focus Step",
                "required": True,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
            "hide_expression": training_session_hide_expression,
            "expression_properties": {"template_options.required": "!" + training_session_hide_expression},
        },
    )

    target_prompt_level: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "What prompt level was targeted for the focus step?",
                "required": True,
                "options": [
                    {"value": "none", "label": "No Prompt (Independent)"},
                    {"value": "shadow", "label": "Shadow Prompt (approximately one inch)"},
                    {"value": "partial_physical", "label": "Partial Physical Prompt (thumb and index finger)"},
                    {"value": "full_physical", "label": "Full Physical Prompt (hand-over-hand)"},
                ],
            },
            "hide_expression": focus_step_hide_expression,
            "expression_properties": {"template_options.required": "!" + focus_step_hide_expression},
        },
    )

    status: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 5,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Step Status",
                "required": True,
                "options": [
                    {"value": "not_yet_started", "label": "Not yet started"},
                    {"value": "not_complete", "label": "Not complete"},
                    {"value": "focus", "label": "Focus"},
                    {"value": "mastered", "label": "Mastered"},
                    {"value": "booster_needed", "label": "Booster needed"},
                    {"value": "booster_mastered", "label": "Booster mastered"},
                ],
            },
        },
    )

    completed: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 6,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Task Complete?",
                "required": True,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    was_prompted: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 7,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Was Prompted?",
                "required": True,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    prompt_level: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 8,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "What prompt did you use to complete the step?",
                "required": True,
                "options": [
                    {"value": "none", "label": "No Prompt (Independent)"},
                    {"value": "shadow", "label": "Shadow Prompt (approximately one inch)"},
                    {"value": "partial_physical", "label": "Partial Physical Prompt (thumb and index finger)"},
                    {"value": "full_physical", "label": "Full Physical Prompt (hand-over-hand)"},
                ],
            },
        },
    )

    had_challenging_behavior: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 9,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Challenging Behavior?",
                "required": True,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    reason_step_incomplete: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 10,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "What was the primary reason for failing to complete the task?",
                "required": True,
                "options": [
                    {"value": "lack_of_attending", "label": "Lack of Attending"},
                    {"value": "challenging_behavior", "label": "Challenging Behavior"},
                    {"value": "sensory_issues", "label": "Sensory Issues(materials are aversive)"},
                    {"value": "other", "label": "Other"},
                ],
            },
        },
    )

    challenging_behaviors: Mapped[list["ChallengingBehavior"]] = relationship()

    num_stars: Mapped[Optional[int]]


#
# ChainSession.step_attempts = relationship(
#     "ChainSessionStep",
#     backref=backref("chain_session", lazy="joined"),
#     cascade="all, delete-orphan",
#     passive_deletes=True,
# )


def _get_chain_session_field_groups(_self):
    return {
        "step_attempts": {
            "type": "repeat",
            "display_order": 3,
            "wrappers": ["card"],
            "repeat_class": ChainSessionStep,
            "template_options": {
                "label": "Which tasks were attempted?",
                "description": "Add a step",
            },
            "expression_properties": {},
        },
    }


ChainSession.get_field_groups = _get_chain_session_field_groups


def _get_chain_session_step_field_groups(_self):
    return {
        "challenging_behaviors": {
            "type": "repeat",
            "display_order": 11,
            "wrappers": ["card"],
            "repeat_class": ChallengingBehavior,
            "template_options": {
                "label": "",
                "description": "Add a challenging behavior",
            },
        },
    }


ChainSessionStep.get_field_groups = _get_chain_session_step_field_groups


def _get_chain_questionnaire_field_groups(_self):
    return {
        "sessions": {
            "type": "repeat",
            "display_order": 3,
            "wrappers": ["card"],
            "repeat_class": ChainSession,
            "template_options": {
                "label": "Chain Session",
                "description": "Add a session",
            },
            "expression_properties": {},
        },
    }


ChainQuestionnaire.get_field_groups = _get_chain_questionnaire_field_groups


class ClinicalDiagnosesQuestionnaire(Base, QuestionnaireMixin):
    __tablename__ = "clinical_diagnoses_questionnaire"
    __label__ = "Clinical Diagnosis"
    __question_type__ = ExportService.TYPE_SENSITIVE
    __estimated_duration_minutes__ = 5
    developmental_other_hide_expression = '!(model.developmental && model.developmental.includes("developmentalOther"))'
    mental_health_other_hide_expression = '!(model.mental_health && model.mental_health.includes("mentalHealthOther"))'
    medical_other_hide_expression = '!(model.medical && model.medical.includes("medicalOther"))'
    genetic_other_hide_expression = '!(model.genetic && model.genetic.includes("geneticOther"))'

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)

    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    developmental: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 1.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "intellectual", "label": "Intellectual disability"},
                    {"value": "globalDevelopmental", "label": "Global developmental delay"},
                    {"value": "learning", "label": "Learning disability"},
                    {"value": "speechLanguage", "label": "Speech or language disorder"},
                    {"value": "coordination", "label": "Developmental coordination disorder"},
                    {"value": "deaf", "label": "Deaf/hard of hearing"},
                    {"value": "visual", "label": "Visual impairment"},
                    {"value": "fetalAlcohol", "label": "Fetal alcohol spectrum disorder"},
                    {"value": "developmentalOther", "label": "Other developmental condition"},
                    {"value": "noDisclose", "label": "I choose not to disclose"},
                ],
            },
        },
    )
    developmental_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.2,
            "type": "input",
            "template_options": {
                "label": "Enter developmental condition",
                "required": True,
            },
            "hide_expression": developmental_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + developmental_other_hide_expression},
        },
    )
    mental_health: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 2,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "anxiety", "label": "Anxiety Disorder"},
                    {"value": "adhd", "label": "Attention-deficit/hyperactivity disorder (ADHD)"},
                    {"value": "bipolar", "label": "Bipolar Disorder"},
                    {"value": "depression", "label": "Depression"},
                    {"value": "ocd", "label": "Obsessive compulsive disorder (OCD)"},
                    {"value": "odd", "label": "Oppositional Defiant Disorder (ODD)"},
                    {"value": "ptsd", "label": "Post-traumatic stress disorder (PTSD)"},
                    {"value": "schizophrenia", "label": "Schizophrenia or Psychotic Disorder"},
                    {"value": "tourette", "label": "Tourette Syndrome or Tic Disorder"},
                    {"value": "mentalHealthOther", "label": "Other mental health condition"},
                    {"value": "noDisclose", "label": "I choose not to disclose"},
                ],
            },
        },
    )
    mental_health_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {
                "label": "Enter mental health condition",
                "required": True,
            },
            "hide_expression": mental_health_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + mental_health_other_hide_expression},
        },
    )
    medical: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 3.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "gastrointestinal", "label": "Chronic Gastrointestinal (GI) problems"},
                    {"value": "seizure", "label": "Epilepsy (seizure disorder)"},
                    {"value": "insomnia", "label": "Insomnia (problems falling or staying asleep)"},
                    {"value": "cerebralPalsy", "label": "Cerebral palsy"},
                    {"value": "asthma", "label": "Asthma"},
                    {"value": "earInfections", "label": "Chronic ear infections"},
                    {"value": "medicalOther", "label": "Other health problem"},
                    {"value": "noDisclose", "label": "I choose not to disclose"},
                ],
            },
        },
    )
    medical_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3.2,
            "type": "input",
            "template_options": {
                "label": "Enter medical condition",
                "required": True,
            },
            "hide_expression": medical_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + medical_other_hide_expression},
        },
    )
    genetic: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 4.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "fragileX", "label": "Fragile X syndrome"},
                    {"value": "tuberousSclerosis", "label": "Tuberous Sclerosis"},
                    {"value": "corneliaDeLange", "label": "Cornelia de Lange syndrome"},
                    {"value": "down", "label": "Down syndrome"},
                    {"value": "angelman", "label": "Angelman syndrome"},
                    {"value": "rett", "label": "Rett syndrome"},
                    {"value": "22q11.2deletion", "label": "22q11.2 Deletion syndrome"},
                    {"value": "geneticOther", "label": "Other genetic condition"},
                    {"value": "noDisclose", "label": "I choose not to disclose"},
                ],
            },
        },
    )
    genetic_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4.2,
            "type": "input",
            "template_options": {
                "label": "Enter genetic condition",
                "required": True,
            },
            "hide_expression": genetic_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + genetic_other_hide_expression},
        },
    )

    def get_field_groups(self):
        return {
            "intro": {
                "fields": [],
                "display_order": 0,
                "wrappers": ["help"],
                "template_options": {
                    "label": "",
                    "description": "",
                },
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"Do you CURRENTLY have any of the following diagnoses? (please check all that apply)"',
                            "self_guardian": '"Do you CURRENTLY have any of the following diagnoses? (please check all that apply)"',
                            "dependent": '"Does " + (formState.preferredName || "your child") + " CURRENTLY have any of the following diagnoses? (please check all that apply)"',
                        }
                    },
                    "template_options.description": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"You may choose not to disclose confidential health information, however, this may cause to you to be excluded from some studies."',
                            "self_guardian": '"You may choose not to disclose confidential health information, however, this may cause to you to be excluded from some studies."',
                            "dependent": '"You may choose not to disclose confidential health information, however, this may cause " + (formState.preferredName || "your child") + " to be excluded from some studies."',
                        }
                    },
                },
            },
            "developmental_group": {
                "fields": ["developmental", "developmental_other"],
                "display_order": 1,
                "wrappers": ["card"],
                "template_options": {"label": "Developmental"},
            },
            "mental_health_group": {
                "fields": ["mental_health", "mental_health_other"],
                "display_order": 2,
                "wrappers": ["card"],
                "template_options": {"label": "Mental health"},
            },
            "medical_group": {
                "fields": ["medical", "medical_other"],
                "display_order": 3,
                "wrappers": ["card"],
                "template_options": {"label": "Medical"},
            },
            "genetic_group": {
                "fields": ["genetic", "genetic_other"],
                "display_order": 4,
                "wrappers": ["card"],
                "template_options": {"label": "Genetic Conditions"},
            },
        }


class CurrentBehaviorsMixin(object):
    info = {}
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __label__ = "Current Behaviors"
    __estimated_duration_minutes__ = 5
    academic_difficulty_other_hide_expression = (
        '!(model.academic_difficulty_areas && model.academic_difficulty_areas.includes("other"))'
    )
    has_academic_difficulties_desc = ""
    academic_difficulty_areas_desc = ""

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)

    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))

    @declared_attr
    def has_academic_difficulties(self):
        return mapped_column(
            Boolean,
            info={
                "display_order": 3,
                "type": "radio",
                "template_options": {
                    "label": "Academic Difficulties",
                    "required": False,
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": self.has_academic_difficulties_desc,
                },
            },
        )

    @declared_attr
    def academic_difficulty_areas(self):
        return mapped_column(
            ARRAY(String),
            info={
                "display_order": 4,
                "type": "multicheckbox",
                "template_options": {
                    "type": "array",
                    "label": "Area of difficulty",
                    "required": True,
                    "options": [
                        {"value": "math", "label": "Math"},
                        {"value": "reading", "label": "Reading"},
                        {"value": "writing", "label": "Writing"},
                        {"value": "other", "label": "Other"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": self.academic_difficulty_areas_desc,
                    "template_options.required": "model.has_academic_difficulties",
                },
                "hide_expression": "!(model.has_academic_difficulties)",
                "validators": {"required": "multicheckbox"},
            },
        )

    academic_difficulty_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4.2,
            "type": "input",
            "template_options": {"label": "Enter area of academic difficulty", "required": True},
            "hide_expression": academic_difficulty_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + academic_difficulty_other_hide_expression},
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_field_groups(self):
        return {}


class CurrentBehaviorsDependentQuestionnaire(Base, QuestionnaireMixin, CurrentBehaviorsMixin):
    __tablename__ = "current_behaviors_dependent_questionnaire"

    has_academic_difficulties_desc = (
        '"Does " + (formState.preferredName || "your child") + " have any difficulties with academics?"'
    )
    academic_difficulty_areas_desc = (
        '"What areas of academics are difficult for " + (formState.preferredName || "your child")'
    )
    concerning_behaviors_other_hide_expression = (
        '!(model.concerning_behaviors && model.concerning_behaviors.includes("concerningOther"))'
    )

    dependent_verbal_ability: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "nonVerbal", "label": "Non-verbal"},
                    {"value": "singleWords", "label": "Single Words"},
                    {"value": "phraseSpeech", "label": "Phrase Speech"},
                    {"value": "fluentErrors", "label": "Fluent Speech with grammatical errors"},
                    {"value": "fluent", "label": "Fluent Speech"},
                ],
            },
            "expression_properties": {
                "template_options.label": '(formState.preferredName || "Your child") + "\'s current ' 'verbal ability:"'
            },
        },
    )
    concerning_behaviors: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 2,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "label": "",
                "required": False,
                "options": [
                    {"value": "aggression", "label": "Aggression"},
                    {"value": "anxiety", "label": "Anxiety"},
                    {"value": "destruction", "label": "Destruction of property"},
                    {"value": "hoarding", "label": "Collecting or hoarding objects"},
                    {"value": "elopement", "label": "Elopement (running away or leaving supervision without an adult)"},
                    {"value": "insistRoutine", "label": "Insistence on routines"},
                    {"value": "irritability", "label": "Irritability"},
                    {"value": "pica", "label": "Pica (eating inedible objects)"},
                    {"value": "rectalDig", "label": "Rectal digging"},
                    {"value": "repetitiveWords", "label": "Repetitive actions, sounds, or speech"},
                    {"value": "restrictEating", "label": "Restricted/picky eating"},
                    {"value": "selfInjury", "label": "Self-injury"},
                    {"value": "soiling", "label": "Soiling property (through urination or fecal smearing)"},
                    {"value": "spitting", "label": "Spitting"},
                    {"value": "screaming", "label": "Screaming"},
                    {"value": "stealing", "label": "Stealing"},
                    {"value": "verbalAggression", "label": "Verbal aggression (profanity or verbal threats)"},
                    {"value": "tantrums", "label": "Tantrums"},
                    {"value": "noDisclose", "label": "I choose not to disclose"},
                    {"value": "concerningOther", "label": "Other"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"Does " + (formState.preferredName || "your child") + '
                '" currently engage in the following behaviors of concern?"'
            },
        },
    )
    concerning_behaviors_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {
                "label": "Enter concerning behavior",
                "required": True,
            },
            "hide_expression": concerning_behaviors_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + concerning_behaviors_other_hide_expression},
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_field_groups(self):
        return super().get_field_groups()


class CurrentBehaviorsSelfQuestionnaire(Base, QuestionnaireMixin, CurrentBehaviorsMixin):
    __tablename__ = "current_behaviors_self_questionnaire"

    has_academic_difficulties_desc = '"Do you have any difficulties with academics?"'
    academic_difficulty_areas_desc = '"What areas of academics are difficult for you?"'

    self_verbal_ability: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "label": "How do you best communicate?",
                "required": False,
                "options": [
                    {"value": "verbal", "label": "Verbally"},
                    {"value": "nonVerbal", "label": "Non-verbally"},
                    {
                        "value": "AACsystem",
                        "label": "An alternative and augmentative communication (AAC) system "
                        "(e.g., Picture exchange, sign language, ipad, etc)",
                    },
                ],
            },
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_field_groups(self):
        return super().get_field_groups()


class DemographicsQuestionnaire(Base, QuestionnaireMixin):
    __tablename__ = "demographics_questionnaire"
    __label__ = "Demographics"
    __question_type__ = ExportService.TYPE_SENSITIVE
    __estimated_duration_minutes__ = 8
    gender_identity_other_hide_expression = '!(model.gender_identity && (model.gender_identity === "genderOther"))'
    race_ethnicity_other_hide_expression = '!(model.race_ethnicity && model.race_ethnicity.includes("raceOther"))'

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)

    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    birth_sex: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1,
            "type": "radio",
            "template_options": {
                "required": True,
                "label": {
                    "RELATIONSHIP_SPECIFIC": {
                        "self_participant": "Your sex at birth",
                        "self_guardian": "Your sex at birth",
                        "self_professional": "Your sex at birth",
                    }
                },
                "options": [
                    {"value": "male", "label": "Male"},
                    {"value": "female", "label": "Female"},
                    {"value": "intersex", "label": "Intersex"},
                ],
            },
            "expression_properties": {
                "template_options.label": {
                    "RELATIONSHIP_SPECIFIC": {
                        "dependent": '(formState.preferredName || "your child") + "\'s" ' '+ " sex at birth"',
                    }
                },
            },
        },
    )
    gender_identity: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2.1,
            "type": "select",
            "template_options": {
                "required": True,
                "options": [
                    {"value": "male", "label": "Male"},
                    {"value": "female", "label": "Female"},
                    {"value": "intersex", "label": "Intersex"},
                    {"value": "transgender", "label": "Transgender"},
                    {"value": "genderOther", "label": "Other"},
                    {"value": "no_answer", "label": "Prefer not to answer"},
                ],
                "label": "Your current gender identity:",
            },
            "expression_properties": {
                "template_options.label": {
                    "RELATIONSHIP_SPECIFIC": {
                        "dependent": '(formState.preferredName || "Your child") + "\'s current gender identity"',
                    }
                },
                "template_options.placeholder": {
                    "RELATIONSHIP_SPECIFIC": {
                        "dependent": '"Please select " + (formState.preferredName || "your child") + "\'s gender"',
                    }
                },
            },
        },
    )
    gender_identity_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {
                "label": "Enter gender identity",
                "required": True,
            },
            "hide_expression": gender_identity_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + gender_identity_other_hide_expression},
        },
    )
    race_ethnicity: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 3.1,
            "type": "multicheckbox",
            "template_options": {
                "label": "Race/Ethnicity",
                "type": "array",
                "required": True,
                "options": [
                    {"value": "raceBlack", "label": "Black / African / African American"},
                    {"value": "raceAsian", "label": "Asian / Asian American"},
                    {"value": "raceWhite", "label": "White / Caucasian"},
                    {"value": "raceHispanic", "label": "Hispanic / Latin(o / a)"},
                    {"value": "raceNative", "label": "Native American / Alaskan Native"},
                    {"value": "racePacific", "label": "Pacific Islander"},
                    {"value": "raceNoAnswer", "label": "Prefer not to answer"},
                    {"value": "raceOther", "label": "Other"},
                ],
                "description": "(select all that apply)",
            },
            "validators": {"required": "multicheckbox"},
        },
    )
    race_ethnicity_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3.2,
            "type": "input",
            "template_options": {
                "label": "Enter race/ethnicity",
                "required": True,
            },
            "hide_expression": race_ethnicity_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + race_ethnicity_other_hide_expression},
        },
    )

    def get_field_groups(self):
        return {
            "gender": {
                "fields": ["birth_sex", "gender_identity", "gender_identity_other"],
                "display_order": 2,
                "wrappers": ["card"],
                "template_options": {"label": "Gender"},
            },
            "race": {
                "fields": ["race_ethnicity", "race_ethnicity_other"],
                "display_order": 3,
                "wrappers": ["card"],
                "template_options": {
                    "label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": "What is your race/ethnicity?",
                            "self_guardian": "What is your race/ethnicity?",
                            "self_professional": "What is your race/ethnicity?",
                        }
                    }
                },
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "dependent": '"What is " + (formState.preferredName || "your child") + "\'s" + '
                            '" race/ethnicity?"',
                        }
                    },
                },
            },
        }


class DevelopmentalQuestionnaire(Base, QuestionnaireMixin):
    __tablename__ = "developmental_questionnaire"
    __label__ = "Birth and Developmental History"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)

    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    had_birth_complications: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 1,
            "type": "radio",
            "template_options": {
                "label": "Were there any complications during the pregnancy or delivery?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    birth_complications_description: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Please describe:",
                "required": False,
            },
            "hide_expression": "!model.had_birth_complications",
        },
    )
    when_motor_milestones: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "early", "label": "Early"},
                    {"value": "onTime", "label": "On-time"},
                    {"value": "delayed", "label": "Delayed"},
                    {"value": "notYet", "label": "Not yet acquired"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"When did " + '
                '(formState.preferredName || "Your child") + '
                '" reach their motor developmental milestones '
                '(e.g., walking, crawling, etc.)?"'
            },
        },
    )
    when_language_milestones: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "early", "label": "Early"},
                    {"value": "onTime", "label": "On-time"},
                    {"value": "delayed", "label": "Delayed"},
                    {"value": "notYet", "label": "Not yet acquired"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"When did " + '
                '(formState.preferredName || "Your child") + '
                '" reach their speech/language developmental milestones '
                '(e.g., babbling, using first words and phrases)?"'
            },
        },
    )
    when_toileting_milestones: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "early", "label": "Early"},
                    {"value": "onTime", "label": "On-time"},
                    {"value": "delayed", "label": "Delayed"},
                    {"value": "notYet", "label": "Not yet acquired"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"When did " + '
                '(formState.preferredName || "Your child") + '
                '" reach their toileting milestones (e.g., potty training)?"'
            },
        },
    )

    def get_field_groups(self):
        return {}


class EducationMixin(object):
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5
    school_services_other_hide_expression = (
        '!(model.school_services && model.school_services.includes("servicesOther"))'
    )
    attends_school_desc = ""

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)

    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))

    @declared_attr
    def attends_school(self):
        return mapped_column(
            Boolean,
            info={
                "display_order": 1,
                "type": "radio",
                "template_options": {
                    "label": "Attend a school or program?",
                    "required": False,
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {
                    "template_options.label": self.attends_school_desc,
                },
            },
        )

    school_name: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2,
            "type": "input",
            "template_options": {
                "label": "Name of the school or program",
                "required": False,
            },
            "hide_expression": "!(model.attends_school)",
        },
    )

    @declared_attr
    def school_type(cls):
        return mapped_column(
            String,
            info={
                "display_order": 3,
                "type": "radio",
                "template_options": {
                    "label": "Type of School",
                    "required": False,
                    "options": [
                        {"value": "public", "label": "Public"},
                        {"value": "private", "label": "Private"},
                        {"value": "homeschool", "label": "Home School"},
                    ],
                },
                "expression_properties": {
                    "template_options.label": cls.school_type_desc,
                },
                "hide_expression": "!(model.attends_school)",
            },
        )

    @declared_attr
    def placement_other(cls):
        return mapped_column(
            String,
            info={
                "display_order": 4.3,
                "type": "input",
                "template_options": {
                    "label": "Enter school placement",
                    "required": True,
                },
                "hide_expression": cls.placement_other_hide_expression,
                "expression_properties": {"template_options.required": "!" + cls.placement_other_hide_expression},
            },
        )

    @declared_attr
    def current_grade(cls):
        return mapped_column(
            String,
            info={
                "display_order": 5,
                "type": "input",
                "template_options": {
                    "label": "School grade level",
                    "required": True,
                },
                "hide_expression": cls.current_grade_hide_expression,
                "expression_properties": {"template_options.required": "!" + cls.current_grade_hide_expression},
            },
        )

    @declared_attr
    def school_services(cls):
        return mapped_column(
            ARRAY(String),
            info={
                "display_order": 6.1,
                "type": "multicheckbox",
                "template_options": {
                    "type": "array",
                    "required": False,
                    "options": [
                        {"value": "504mod", "label": "504 Modification Plan"},
                        {"value": "iep", "label": "Individualized Education Program (IEP)"},
                        {"value": "1:1aide", "label": "1:1 aide or paraprofessional in classroom"},
                        {
                            "value": "partTimeInstruction",
                            "label": "Part-time specialized instruction in a resource room or "
                            "special education classroom",
                        },
                        {
                            "value": "fullTimeInstruction",
                            "label": "Full-time specialized instruction in a resource room or "
                            "special education classroom",
                        },
                        {"value": "specializedSchool", "label": "Specialized school for special learning needs"},
                        {"value": "dayTreatment", "label": "Day treatment or residential center"},
                        {
                            "value": "disabilitySupports",
                            "label": "Disability supports services (at college/vocational " "school)",
                        },
                        {"value": "servicesNone", "label": "None of the above"},
                        {"value": "servicesOther", "label": "Other"},
                    ],
                },
                "expression_properties": {
                    "template_options.label": cls.school_services_desc,
                },
                "hide_expression": "!(model.attends_school)",
            },
        )

    school_services_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 6.2,
            "type": "input",
            "template_options": {
                "label": "Describe additional services",
                "required": True,
            },
            "hide_expression": school_services_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + school_services_other_hide_expression},
        },
    )

    def get_field_groups(self):
        return {
            "placement_group": {
                "display_order": 4,
                "wrappers": ["card"],
                "template_options": {"label": "Placement"},
                "hide_expression": "!(model.attends_school)",
            },
            "school_services_group": {
                "fields": ["school_services", "school_services_other"],
                "display_order": 6,
                "wrappers": ["card"],
                "template_options": {"label": "School Services"},
                "hide_expression": "!(model.attends_school)",
            },
        }


class EducationDependentQuestionnaire(Base, QuestionnaireMixin, EducationMixin):
    __tablename__ = "education_dependent_questionnaire"
    __label__ = "Education"

    attends_school_desc = '"Does " + (formState.preferredName || "your child") + " attend school?"'
    school_type_desc = '"Is " + (formState.preferredName || "your child") + "\'s school:"'
    school_services_desc = '"Please check the following services " + (formState.preferredName || "your child") + " currently receives in school (check all that apply):"'
    placement_other_hide_expression = '!(model.dependent_placement && model.dependent_placement === "schoolOther")'
    current_grade_hide_expression = '!(model.dependent_placement && model.dependent_placement === "grades1to12")'

    dependent_placement: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4.2,
            "type": "select",
            "template_options": {
                "label": "",
                "placeholder": "Please select placement",
                "required": False,
                "options": [
                    {"value": "daycare", "label": "Daycare center"},
                    {"value": "preschool", "label": "Preschool"},
                    {"value": "kindergarten", "label": "Kindergarten"},
                    {"value": "grades1to12", "label": "1st through 12th grade, please specify CURRENT GRADE below"},
                    {"value": "vocational", "label": "Vocational school for learning job or life skills"},
                    {"value": "college", "label": "College/university"},
                    {"value": "graduate", "label": "Graduate school"},
                    {"value": "schoolOther", "label": "Other"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"What is " + (formState.preferredName || "your child") + "\'s '
                'current grade/school placement?"',
            },
            "hide_expression": "!(model.attends_school)",
        },
    )

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["placement_group"]["fields"] = ["dependent_placement", "placement_other", "current_grade"]
        return field_groups


class EducationSelfQuestionnaire(Base, QuestionnaireMixin, EducationMixin):
    __tablename__ = "education_self_questionnaire"
    __label__ = "Education"

    attends_school_desc = '"Do you attend an academic program, such as a school, college, or university?"'
    school_type_desc = '"Is this a public school, private school, or are you home schooled?"'
    school_services_desc = '"Please check all school services that you are currently receiving through your academic program (check all that apply):"'
    placement_other_hide_expression = '!(model.self_placement && model.self_placement === "schoolOther")'
    current_grade_hide_expression = '!(model.self_placement && model.self_placement === "highSchool")'

    self_placement: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4.1,
            "type": "select",
            "template_options": {
                "label": "Program Type",
                "placeholder": "Please select program type",
                "required": False,
                "options": [
                    {"value": "highSchool", "label": "High school"},
                    {"value": "vocational", "label": "Vocational school where I am learning job or life skills"},
                    {"value": "college", "label": "College/university"},
                    {"value": "graduate", "label": "Graduate school"},
                    {"value": "schoolOther", "label": "Other"},
                ],
            },
            "hide_expression": "!(model.attends_school)",
        },
    )

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["placement_group"]["fields"] = ["self_placement", "placement_other", "current_grade"]
        return field_groups


class EmploymentQuestionnaire(Base, QuestionnaireMixin):
    __tablename__ = "employment_questionnaire"
    __label__ = "Employment"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 2

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)

    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    is_currently_employed: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 1.1,
            "type": "radio",
            "template_options": {
                "label": "Are you currently employed?",
                "required": False,
                "options": [{"value": True, "label": "Yes"}, {"value": False, "label": "No"}],
            },
        },
    )
    employment_capacity: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.2,
            "type": "radio",
            "default_value": "n/a",
            "template_options": {
                "label": "In what capacity?",
                "required": False,
                "options": [
                    {"value": "fullTime", "label": "Full time (> 35 hours per week)"},
                    {"value": "partTime", "label": "Part time"},
                ],
            },
            "hide_expression": "!(model.is_currently_employed)",
        },
    )
    has_employment_support: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2,
            "type": "radio",
            "template_options": {
                "label": "Receiving Support?",
                "description": "Do you currently receive supports to help you work successfully, such as job coaching "
                "or vocational training?",
                "required": False,
                "options": [
                    {"value": "yes", "label": "Yes"},
                    {"value": "interested", "label": "No, but I am interested"},
                    {"value": "no", "label": "No"},
                ],
            },
        },
    )

    def get_field_groups(self):
        return {}


class EvaluationHistoryMixin(object):
    __question_type__ = ExportService.TYPE_SENSITIVE
    __estimated_duration_minutes__ = 5
    who_diagnosed_other_hide_expression = '!(model.who_diagnosed && (model.who_diagnosed === "diagnosisOther"))'
    where_diagnosed_other_hide_expression = '!(model.where_diagnosed && (model.where_diagnosed === "diagnosisOther"))'

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))

    @declared_attr
    def has_autism_diagnosis(cls):
        return mapped_column(
            Boolean,
            info={
                "display_order": 1,
                "type": "radio",
                "template_options": {
                    "required": True,
                    "label": "Formal Diagnosis?",
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {"template_options.description": cls.has_autism_diagnosis_label},
            },
        )

    @declared_attr
    def self_identifies_autistic(cls):
        return mapped_column(
            Boolean,
            info={
                "display_order": 2,
                "type": "radio",
                "template_options": {
                    "required": False,
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {"template_options.label": cls.self_identifies_autistic_label},
            },
        )

    @declared_attr
    def years_old_at_first_diagnosis(cls):
        return mapped_column(
            Integer,
            info={
                "display_order": 3,
                "type": "input",
                "template_options": {
                    "label": "Age at Diagnosis",
                    "type": "number",
                    "max": 130,
                },
                "expression_properties": {
                    "template_options.description": cls.years_old_at_first_diagnosis_label,
                    "template_options.required": "model.has_autism_diagnosis",
                },
                "hide_expression": "!(model.has_autism_diagnosis)",
                "validation": {
                    "messages": {
                        "max": "Please enter age in years",
                    }
                },
            },
        )

    @declared_attr
    def who_diagnosed(cls):
        return mapped_column(
            String,
            info={
                "display_order": 4,
                "type": "select",
                "template_options": {
                    "label": "First Diagnosed by:",
                    "placeholder": "Please select from these options",
                    "options": [
                        {
                            "value": "pediatrician",
                            "label": "Pediatrician/Developmental pediatrician/Primary care physician",
                        },
                        {"value": "psychiatrist", "label": "Psychiatrist"},
                        {"value": "neurologist", "label": "Neurologist"},
                        {"value": "psychologist", "label": "Psychologist"},
                        {
                            "value": "healthTeam",
                            "label": "Team of healthcare professionals",
                        },
                        {"value": "diagnosisOther", "label": "Other"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": cls.who_diagnosed_label,
                    "template_options.required": "model.has_autism_diagnosis",
                },
                "hide_expression": "!(model.has_autism_diagnosis)",
            },
        )

    who_diagnosed_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 5,
            "type": "input",
            "template_options": {
                "label": "Diagnosed by other?",
                "placeholder": "Please Describe",
                "required": True,
            },
            "hide_expression": who_diagnosed_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + who_diagnosed_other_hide_expression},
        },
    )

    @declared_attr
    def where_diagnosed(cls):
        return mapped_column(
            String,
            info={
                "display_order": 6,
                "type": "radio",
                "className": "vertical-radio-group",
                "template_options": {
                    "label": "Diagnosed At",
                    "placeholder": "Please select from these options",
                    "options": [
                        {
                            "value": "1uvaDp",
                            "label": "UVA Developmental Pediatrics or UVA Child Development and Rehabilitation Center (formerly Kluge Children's Rehabilitation Center, KCRC)",
                        },
                        {"value": "2sjcCse", "label": "Sheila Johnson Center or Curry School of Education"},
                        {"value": "3via", "label": "Virginia Institute of Autism (VIA)"},
                        {"value": "4school", "label": "School system"},
                        {"value": "5evms", "label": "Eastern Virginia Medical School (EVMS)"},
                        {"value": "6chkd", "label": "Children’s Hospital of the Kings Daughters (CHKD)"},
                        {"value": "7cas", "label": "Commonwealth Autism Services (Virginia Commonwealth University)"},
                        {"value": "8vtAc", "label": "Virginia Tech Autism Clinic"},
                        {"value": "9gmu", "label": "George Mason University"},
                        {"value": "10brAac", "label": "Blue Ridge Autism and Achievement Center"},
                        {"value": "11cnh", "label": "Children’s National Hospital"},
                        {
                            "value": "12kki",
                            "label": "Center for Autism and Related Disorders (Kennedy Krieger Institute)",
                        },
                        {"value": "13vcu", "label": "Children’s Hospital of Richmond (VCU)"},
                        {"value": "14vtc", "label": "Virginia Tech Carilion"},
                        {"value": "15centra", "label": "CENTRA Lynchburg"},
                        {"value": "16apg", "label": "Alexandria Pediatrician Group"},
                        {"value": "17cc", "label": "Carilion Clinic"},
                        {"value": "18mwh", "label": "Mary Washington Hospital"},
                        {"value": "19rna", "label": "Roanoke Neurological Associates"},
                        {"value": "20ruac", "label": "Radford University Autism Center"},
                        {"value": "21rcim", "label": "Rimland Center for Integrative Medicine"},
                        {"value": "22occa", "label": "One Child Center for Autism (Williamsburg)"},
                        {"value": "23inova", "label": "INOVA Health System"},
                        {"value": "24sentara", "label": "Sentara Health System"},
                        {"value": "25psv", "label": "Pediatric Specialists of Virginia"},
                        {"value": "diagnosisOther", "label": "Other"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": cls.where_diagnosed_label,
                    "template_options.required": "model.has_autism_diagnosis",
                },
                "hide_expression": "!(model.has_autism_diagnosis)",
            },
        )

    where_diagnosed_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 7,
            "type": "input",
            "template_options": {
                "label": "Where was this diagnosis made?",
                "required": True,
            },
            "hide_expression": where_diagnosed_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + where_diagnosed_other_hide_expression},
        },
    )

    partner_centers_evaluation: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 8.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {
                        "value": "uva",
                        "label": "UVA Developmental Pediatrics or UVA Child Development and Rehabilitation"
                        " Center (formerly Kluge Children's Rehabilitation Center, KCRC)",
                    },
                    {"value": "sjc", "label": "Sheila Johnson Center or Curry School of Education"},
                    {"value": "via", "label": "Virginia Institute of Autism (VIA)"},
                    {"value": "fc", "label": "Faison Center"},
                    {"value": "inova", "label": "INOVA Health System"},
                    {"value": "none", "label": "None of the above"},
                ],
            },
        },
    )

    @declared_attr
    def gives_permission_to_link_evaluation_data(cls):
        return mapped_column(
            Boolean,
            info={
                "display_order": 9,
                "type": "radio",
                "template_options": {
                    "label": "Permission to Link Data",
                    "required": False,
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": cls.gives_permission_to_link_evaluation_data_desc,
                },
                "hide_expression": '!(model.partner_centers_evaluation && (model.partner_centers_evaluation.length > 0) && !model.partner_centers_evaluation.includes("none"))',
            },
        )

    @declared_attr
    def has_iq_test(cls):
        return mapped_column(
            Boolean,
            info={
                "display_order": 10,
                "type": "radio",
                "template_options": {
                    "required": False,
                    "label": "Taken an IQ Test?",
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {
                    "template_options.description": cls.has_iq_test_desc,
                },
            },
        )

    @declared_attr
    def recent_iq_score(cls):
        return mapped_column(
            Integer,
            info={
                "display_order": 11,
                "type": "input",
                "template_options": {
                    "label": "IQ Score",
                    "placeholder": "Please enter the number of the most recent score, if known. Otherwise, leave this field blank.",
                    "type": "number",
                    "max": 200,
                    "min": 0,
                },
                "hide_expression": "!(model.has_iq_test)",
            },
        )

    def get_field_groups(self):
        return {
            "partner_centers": {
                "fields": ["partner_centers_evaluation", "gives_permission_to_link_evaluation_data"],
                "display_order": 8,
                "wrappers": ["card"],
                "template_options": {"label": ""},
                "expression_properties": {},
            }
        }


class EvaluationHistoryDependentQuestionnaire(Base, QuestionnaireMixin, EvaluationHistoryMixin):
    __tablename__ = "evaluation_history_dependent_questionnaire"
    __label__ = "Evaluation History"

    self_identifies_autistic_label = (
        '"Does " + (formState.preferredName || "your child") + " self-identify as having Autism?"'
    )
    has_autism_diagnosis_label = (
        '"Has " + (formState.preferredName || "your child") + " been formally diagnosed with Autism Spectrum Disorder?"'
    )
    years_old_at_first_diagnosis_label = '"How old (in years) was " + (formState.preferredName || "your child") + " when they were first diagnosed with ASD?"'
    who_diagnosed_label = '"Who first diagnosed " + (formState.preferredName || "your child") + " with ASD?"'
    where_diagnosed_label = '"Where did " + (formState.preferredName || "your child") + " receive this diagnosis?"'
    gives_permission_to_link_evaluation_data_desc = '"Do we have your permission to link " + (formState.preferredName + "\'s") + " evaluation data to the UVa Autism Database?"'
    has_iq_test_desc = '"Has " + (formState.preferredName) + " been given an IQ or intelligence test?"'

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["partner_centers"]["expression_properties"]["template_options.label"] = (
            '"Has " + (formState.preferredName || "your child") + '
            '" ever been evaluated at any of the following centers?"'
        )
        return field_groups


class EvaluationHistorySelfQuestionnaire(Base, QuestionnaireMixin, EvaluationHistoryMixin):
    __tablename__ = "evaluation_history_self_questionnaire"
    __label__ = "Evaluation History"

    has_autism_diagnosis_label = '"Have you been formally diagnosed with Autism Spectrum Disorder?"'
    self_identifies_autistic_label = '"Do you have autism?"'
    years_old_at_first_diagnosis_label = '"How old were you (in years) when you were first diagnosed with ASD?"'
    who_diagnosed_label = '"Who first diagnosed you with ASD?"'
    where_diagnosed_label = '"Where did you receive this diagnosis?"'
    gives_permission_to_link_evaluation_data_desc = (
        '"Do we have your permission to link your evaluation data to the UVA Autism Database?"'
    )
    has_iq_test_desc = '"Have you been given an IQ or intelligence test?"'

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["partner_centers"]["template_options"][
            "label"
        ] = "Have you ever been evaluated at any of the following centers?"
        return field_groups


class HomeMixin(object):
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))

    @declared_attr
    def housemates(cls):
        return relationship(
            "Housemate",
            backref=backref(cls.__tablename__, lazy="joined"),
            cascade="all, delete-orphan",
            passive_deletes=True,
        )

    @declared_attr
    def struggle_to_afford(cls):
        return mapped_column(
            Boolean,
            info={
                "display_order": 4,
                "type": "radio",
                "template_options": {
                    "required": False,
                    "label": "Financial Struggles",
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {"template_options.description": cls.struggle_to_afford_desc},
            },
        )

    def get_field_groups(self):
        field_groups = {
            "housemates": {
                "type": "repeat",
                "display_order": 3,
                "wrappers": ["card"],
                "repeat_class": Housemate,
                "template_options": {
                    "label": "Who else lives there?",
                    "description": "Add a housemate",
                },
                "expression_properties": {},
            },
        }
        return field_groups


class HomeDependentQuestionnaire(Base, QuestionnaireMixin, HomeMixin):
    __tablename__ = "home_dependent_questionnaire"
    __label__ = "Home"
    dependent_living_other_hide_expression = (
        '!(model.dependent_living_situation && model.dependent_living_situation.includes("livingOther"))'
    )

    struggle_to_afford_desc = (
        '"Do you or " + (formState.preferredName || "your child") + "\'s other caregivers ever struggle with being '
        'able to afford to pay for household needs, food, or security for the family?"'
    )

    dependent_living_situation: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 2.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": True,
                "label": "Current Living Situation",
                "options": [
                    {"value": "fullTimeGuardian", "label": "With me full-time"},
                    {"value": "partTimeGuardian", "label": "With me part time"},
                    {"value": "otherFamily", "label": "With other parent/guardian/family member "},
                    {"value": "residentialFacility", "label": "Residential facility"},
                    {"value": "groupHome", "label": "Group home"},
                    {"value": "livingOther", "label": "Other (please explain)"},
                ],
            },
            "validators": {"required": "multicheckbox"},
        },
    )
    dependent_living_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {
                "label": "",
                "required": True,
            },
            "hide_expression": dependent_living_other_hide_expression,
            "expression_properties": {
                "template_options.label": '"Please describe "+ (formState.preferredName || "your child") + "\'s current living situation"',
                "template_options.required": "!" + dependent_living_other_hide_expression,
            },
        },
    )

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["dependent_living"] = {
            "fields": ["dependent_living_situation", "dependent_living_other"],
            "display_order": 2,
            "wrappers": ["card"],
            "template_options": {"label": "Current Living Situation"},
            "expression_properties": {
                "template_options.label": '"Where does " + (formState.preferredName || "your child") + " currently '
                'live (select all that apply)?"'
            },
        }
        field_groups["housemates"][
            "hide_expression"
        ] = '((formState.mainModel.dependent_living_situation && formState.mainModel.dependent_living_situation.includes("residentialFacility"))||(formState.mainModel.dependent_living_situation && formState.mainModel.dependent_living_situation.includes("groupHome")))'

        field_groups["housemates"]["expression_properties"] = {
            "template_options.label": '"Who else lives with " + (formState.preferredName || "your child") + "?"'
        }

        return field_groups


class Housemate(Base, QuestionnaireMixin):
    __tablename__ = "housemate"
    __label__ = "Housemate"
    __no_export__ = True  # This will be transferred as a part of a parent class
    relationship_other_hide_expression = '!(model.relationship && (model.relationship === "relationOther"))'

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    home_dependent_questionnaire_id: Mapped[int] = mapped_column(
        ForeignKey("home_dependent_questionnaire.id", ondelete="CASCADE"), nullable=True
    )
    home_self_questionnaire_id: Mapped[int] = mapped_column(
        ForeignKey("home_self_questionnaire.id", ondelete="CASCADE"), nullable=True
    )
    name: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3.1,
            "type": "input",
            "template_options": {"label": "Name", "required": True},
        },
    )
    relationship: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3.2,
            "type": "select",
            "template_options": {
                "required": False,
                "label": "Relationship",
                "placeholder": "Please select",
                "options": [
                    {"value": "bioParent", "label": "Biological Parent"},
                    {"value": "bioSibling", "label": "Biological Sibling"},
                    {"value": "stepParent", "label": "Step Parent"},
                    {"value": "stepSibling", "label": "Step Sibling"},
                    {"value": "adoptParent", "label": "Adoptive Parent"},
                    {"value": "adoptSibling", "label": "Adoptive Sibling"},
                    {"value": "spouse", "label": "Spouse"},
                    {
                        "value": "significantOther",
                        "label": "Significant Other",
                    },
                    {"value": "child", "label": "Child"},
                    {"value": "roommate", "label": "Roommate"},
                    {"value": "paidCaregiver", "label": "Paid Caregiver"},
                    {"value": "relationOther", "label": "Other"},
                ],
            },
            "expression_properties": {
                "template_options.label": {
                    "RELATIONSHIP_SPECIFIC": {
                        "self_participant": '"Relationship to you"',
                        "self_guardian": '"Relationship to you"',
                        "self_professional": '"Relationship to you"',
                        "dependent": '"Relationship to " + (formState.preferredName || "your child")',
                    }
                }
            },
        },
    )
    relationship_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3.3,
            "type": "input",
            "template_options": {
                "label": "Please enter their relationship",
                "required": True,
            },
            "hide_expression": relationship_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + relationship_other_hide_expression},
        },
    )
    age: Mapped[int] = mapped_column(
        info={
            "display_order": 3.4,
            "type": "input",
            "template_options": {
                "label": "Age",
                "type": "number",
                "max": 130,
                "required": True,
            },
            "validation": {
                "messages": {
                    "max": "Please enter age in years",
                }
            },
        },
    )
    has_autism: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 3.5,
            "type": "radio",
            "template_options": {
                "label": "Does this relation have autism?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    def get_field_groups(self):
        return {}


class HomeSelfQuestionnaire(Base, QuestionnaireMixin, HomeMixin):
    __tablename__ = "home_self_questionnaire"
    __label__ = "Home"
    self_living_other_hide_expression = (
        '!(model.self_living_situation && model.self_living_situation.includes("livingOther"))'
    )

    struggle_to_afford_desc = (
        '"Do you ever struggle with being able to afford to pay for household needs, food, or security?"'
    )

    self_living_situation: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 1.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "label": "Current Living Situation",
                "required": True,
                "description": "(select all that apply)",
                "options": [
                    {"value": "alone", "label": "On my own"},
                    {"value": "spouse", "label": "With a spouse or significant other"},
                    {"value": "family", "label": "With my family"},
                    {"value": "roommates", "label": "With roommates"},
                    {"value": "caregiver", "label": "With a paid caregiver"},
                    {"value": "livingOther", "label": "Other"},
                ],
                "validators": {"required": "multicheckbox"},
            },
        },
    )
    self_living_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.2,
            "type": "input",
            "template_options": {
                "label": "Describe your current living situation",
                "required": True,
            },
            "hide_expression": self_living_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + self_living_other_hide_expression},
        },
    )

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["housemates"]["template_options"]["label"] = "Who else lives with you?"
        field_groups["self_living"] = {
            "fields": ["self_living_situation", "self_living_other"],
            "display_order": 1,
            "wrappers": ["card"],
            "template_options": {"label": "Where do you currently live?"},
        }
        return field_groups


class Medication(Base, QuestionnaireMixin):
    __tablename__ = "medication"
    __label__ = "Medication"
    __no_export__ = True  # This will be transferred as a part of a parent class
    symptom_other_hide_expression = '!(model.symptom && (model.symptom === "symptomOther"))'

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    supports_questionnaire_id: Mapped[int] = mapped_column(ForeignKey("supports_questionnaire.id", ondelete="CASCADE"))
    symptom: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1,
            "type": "select",
            "template_options": {
                "label": "Select symptom",
                "placeholder": "Please select",
                "required": True,
                "options": [
                    {"value": "symptomAnxiety", "label": "Anxiety"},
                    {"value": "symptomDepression", "label": "Depression"},
                    {"value": "symptomInsomnia", "label": "Insomnia"},
                    {"value": "symptomADHD", "label": "ADHD"},
                    {"value": "symptomOther", "label": "Other"},
                ],
            },
        },
    )
    symptom_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Enter symptom",
                "required": True,
            },
            "hide_expression": symptom_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + symptom_other_hide_expression},
        },
    )
    name: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2,
            "type": "textarea",
            "template_options": {
                "label": "Name of Medication (if known)",
            },
        },
    )
    notes: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3,
            "type": "textarea",
            "template_options": {
                "label": "Notes on use and/or issues with medication",
                "required": False,
            },
        },
    )

    def get_field_groups(self):
        info = {
            "symptom_group": {
                "fields": ["symptom", "symptom_other"],
                "display_order": 1,
                "wrappers": ["card"],
                "template_options": {"label": ""},
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"Symptom for which you are taking medication"',
                            "self_guardian": '"Symptom for which you are taking medication"',
                            "self_professional": '"Symptom for which you are taking medication"',
                            "dependent": '"Symptom for which " + (formState.preferredName || "your child") + " is taking medication"',
                        }
                    }
                },
            }
        }
        return info


class ProfessionalProfileQuestionnaire(Base, QuestionnaireMixin):
    __tablename__ = "professional_profile_questionnaire"
    __label__ = "Professional Profile"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 2
    professional_identity_other_hide_expression = (
        '!(model.professional_identity && model.professional_identity.includes("profOther"))'
    )
    learning_interests_other_hide_expression = (
        '!(model.learning_interests && model.learning_interests.includes("learnOther"))'
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)

    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    purpose: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1,
            "type": "select",
            "template_options": {
                "label": "For what purposes are you interested in accessing the Autism DRIVE?",
                "placeholder": "Please select",
                "options": [
                    {"value": "profResources", "label": "To learn more about Autism and Autism Resources available"},
                    {"value": "profResearch", "label": "To learn about and engage in research projects"},
                    {"value": "profResourcesAndResearch", "label": "Both"},
                ],
            },
        },
    )
    professional_identity: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 2.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "admin", "label": "Administrator"},
                    {"value": "adaptive", "label": "Adaptive Physical Education Specialist or Teacher"},
                    {"value": "artTher", "label": "Art Therapist"},
                    {"value": "behaviorAnalyst", "label": "Behavior Analyst"},
                    {"value": "audio", "label": "Audiologist"},
                    {"value": "behaviorTher", "label": "Behavior Therapist (e.g., Behavior Support Specialist, RBT)"},
                    {"value": "caseManag", "label": "Case Manager"},
                    {"value": "counselor", "label": "Counselor"},
                    {"value": "diet", "label": "Dietician"},
                    {"value": "directSupp", "label": "Direct Support Professional"},
                    {"value": "dramaTher", "label": "Drama Therapist"},
                    {
                        "value": "earlyInter",
                        "label": "Early Intervention Specialist/Early Intervention Special Educator",
                    },
                    {"value": "inHomeCare", "label": "In-home caregiver"},
                    {"value": "interp", "label": "Interpreter"},
                    {"value": "jobCoach", "label": "Job coach"},
                    {"value": "musicTher", "label": "Music Therapist"},
                    {"value": "nursing", "label": "Nursing professional"},
                    {"value": "OccupatTher", "label": "Occupational Therapist"},
                    {"value": "paraprof", "label": "Paraprofessional"},
                    {"value": "physician", "label": "Physician"},
                    {"value": "physicalTher", "label": "Physical Therapist"},
                    {"value": "psychologist", "label": "Psychologist"},
                    {"value": "psychiatrist", "label": "Psychiatrist"},
                    {"value": "recInstruct", "label": "Recreational instructor"},
                    {"value": "rehabTher", "label": "Rehabilitation Therapist"},
                    {"value": "researcher", "label": "Researcher or Research Assistant"},
                    {"value": "socialWork", "label": "Social Worker"},
                    {"value": "speechLangPath", "label": "Speech Language Pathologist"},
                    {"value": "supportCoord", "label": "Support Coordinator or Specialist"},
                    {"value": "teacherGenEd", "label": "Teacher or teaching assistant, General Education"},
                    {"value": "teacherSpecEd", "label": "Teacher or teaching assistant, Special Education"},
                    {"value": "techSpec", "label": "Technology Specialist"},
                    {"value": "transitCoor", "label": "Transition coordinator"},
                    {"value": "vocationRehab", "label": "Vocational Rehabilitation Specialist"},
                    {"value": "profNoAnswer", "label": "Prefer not to answer"},
                    {"value": "profOther", "label": "Other"},
                ],
            },
        },
    )
    professional_identity_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {
                "label": "Describe professional identity",
                "required": True,
            },
            "hide_expression": professional_identity_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + professional_identity_other_hide_expression},
        },
    )
    learning_interests: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        info={
            "display_order": 3.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "afterSchoolProg", "label": "After-school programs"},
                    {"value": "appliedBehav", "label": "Applied Behavior Analysis (ABA) services"},
                    {"value": "assistiveTech", "label": "Assistive technology and devices"},
                    {"value": "behavManag", "label": "Behavior management"},
                    {"value": "caseManag", "label": "Case management"},
                    {"value": "collegeTransi", "label": "College/University transitions"},
                    {"value": "commAides", "label": "Communication aides"},
                    {"value": "diagServ", "label": "Diagnostic services"},
                    {"value": "eduPract", "label": "Educational practices"},
                    {"value": "effectTher", "label": "Effective therapies"},
                    {"value": "fundingOpt", "label": "Funding options"},
                    {"value": "genCond", "label": "Genetic conditions related to autism"},
                    {"value": "indivEdPlan", "label": "Individualized education plans"},
                    {"value": "indivFamSupp", "label": "Individualized Family Support Plans"},
                    {"value": "indivServPlan", "label": "Individualized Service Plans"},
                    {"value": "insuranceCov", "label": "Insurance coverage"},
                    {"value": "medCondit", "label": "Medical conditions related to autism"},
                    {"value": "mentalHealth", "label": "Mental health"},
                    {"value": "news", "label": "News and current advances in the field"},
                    {"value": "parentAdvoc", "label": "Parent advocacy"},
                    {"value": "pharmTreat", "label": "Pharmacological treatments"},
                    {"value": "resOpAdult", "label": "Residential options for adults with autism"},
                    {"value": "resOpChild", "label": "Residential options for children with autism"},
                    {"value": "therapies", "label": "Therapies"},
                    {"value": "transitionSupp", "label": "Transition-based supports"},
                    {"value": "learnNoAnswer", "label": "Prefer not to answer"},
                    {"value": "learnOther", "label": "Other"},
                ],
            },
        },
    )
    learning_interests_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3.2,
            "type": "input",
            "template_options": {
                "label": "Enter other interests",
                "required": True,
            },
            "hide_expression": learning_interests_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + learning_interests_other_hide_expression},
        },
    )
    currently_work_with_autistic: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 4,
            "type": "radio",
            "template_options": {
                "label": "Do you currently work with a person or people who have autism?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    previous_work_with_autistic: Mapped[Optional[bool]] = mapped_column(
        info={
            "display_order": 4,
            "type": "radio",
            "template_options": {
                "label": "Did you previously work with someone/people who had autism? ",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    length_work_with_autistic: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 5,
            "type": "input",
            "template_options": {
                "label": "In total, how long have you worked with someone/people who have autism? ",
                "required": False,
            },
        },
    )

    def get_field_groups(self):
        return {
            "professional_identity": {
                "fields": ["professional_identity", "professional_identity_other"],
                "display_order": 2,
                "wrappers": ["card"],
                "template_options": {"label": "I am a(n):"},
            },
            "learning_interests": {
                "fields": ["learning_interests", "learning_interests_other"],
                "display_order": 3,
                "wrappers": ["card"],
                "template_options": {"label": "What topics or areas are you interested in learning about? "},
            },
        }


class RegistrationQuestionnaire(Base, QuestionnaireMixin):
    __tablename__ = "registration_questionnaire"
    __label__ = "Registration"
    __question_type__ = ExportService.TYPE_IDENTIFYING
    __estimated_duration_minutes__ = 5

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)

    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    zip_code: Mapped[int]
    relationship_to_autism: Mapped[list[str]] = mapped_column(ARRAY(String))
    relationship_other: Mapped[Optional[str]]
    marketing_channel: Mapped[list[str]] = mapped_column(ARRAY(String))
    marketing_other: Mapped[Optional[str]]
    newsletter_consent: Mapped[bool] = mapped_column(default=False)

    def get_field_groups(self):
        return {}


class SupportsQuestionnaire(Base, QuestionnaireMixin):
    __tablename__ = "supports_questionnaire"
    __label__ = "Supports"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5
    alternative_med_other_hide_expression = '!(model.alternative_med && model.alternative_med.includes("altMedVitaminOther") || model.alternative_med && model.alternative_med.includes("altMedOther"))'

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    time_on_task_ms: Mapped[int] = mapped_column(default=0)

    participant_id: Mapped[int] = mapped_column(ForeignKey("stardrive_participant.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("stardrive_user.id"))
    medications = relationship(
        "Medication",
        backref=backref("supports_questionnaire", lazy="joined"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    alternative_med: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "options": [
                    {"value": "altMedChiropractics", "label": "Chiropractics"},
                    {"value": "altMedB6Mag", "label": "High dosing Vitamin B6 and magnesium"},
                    {"value": "altMedVitaminOther", "label": "Other vitamin supplements"},
                    {"value": "altMedAminoAcids", "label": "Amino Acids"},
                    {"value": "altMedEssFattyAcids", "label": "Essential fatty acids"},
                    {"value": "altMedGlutenFree", "label": "Gluten-free diet"},
                    {"value": "altMedOther", "label": "Other"},
                ],
                "description": "(select all that apply)",
            },
        },
    )
    alternative_med_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Enter other alternative treatment",
                "required": True,
            },
            "hide_expression": alternative_med_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + alternative_med_other_hide_expression},
        },
    )
    therapies = relationship(
        "Therapy",
        backref=backref("supports_questionnaire", lazy="joined"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    assistive_devices = relationship(
        "AssistiveDevice",
        backref=backref("supports_questionnaire", lazy="joined"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    alternative_augmentative = relationship(
        "AlternativeAugmentative",
        backref=backref("supports_questionnaire", lazy="joined"),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def get_field_groups(self):
        return {
            "medications": {
                "type": "repeat",
                "display_order": 1,
                "wrappers": ["card"],
                "repeat_class": Medication,
                "template_options": {
                    "label": "",
                    "description": "Add a medication",
                },
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"Do you take any medications and/or vitamins?"',
                            "self_guardian": '"Do you take any medications and/or vitamins?"',
                            "dependent": '"Does " + (formState.preferredName || "your child")  + " take any medications and/or vitamins?"',
                        }
                    }
                },
            },
            "alternative_med_group": {
                "fields": ["alternative_med", "alternative_med_other"],
                "display_order": 2,
                "wrappers": ["card"],
                "template_options": {"label": ""},
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"Are you receiving any complementary or alternative treatments?"',
                            "self_guardian": '"Are you receiving any complementary or alternative treatments?"',
                            "self_professional": '"Are you receiving any complementary or alternative treatments?"',
                            "dependent": '"Is " + (formState.preferredName || "your child") + " receiving any complementary or alternative treatments?"',
                        }
                    }
                },
            },
            "therapies": {
                "type": "repeat",
                "display_order": 3,
                "wrappers": ["card"],
                "repeat_class": Therapy,
                "template_options": {
                    "label": "",
                    "description": "Add a therapy or service",
                },
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"What kinds of therapies and services do you currently receive?"',
                            "self_guardian": '"What kinds of therapies and services do you currently receive?"',
                            "dependent": '"What kinds of therapies and services does " + (formState.preferredName || "your child")  + " currently receive?"',
                        }
                    }
                },
            },
            "assistive_devices": {
                "type": "repeat",
                "display_order": 4,
                "wrappers": ["card"],
                "repeat_class": AssistiveDevice,
                "template_options": {
                    "label": "",
                    "description": "Add an assistive device",
                },
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"Do you use an assistive device?"',
                            "self_guardian": '"Do you use an assistive device?"',
                            "dependent": '"Does " + (formState.preferredName || "your child")  + " use an assistive device?"',
                        }
                    }
                },
            },
            "alternative_augmentative": {
                "type": "repeat",
                "display_order": 5,
                "wrappers": ["card"],
                "repeat_class": AlternativeAugmentative,
                "template_options": {
                    "label": "",
                    "description": "Add AAC",
                },
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"Do you use an AAC (alternative & augmentative communication) system?"',
                            "self_guardian": '"Do you use an AAC (alternative & augmentative communication) system?"',
                            "dependent": '"Does " + (formState.preferredName || "your child")  + " use an AAC (alternative & augmentative communication) system?"',
                        }
                    }
                },
            },
        }


class Therapy(Base, QuestionnaireMixin):
    __tablename__ = "therapy"
    __label__ = "Therapy or Service"
    __no_export__ = True  # This will be transferred as a part of a parent class
    type_other_hide_expression = '!(model.type && (model.type === "other"))'

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    supports_questionnaire_id: Mapped[int] = mapped_column(ForeignKey("supports_questionnaire.id", ondelete="CASCADE"))
    type: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1,
            "type": "radio",
            "className": "vertical-radio-group",
            "template_options": {
                "label": "Select type",
                "placeholder": "Please select",
                "required": True,
                "options": [
                    {
                        "value": "speechLanguage",
                        "label": "Speech/Language Therapy",
                    },
                    {"value": "occupational", "label": "Occupational Therapy"},
                    {"value": "physical", "label": "Physical Therapy"},
                    {
                        "value": "behavioral",
                        "label": "Behavior Therapy (ABA, Lovaas, Discrete Trial Training)",
                    },
                    {
                        "value": "natDevBehavioral",
                        "label": "Naturalistic Developmental Behavioral (Pivotal Response Training, Early Start Denver Model, JASPER, etc)",
                    },
                    {
                        "value": "developmental",
                        "label": "Developmental or relationship-based Therapy (DIR/Floortime)",
                    },
                    {
                        "value": "family",
                        "label": "Family Therapy and/or counseling",
                    },
                    {
                        "value": "behavioralParent",
                        "label": "Behavioral parent training (non ASD specific)",
                    },
                    {
                        "value": "individual",
                        "label": "Individual counseling or therapy",
                    },
                    {
                        "value": "medication",
                        "label": "Medication management/Psychiatry",
                    },
                    {
                        "value": "socialSkills",
                        "label": "Social skills training",
                    },
                    {
                        "value": "parentEducation",
                        "label": "Parent education workshops",
                    },
                    {
                        "value": "alternativeTreatments",
                        "label": "Complementary or alternative treatments (e.g., vitamin/nutrient supplements, special diet, food restrictions)",
                    },
                    {"value": "other", "label": "Others (please specify)"},
                ],
            },
        },
    )
    type_other: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Enter therapy or service",
                "required": True,
            },
            "hide_expression": type_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + type_other_hide_expression},
        },
    )
    timeframe: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "current", "label": "Currently receiving"},
                    {"value": "past", "label": "Received in the past"},
                    {"value": "futureInterest", "label": "Interested in receiving"},
                ],
            },
        },
    )
    notes: Mapped[Optional[str]] = mapped_column(
        info={
            "display_order": 4,
            "type": "textarea",
            "template_options": {
                "label": "Notes on use and/or issues with therapy or service",
                "required": False,
            },
        },
    )

    def get_field_groups(self):
        info = {
            "type_group": {
                "fields": ["type", "type_other"],
                "display_order": 1,
                "wrappers": ["card"],
                "template_options": {"label": "Type of therapy or service"},
            }
        }
        return info


class ResourceChangeLog(Base):
    __tablename__ = "resource_change_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    user_id: Mapped[int]
    user_email: Mapped[str]
    resource_id: Mapped[int]
    resource_title: Mapped[str]
    last_updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
