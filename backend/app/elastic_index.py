from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from dateutil import tz
from elasticsearch import RequestError, Elasticsearch
from elasticsearch_dsl import (
    Date,
    Keyword,
    Text,
    Index,
    analyzer,
    Integer,
    tokenizer,
    Document,
    Double,
    GeoPoint,
    Search,
    A,
    Q,
    Boolean,
    analysis,
)
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MultiMatch, MatchAll, MoreLikeThis
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import session
from config.load import settings

if TYPE_CHECKING:
    from app.models import Resource, Location, Event, Study

    DatabaseObject = Event | Resource | Location | Study

from app.enums import Permission

autocomplete = analyzer(
    "autocomplete",
    tokenizer=tokenizer("ngram", "edge_ngram", min_gram=2, max_gram=15, token_chars=["letter", "digit"]),
    filter=["lowercase"],
)
autocomplete_search = analyzer("autocomplete_search", tokenizer=tokenizer("lowercase"))

english_stem_filter = analysis.token_filter("my_english_filter", name="minimal_english", type="stemmer")
stem_analyzer = analyzer("stem_analyzer", tokenizer=tokenizer("standard"), filter=["lowercase", english_stem_filter])


class StarDocument(Document):
    """
    Star Documents are ElasticSearch documents and can be used to index an Event, Location, Resource, or Study
    """

    type = Keyword()
    label = Keyword()
    id = Integer()
    title = Text()
    date = Date()
    last_updated = Date()
    content = Text(analyzer=stem_analyzer)
    description = Text()
    post_event_description = Text()
    organization_name = Keyword()
    website = Keyword()
    location = Keyword()
    ages = Keyword(multi=True)
    languages = Keyword(multi=True)
    status = Keyword()
    category = Keyword(multi=True)
    latitude = Double()
    longitude = Double()
    geo_point = GeoPoint()
    no_address = Boolean()
    is_draft = Boolean()


