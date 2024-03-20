from sqlalchemy import Select
from sqlalchemy.orm import joinedload, QueryableAttribute
from sqlalchemy.orm.interfaces import LoaderOption
from sqlalchemy.sql.base import ExecutableOption

from app.models import Resource, ResourceCategory, Category, Location, Event, Study, StudyCategory, StudyInvestigator

NestedQueryableAttribute = QueryableAttribute | list["NestedQueryableAttribute"]


def _add_joins_to_statement(
    statement: Select, attrs_list: list[NestedQueryableAttribute] = None, options_list: list[ExecutableOption] = None
) -> Select:
    """
    Adds joins to a select statement

    joins could be a nested list of QueryableAttribute objects OR a list of ExecutableOption objects.

    If the former, the QueryableAttribute objects are wrapped with the joinedload function.
    If the latter, the ExecutableOption objects are added to the statement options without modification.

    [
        Study.study_categories,
            [
                StudyCategory.category,
                [
                    Category.parent,
                    Category.children,
                ],
            ],
        Study.study_investigators,
            [
                StudyInvestigator.investigator,
            ]
        Study.investigators,
    ]

    """

    def _add_nested_joinedloads(_statement, maybe_nested_attr: NestedQueryableAttribute):
        if isinstance(maybe_nested_attr, QueryableAttribute):
            _statement = _statement.options(joinedload(maybe_nested_attr))

        elif isinstance(maybe_nested_attr, list):
            for attr in maybe_nested_attr:
                _add_nested_joinedloads(_statement, attr)

    if attrs_list is not None:
        for attr in attrs_list:
            _add_nested_joinedloads(statement, attr)

    return statement


def add_resource_joins(statement: Select | ExecutableOption) -> Select | LoaderOption:
    return statement.options(
        joinedload(Resource.resource_categories).joinedload(ResourceCategory.category),
        add_cat_joins(joinedload(Resource.categories)),
    )


def add_location_joins(statement: Select | ExecutableOption) -> Select | LoaderOption:
    return statement.options(
        joinedload(Location.resource_categories).joinedload(ResourceCategory.category),
        add_cat_joins(joinedload(Location.categories)),
    )


def add_event_joins(statement: Select | ExecutableOption) -> Select | LoaderOption:
    return statement.options(
        joinedload(Event.resource_categories).joinedload(ResourceCategory.category),
        add_cat_joins(joinedload(Event.categories)),
    )


def add_study_joins(statement: Select | ExecutableOption) -> Select | LoaderOption:
    return statement.options(
        joinedload(Study.study_categories).joinedload(StudyCategory.category),
        add_cat_joins(joinedload(Study.categories)),
        joinedload(Study.study_investigators).joinedload(StudyInvestigator.investigator),
        joinedload(Study.investigators),
    )


def add_cat_joins(statement: Select | ExecutableOption) -> Select | LoaderOption:
    return statement.options(
        joinedload(Category.parent),
        joinedload(Category.children),
        joinedload(Category.resources),
        joinedload(Category.studies),
    )
