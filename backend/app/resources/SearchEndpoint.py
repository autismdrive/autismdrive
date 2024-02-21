import elasticsearch
import flask_restful
from elasticsearch_dsl.response import Response as ElasticsearchResponse, AggResponse
from elasticsearch_dsl.utils import HitMeta
from flask import request
from marshmallow import ValidationError
from sqlalchemy import select

from app.elastic_index import elastic_index
from app.models import Category, Hit, MapHit, Search
from app.rest_exception import RestException
from app.schemas import SchemaRegistry


class SearchEndpoint(flask_restful.Resource):
    def __post__(self, result_types=None) -> Search:
        request_data = request.get_json()

        # Handle some sloppy category data.
        if "category" in request_data and (not request_data["category"] or not request_data["category"]["id"]):
            del request_data["category"]

        try:
            search: Search = SchemaRegistry.SearchSchema().load(request_data)
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
        return SchemaRegistry.SearchSchema().dump(search)

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
        return SchemaRegistry.SearchSchema().dump(search)

    def update_aggregations(self, search: Search, aggregations: AggResponse):
        """Mutates given SchemaRegistry.SearchSchema object with counts for the given aggregations."""
        for bucket in aggregations.ages.buckets:
            search.add_aggregation("ages", bucket.key, bucket.doc_count, bucket.key in search.ages)
        for bucket in aggregations.languages.buckets:
            search.add_aggregation("languages", bucket.key, bucket.doc_count, bucket.key in search.languages)
        for bucket in aggregations.type.buckets:
            search.add_aggregation("types", bucket.key, bucket.doc_count, bucket.key in search.types)

    # given a results of a search, creates the appropriate category.
    # Also assures that there is a category at the top called "TOP".
    def update_category_counts(self, category: Category, results: ElasticsearchResponse):
        from app.resources.CategoryEndpoint import add_joins_to_statement, get_category_by_id
        from app.database import session

        "Make a fake category to hold all the other categories."
        topic_category = Category(id=99999, name="Topics", children=[], parent=None)
        if not category:
            category = topic_category
            category.children = (
                session.execute(
                    add_joins_to_statement(select(Category))
                    .filter_by(parent_id=None)
                    .order_by(Category.display_order)
                    .order_by(Category.name.desc())
                )
                .unique()
                .scalars()
                .all()
            )
        else:
            c_id = category.id
            category = topic_category if c_id == topic_category.id else get_category_by_id(c_id, with_joins=True)

            # Add the Topics bucket to the top of the category tree.
            c = category

            while c and c.parent:
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
