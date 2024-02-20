import copy

import elasticsearch
import flask_restful
from elasticsearch_dsl.response import Response as ElasticsearchResponse, AggResponse
from elasticsearch_dsl.utils import HitMeta
from flask import request
from marshmallow import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import session
from app.elastic_index import elastic_index
from app.models import Category, Hit, MapHit, Search
from app.rest_exception import RestException
from app.schemas import SearchSchema


class SearchEndpoint(flask_restful.Resource):
    def __post__(self, result_types=None) -> Search:
        request_data = request.get_json()

        # Handle some sloppy category data.
        if "category" in request_data and (not request_data["category"] or not request_data["category"]["id"]):
            del request_data["category"]

        try:
            search: Search = SearchSchema().load(request_data)
        except ValidationError as e:
            raise RestException(RestException.INVALID_OBJECT, details=e.messages)

        try:
            # Overwrite the result types if requested.
            if not search.types and result_types:
                search.types = result_types
            results: ElasticsearchResponse = elastic_index.search(search)
        except elasticsearch.ApiError as e:
            raise RestException(RestException.ELASTIC_ERROR, details=e.body)

        search.reset()  # zero out any existing counts or data on the search prior to populating.
        search.total = results.hits.total

        if search.map_data_only:
            return self.map_data_only_search_results(search, results.hits)
        else:
            return self.full_search_results(search, results)

    def highlights_str(self, hit_meta: HitMeta) -> str:
        highlights = ""
        if "highlight" in hit_meta:
            highlights = "... ".join(hit_meta.highlight.content)

        return highlights

    def full_search_results(self, search: Search, results: ElasticsearchResponse) -> Search:
        search.category = self.update_category_counts(search.category, results)
        self.update_aggregations(search, results.aggregations)
        search.hits = [Hit(highlights=self.highlights_str(h.meta), **h.to_dict()) for h in results.hits]
        return SearchSchema().dump(search)

    def map_data_only_search_results(self, search: Search, results: list[Hit]) -> Search:
        search.hits = []
        for hit in results:
            if hit.longitude and hit.latitude:
                search_hit = MapHit(
                    id=hit.id,
                    latitude=hit.latitude,
                    longitude=hit.longitude,
                    no_address=hit.no_address,
                    type=hit.type,
                )
                search.hits.append(search_hit)
        return SearchSchema().dump(search)

    def update_aggregations(self, search: Search, aggregations: AggResponse):
        """Mutates given SearchSchema object with counts for the given aggregations."""
        for bucket in aggregations.ages.buckets:
            search.add_aggregation("ages", bucket.key, bucket.doc_count, bucket.key in search.ages)
        for bucket in aggregations.languages.buckets:
            search.add_aggregation("languages", bucket.key, bucket.doc_count, bucket.key in search.languages)
        for bucket in aggregations.type.buckets:
            search.add_aggregation("types", bucket.key, bucket.doc_count, bucket.key in search.types)

    # given a results of a search, creates the appropriate category.
    # Also assures that there is a category at the top called "TOP".
    def update_category_counts(self, category: Category, results: ElasticsearchResponse):
        topic_category = Category(name="Topics")
        if not category:
            category = topic_category
            category.children = (
                session.execute(
                    select(Category)
                    .options(joinedload(Category.parent))
                    .options(joinedload(Category.children))
                    .filter_by(parent_id=None)
                    .order_by(Category.display_order)
                    .order_by(Category.name.desc())
                )
                .unique()
                .scalars()
                .all()
            )
            session.close()
        else:
            c_id = category.id
            db_category = (
                session.execute(
                    select(Category)
                    .options(joinedload(Category.parent))
                    .options(joinedload(Category.children))
                    .filter_by(id=c_id)
                )
                .unique()
                .scalar_one()
            )
            session.close()

            # Add the Topics bucket to the top of the category tree.
            c = copy.deepcopy(db_category)

            while c.parent:
                c = c.parent

            c.parent = topic_category
            category = copy.deepcopy(c)

        for child in category.children:
            for bucket in results.aggregations.category.buckets:
                # Remove topic category id from child search path
                child_key: str = child.search_path().replace(f"{topic_category.id},", "")

                if bucket.key == child_key:
                    child.hit_count = bucket.doc_count
        return category

    def post(self):
        return self.__post__()
