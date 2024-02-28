import json
from dataclasses import dataclass, KW_ONLY
from datetime import datetime, date
from typing import cast, TypedDict

from marshmallow import Schema

from app.models import Resource, Event, Location, Study

DatabaseObject = Event | Resource | Location | Study


@dataclass()
class DatabaseObjectDict:
    """Union of all possible fields in a Resource, Location, Event, or Study. All fields are optional."""

    _: KW_ONLY
    admin_notes: list[dict] = None
    ages: list[str] = None
    benefit_description: str = None
    categories: list[dict] = None
    city: str = None
    contact_email: str = None
    coordinator_email: str = None
    covid19_categories: list[str] = None
    date: str | datetime = None
    description: str = None
    eligibility_url: str = None
    email: str = None
    id: int = None
    image_url: str = None
    includes_registration: bool = None
    insurance: str = None
    investigators: list[dict] = None
    is_draft: bool = None
    is_uva_education_content: bool = None
    languages: list[str] = None
    last_updated: str | datetime = None
    latitude: float = None
    location: str = None
    location_name: str = None
    longitude: float = None
    max_users: int = None
    num_visits: int = None
    organization_name: str = None
    participant_description: str = None
    phone: str = None
    phone_extension: str = None
    post_event_description: str = None
    post_survey_link: str = None
    primary_contact: str = None
    registered_users: list[dict] = None
    registration_url: str = None
    resource_categories: list[dict] = None
    results_url: str = None
    short_description: str = None
    short_title: str = None
    should_hide_related_resources: str = None
    state: str = None
    status: str = None
    street_address1: str = None
    street_address2: str = None
    study_categories: list[dict] = None
    study_investigators: list[dict] = None
    study_users: list[dict] = None
    survey_url: str = None
    ticket_cost: str = None
    time: str = None
    title: str = None
    type: str = None
    users: list[dict] = None
    video_code: str = None
    webinar_link: str = None
    website: str = None
    zip: str = None
    label: str = None
    content: str = None
    category: list[str] = None
    geo_point: dict = None
    no_address: bool = None

    @classmethod
    def from_dict(cls, d: dict) -> "DatabaseObjectDict":
        import inspect

        kw_dict = {k: v for k, v in d.items() if k in inspect.signature(cls).parameters}
        return cls(**kw_dict)

    @classmethod
    def field_names(cls) -> list[str]:
        import inspect

        return [k for k, v in inspect.signature(cls).parameters.items()]


def indexable_content(item: Resource | Location | Event | Study | DatabaseObjectDict) -> str:
    """
    Returns a single string containing all the indexable text fields
    in the given Resource, Location, Event, or Study, separated by spaces.
    """
    indexable_text = ""

    if hasattr(item, "type") and item.type in ["resource", "location", "event"]:
        indexable_text += category_names(item)

    fields = [
        "short_title",
        "short_description",
        "title",
        "description",
        "post_event_description",
        "insurance",
        "participant_description",
        "benefit_description",
        "location",
        "city",
    ]

    for field in fields:
        if hasattr(item, field):
            value = getattr(item, field)
            if value is not None and len(value) > 0:
                indexable_text += " " + value

    return indexable_text


def category_names(item: Resource | Location | Event | Study) -> str:
    """
    Returns a single string containing all the indexable category fields
    in the given Resource, Location, Event, or Study, separated by spaces.
    """

    cat_text = ""
    for cat in item.categories:
        cat_text = cat_text + " " + cat.name

    fields = ["ages", "languages", "covid19_categories"]

    for field in fields:
        if hasattr(item, field):
            value = getattr(item, field)
            if value is not None and len(value) > 0:
                cat_text += " " + " ".join(value)

    return cat_text


def to_database_object_dict(schema: Schema = None, db_object: DatabaseObject = None) -> DatabaseObjectDict:
    """
    Converts a Resource, Location, Event, or Study object to a DatabaseObjectDict.

    We have to do this to avoid circular imports and stale sessions causing all kinds of downstream problems
    when indexing database objects that have many nested relationships and complicated join behaviors.
    """
    from app.utils.category_utils import all_search_paths

    if schema is None:
        raise ValueError(f"Invalid schema.")

    if db_object is None:
        raise ValueError(f"Invalid db_object.")

    category_search_paths = [all_search_paths(c.id) for c in db_object.categories]
    has_address = (
        hasattr(db_object, "street_address1")
        and db_object.street_address1 is not None
        and db_object.street_address1 != ""
    )

    geo_point = None
    if (
        hasattr(db_object, "latitude")
        and db_object.latitude is not None
        and hasattr(db_object, "longitude")
        and db_object.longitude is not None
    ):
        geo_point = dict(lat=db_object.latitude, lon=db_object.longitude)

    extra_fields = {
        "type": db_object.__tablename__,
        "label": db_object.__label__,
        "content": indexable_content(db_object),
        "category": category_search_paths,
        "geo_point": geo_point,
        "no_address": bool(not has_address),
    }

    all_fields = DatabaseObjectDict.field_names()

    max_depth = 10

    def _parse(value: any, depth: int = 0):
        if depth > max_depth:
            return None

        if isinstance(value, (str, int, float, bool, type(None))):
            return value

        if isinstance(value, (date, datetime)):
            return value.isoformat()

        if isinstance(value, list):
            return [_parse(v, depth + 1) for v in value]

        if isinstance(value, dict):
            return {k: _parse(v, depth + 1) for k, v in value.items() if not k.startswith("_")}

        if hasattr(value, "__dict__"):
            return _parse(value.__dict__, depth + 1)

        try:
            json_obj = json.loads(json.dumps(value, default=str))
            return _parse(json_obj, depth + 1)

        except Exception as e:
            raise ValueError(f"Invalid value: {value} - ", e)

    def _get(field: str, default=None):
        if hasattr(db_object, field):
            value = db_object.__getattribute__(field)
            return _parse(value)
        return default

    dumped = {k: _get(k) for k in all_fields}

    plain_dict = dumped | extra_fields

    return DatabaseObjectDict.from_dict(plain_dict)
