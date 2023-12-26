import elasticsearch
import flask_restful
from flask import request, json
from marshmallow import ValidationError

from app.database import session
from app.elastic_index import elastic_index
from app.models import Category, Hit, MapHit
from app.models import MapHit
from app.rest_exception import RestException
from app.schemas import SearchSchema


class SearchEndpoint(flask_restful.Resource):
    def __post__(self, result_types=None):
        request_data = request.get_json()

        # Handle some sloppy category data.
        if "category" in request_data and (not request_data["category"] or not request_data["category"]["id"]):
            del request_data["category"]

        try:
            search = SearchSchema().load(request_data)
        except ValidationError as e:
            raise RestException(RestException.INVALID_OBJECT, details=e.messages)

        try:
            # Overwrite the result types if requested.
            if not search.types and result_types:
                search.types = result_types
            results = elastic_index.search(search)
        except elasticsearch.ApiError as e:
            raise RestException(RestException.ELASTIC_ERROR, details=e.body)

        search.reset()  # zero out any existing counts or data on the search prior to populating.
        search.total = results.hits.total

        if search.map_data_only:
            return self.map_data_only_search_results(search, results)
        else:
            return self.full_search_results(search, results)

    def full_search_results(self, search, results):
        search.category = self.update_category_counts(search.category, results)
        self.update_aggregations(search, results.aggregations)

        search.hits = []
        for hit in results:
            highlights = ""
            if "highlight" in hit.meta:
                highlights = "... ".join(hit.meta.highlight.content)

            search_hit = Hit(
                hit.id,
                hit.content,
                hit.description,
                hit.title,
                hit.type,
                hit.label,
                hit.date,
                hit.last_updated,
                highlights,
                hit.latitude,
                hit.longitude,
                hit.status,
                hit.no_address,
                hit.is_draft,
                hit.post_event_description,
            )
            search.hits.append(search_hit)

        return SearchSchema().dump(search)

    def map_data_only_search_results(self, search, results):
        search.hits = []
        for hit in results:
            if hit.longitude and hit.latitude:
                search_hit = MapHit(hit.id, hit.type, hit.latitude, hit.longitude, hit.no_address)
                search.hits.append(search_hit)
        return SearchSchema().dump(search)

    def update_aggregations(self, search, aggregations):
        for bucket in aggregations.ages.buckets:
            search.add_aggregation("ages", bucket.key, bucket.doc_count, bucket.key in search.ages)
        for bucket in aggregations.languages.buckets:
            search.add_aggregation("languages", bucket.key, bucket.doc_count, bucket.key in search.languages)
        for bucket in aggregations.type.buckets:
            search.add_aggregation("types", bucket.key, bucket.doc_count, bucket.key in search.types)

    # given a results of a search, creates the appropriate category.
    # Also assures that there is a category at the top called "TOP".
    def update_category_counts(self, category, results):
        topic_category = Category(name="Topics")
        if not category:
            category = topic_category
            category.children = (
                session.query(Category)
                .filter(Category.parent_id == None)
                .order_by(Category.display_order)
                .order_by(Category.name.desc())
                .all()
            )
        else:
            c = category
            while c.parent:
                c = c.parent
            c.parent = topic_category

        for child in category.children:
            for bucket in results.aggregations.category.buckets:
                # Remove topic category id from child search path
                child_key: str = child.search_path().replace(f"{topic_category.id},", "")

                if bucket.key == child_key:
                    child.hit_count = bucket.doc_count
        return category

    def post(self):
        return self.__post__()
