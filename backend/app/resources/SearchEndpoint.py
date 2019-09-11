import elasticsearch
import flask_restful
from flask import request, json

from app import elastic_index, RestException, db
from app.model.category import Category
from app.model.search import Facet, FacetCount, Hit, Filter
from app.schema.schema import SearchSchema


class SearchEndpoint(flask_restful.Resource):
    def __post__(self, result_types = None):
        request_data = request.get_json()
        has_request_data = request_data is not None
        has_filters = has_request_data and 'filters' in request_data and request_data['filters'] is not None

        if has_filters and result_types is not None:
            filters = list(request_data['filters'])
            if len(filters) > 0:
                for f in filters:
                    if f['field'] == 'type':
                        has_types = len(f['value']) > 0 and set(f['value']).issubset(set(result_types))
                        if not has_types:  # Filter is empty or contains an item not in result_types
                            f['value'] = list(result_types)
            else:
                request_data['filters'] = [{'field': 'type', 'value': list(result_types)}]

        # Handle some sloppy category data.
        if 'category' in request_data and (not request_data['category'] or not request_data['category']['id']):
            del request_data['category']

        search, errors = SearchSchema().load(request_data)

        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        try:
            results = elastic_index.search(search)
        except elasticsearch.ElasticsearchException as e:
            raise RestException(RestException.ELASTIC_ERROR, details=json.dumps(e.info))

        search.total = results.hits.total
        search.facets = []
        search.category = self.update_category_counts(search.category, results)

        search.hits = []
        for hit in results:
            highlights = ""
            if "highlight" in hit.meta:
                highlights = "... ".join(hit.meta.highlight.content)
            hit = Hit(hit.id, hit.content, hit.description, hit.title, hit.type, hit.label, hit.last_updated, highlights, hit.latitude, hit.longitude)
            search.hits.append(hit)

        return SearchSchema().jsonify(search)

    # given a results of a search, creates the appropriate category.
    # Also assures that there is a category at the top called "TOP".
    def update_category_counts(self, category, results):
        if not category:
            category = Category(name="Topics")
            category.children = db.session.query(Category)\
                .filter(Category.parent_id == None)\
                .order_by(Category.name)\
                .all()
        else:
            c = category
            while c.parent:
                c = c.parent
            c.parent = Category(name="Topics")

        for child in category.children:
            for bucket in results.aggregations.terms.buckets:
                if bucket.key == child.search_path():
                    child.hit_count = bucket.doc_count
        return category

    def post(self):
        return self.__post__()