class ElasticIndex(object):
    # Initialize the ElasticIndex as a Singleton
    _instance = None

    logger = logging.getLogger("ElasticIndex")
    connection: Elasticsearch
    index_prefix: str
    index_name: str
    index: Index

    def __init__(self):
        ElasticIndex.instance()

    @classmethod
    def instance(cls) -> ElasticIndex:
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.logger.debug("Initializing Elastic Index")
            cls.establish_connection(settings.ELASTIC_SEARCH)
            cls.index_prefix = settings.ELASTIC_SEARCH["index_prefix"]

            cls.index_name = "%s_resources" % cls.index_prefix
            cls.index = Index(cls.index_name)
            cls.index.document(StarDocument)

            try:
                cls.index.create()
            except RequestError as requestError:
                if requestError.error == "resource_already_exists_exception":
                    cls.logger.info("The index already exists.")
                else:
                    cls.logger.fatal("Error Creating Index. ")
                    raise requestError
            except Exception as e:
                cls.logger.info("Failed to create the index(s).  They may already exist." + str(e))

        return cls._instance

    @classmethod
    def establish_connection(cls, es_settings):
        """Establish connection to an ElasticSearch host, and initialize the Submission collection"""
        if es_settings["http_auth_user"] != "":
            cls.connection = connections.create_connection(
                hosts=es_settings["hosts"],
                port=es_settings["port"],
                request_timeout=es_settings["timeout"],
                verify_certs=es_settings["verify_certs"],
                use_ssl=es_settings["use_ssl"],
                http_auth=(es_settings["http_auth_user"], es_settings["http_auth_pass"]),
            )
        else:
            # Don't set http_auth at all for connecting to AWS ElasticSearch or you will
            # get a cryptic message that is darn near ungoogleable.
            cls.connection = connections.create_connection(
                hosts=es_settings["hosts"],
                request_timeout=es_settings["timeout"],
                verify_certs=es_settings["verify_certs"],
                ssl_show_warn=es_settings["use_ssl"],
            )

    @classmethod
    def clear(cls):
        _instance = cls._instance

        try:
            _instance.logger.info("Clearing the index.")
            _instance.index.delete(ignore_unavailable=True)
            _instance.index.create()
        except:
            _instance.logger.error("Failed to delete the indices. They might not exist.")

    @classmethod
    def refresh_and_flush(cls, es_index: Index, flush=True):
        es_index.refresh()

        if flush:
            es_index.flush(force=True, wait_if_ongoing=True)

    @classmethod
    def remove_document(cls, document: DatabaseObject, flush: bool = True):
        obj = cls._instance.get_document(document)
        obj.delete(version=None)

        cls.refresh_and_flush(cls._instance.index, flush)

    @classmethod
    def get_id(cls, document: DatabaseObject):
        return document.__tablename__.lower() + "_" + str(document.id)

    @classmethod
    def get_document(cls, document: DatabaseObject):
        uid = cls._instance.get_id(document)
        return StarDocument.get(id=uid, index=cls._instance.index_name)

    @classmethod
    def update_document(cls, document: DatabaseObject, flush=True, latitude=None, longitude=None):
        # update is the same as add, as it will overwrite.  Better to have code in one place.
        cls._instance.add_document(document, flush, latitude, longitude)

    @classmethod
    def add_document(
        cls,
        document: DatabaseObject,
        flush: bool = True,
        latitude: float = None,
        longitude: float = None,
        post_event_description: str = None,
    ):
        doc = StarDocument(
            id=document.id,
            type=document.__tablename__,
            label=document.__label__,
            title=document.title,
            last_updated=document.last_updated,
            content=document.indexable_content(),
            description=document.description,
            post_event_description=post_event_description,
            organization_name=document.organization_name,
            location=None,
            ages=document.ages,
            status=None,
            category=[],
            latitude=None,
            longitude=None,
            geo_point=None,
        )

        if hasattr(document, "date"):
            doc.date = document.date
        if hasattr(document, "post_event_description"):
            doc.post_event_description = document.post_event_description
        if hasattr(document, "languages"):
            doc.languages = document.languages
        if hasattr(document, "website"):
            doc.website = document.website
        if hasattr(document, "is_draft"):
            doc.is_draft = document.is_draft
        if hasattr(document, "status") and document.status is not None:
            doc.status = document.status.value
        if hasattr(document, "city") and document.city is not None:
            doc.content = doc.content + " " + document.city

        doc.meta.id = cls._instance.get_id(document)

        for cat in document.categories:
            doc.category.extend(cat.all_search_paths())

        if document.__tablename__ == "study":
            doc.title = document.short_title
            doc.description = document.short_description

        if (doc.type in ["location", "event"]) and None not in (latitude, longitude):
            doc.latitude = latitude
            doc.longitude = longitude
            doc.geo_point = dict(lat=latitude, lon=longitude)
            doc.no_address = not document.street_address1

        StarDocument.save(doc, index=cls._instance.index_name)

        cls.refresh_and_flush(cls._instance.index, flush)

    @classmethod
    def load_documents(
        cls, resources: list[Resource], events: list[Event], locations: list[Location], studies: list[Study]
    ):
        print(
            "Loading search records of events, locations, resources, and studies into Elasticsearch index: %s"
            % cls._instance.index_prefix
        )
        for r in resources:
            cls._instance.add_document(r, flush=False)
        for e in events:
            post_event_description = e.post_event_description if hasattr(e, "post_event_description") else None
            cls._instance.add_document(
                e,
                flush=False,
                latitude=e.latitude,
                longitude=e.longitude,
                post_event_description=post_event_description,
            )
        for loc in locations:
            cls._instance.add_document(loc, flush=False, latitude=loc.latitude, longitude=loc.longitude)
        for s in studies:
            cls._instance.add_document(s, flush=False)

        cls.refresh_and_flush(cls._instance.index)

    @classmethod
    def search(cls, search):
        from flask import g
        from app.models import User

        sort = None if search.sort is None else search.sort.translate()

        if not search.words:
            query = MatchAll()
        else:
            query = MultiMatch(query=search.words, fields=["content"])

        elastic_search = (
            Search(index=cls._instance.index_name)
            .doc_type(StarDocument)
            .query(query)
            .highlight("content", type="unified", fragment_size=150)
        )

        elastic_search = elastic_search[search.start : search.start + search.size]

        # Filter results for type, ages, and languages
        if search.types:
            if set(search.types) == {"resource"}:
                # Include past events in resource search results
                search.types.append("event")

            elastic_search = elastic_search.filter("terms", **{"type": search.types})
        if search.ages:
            elastic_search = elastic_search.filter("terms", **{"ages": search.ages})
        if search.languages:
            elastic_search = elastic_search.filter("terms", **{"languages": search.languages})

        if set(search.types) == {"resource", "event"}:
            # Include past events in resource search results
            elastic_search = elastic_search.filter(
                "bool",
                **{
                    "should": [
                        cls._past_events_filter(cls._start_of_day()),  # Past events OR
                        cls._non_events_filter(),  # Date field is empty
                    ]
                },
            )
        elif search.date:
            # Filter results by date
            elastic_search = elastic_search.filter("range", **{"date": {"gte": cls._start_of_day(search.date)}})
        elif set(search.types) == {"event"}:
            elastic_search = elastic_search.filter("bool", **{"should": cls._future_events_filter(cls._start_of_day())})
        else:
            elastic_search = elastic_search.filter("bool", **{"should": cls._default_filter(cls._start_of_day())})

        if search.geo_box:
            elastic_search = elastic_search.filter(
                "geo_bounding_box",
                **{
                    "geo_point": {
                        "top_left": {"lat": search.geo_box.top_left.lat, "lon": search.geo_box.top_left.lon},
                        "bottom_right": {
                            "lat": search.geo_box.bottom_right.lat,
                            "lon": search.geo_box.bottom_right.lon,
                        },
                    }
                },
            )

        if sort is not None:
            elastic_search = elastic_search.sort(sort)

        if "user" in g and g.user:
            user_id = g.user.id
            db_user = (
                session.execute(select(User).options(joinedload(User.participants)).filter_by(id=user_id))
                .unique()
                .scalar_one_or_none()
            )

            if db_user and Permission.edit_resource not in db_user.role.permissions():
                elastic_search = elastic_search.filter(Q("bool", must_not=[Q("match", is_draft=True)]))

            session.close()
        else:
            elastic_search = elastic_search.filter(Q("bool", must_not=[Q("match", is_draft=True)]))

        category_agg_args = {
            "name_or_agg": "terms",
            "field": "category",
            "exclude": ".*\\,.*",
            "size": 25,
        }
        if search.category and search.category.id:
            elastic_search = elastic_search.filter("terms", category=[str(search.category.search_path())])

            # Include all subcategories of the given root-level category.
            if search.category.calculate_level() == 0:
                category_agg_args.update(
                    {
                        "exclude": ".*\\,.*\\,.*",  # Exclude other root-level categories.
                        "include": f"{search.category.id}\\,.*",  # Include root-level category's children.
                    }
                )

            else:
                # All categories.
                category_agg_args.pop("exclude")

                # Include only children of the given 2nd-level category.
                if search.category.calculate_level() == 1:
                    category_agg_args.update({"include": ".*\\,.*\\,.*"})

        elastic_search.aggs.bucket("category", A(**category_agg_args))
        elastic_search.aggs.bucket("type", A("terms", field="type"))
        elastic_search.aggs.bucket("ages", A("terms", field="ages"))
        elastic_search.aggs.bucket("languages", A("terms", field="languages"))

        # KEEPING FOR NOW - THESE WERE THE ORIGINAL FACETS WE HAD SET UP.  WILL NEED TO CONVERT TO AGGREGATIONS
        # IF WE WANT TO KEEP ANY OF THESE.
        # 'Location': elasticsearch_dsl.TermsFacet(field='location'),
        # 'Type': elasticsearch_dsl.TermsFacet(field='label'),
        # 'Age Range': elasticsearch_dsl.TermsFacet(field='age_range'),
        # 'Category': elasticsearch_dsl.TermsFacet(field='category'),
        # 'Organization': elasticsearch_dsl.TermsFacet(field='organization'),
        # 'Status': elasticsearch_dsl.TermsFacet(field='status'),
        # 'Topic': elasticsearch_dsl.TermsFacet(field='topic'),

        # from icecream import ic
        #
        # ic.configureOutput(includeContext=True, contextAbsPath=True)
        #
        # ic(f"{json.dumps(elastic_search.to_dict())}")

        return elastic_search.execute()

    @classmethod
    def more_like_this(cls, item, max_hits=3):
        """Finds all resources related to the given item."""

        query = MoreLikeThis(
            like=[
                # {'_id': ElasticIndex._get_id(item), '_index': cls._instance.index_name},
                item.indexable_content(),
                item.category_names(),
            ],
            # min_term_freq=1,
            # min_doc_freq=2,
            # max_query_terms=12,
            fields=["title", "content", "description", "location", "category", "organization_name", "website"],
        )

        elastic_search = Search(index=cls._instance.index_name).doc_type(StarDocument).query(query)

        elastic_search = elastic_search[0:max_hits]

        # Filter out past events
        elastic_search = elastic_search.filter("bool", **{"should": cls._default_filter(cls._start_of_day())})

        return elastic_search.execute()

    @staticmethod
    def _start_of_day(date=datetime.utcnow().date()) -> str:
        return datetime(date.year, date.month, date.day, tzinfo=tz.tzutc()).isoformat()

    @staticmethod
    def _past_events_filter(d: str):
        """Past events with a non-empty post-event description"""
        return {
            "bool": {
                "filter": [
                    {"terms": {"type": ["event"]}},
                    {"exists": {"field": "post_event_description"}},
                    {"range": {"date": {"lt": d}}},
                ]
            }
        }

    @staticmethod
    def _future_events_filter(d: str):
        """Future events"""
        return {
            "bool": {
                "filter": [
                    {"terms": {"type": ["event"]}},
                    {"range": {"date": {"gte": d}}},
                ]
            }
        }

    @staticmethod
    def _non_events_filter():
        """Non-events (i.e., date field is empty)"""
        return {"bool": {"must_not": {"exists": {"field": "date"}}}}

    @staticmethod
    def _default_filter(d: str):
        """Past events, future events, and non-events"""
        return [
            ElasticIndex._past_events_filter(d),
            ElasticIndex._future_events_filter(d),
            ElasticIndex._non_events_filter(),
        ]


elastic_index = ElasticIndex.instance()
