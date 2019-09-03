import elasticsearch
import flask_restful
from flask import request, json

from app import elastic_index, RestException
from app.model.search import Facet, FacetCount, Hit
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
                    if f['field'] == 'Type':
                        has_types = len(f['value']) > 0 and set(f['value']).issubset(set(result_types))
                        if not has_types:  # Filter is empty or contains an item not in result_types
                            f['value'] = list(result_types)
            else:
                request_data['filters'] = [{'field': 'Type', 'value': list(result_types)}]

        search, errors = SearchSchema().load(request_data)
        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        try:
            results = elastic_index.search(search)
        except elasticsearch.ElasticsearchException as e:
            raise RestException(RestException.ELASTIC_ERROR, details=json.dumps(e.info))

        search.total = results.hits.total
        search.facets = []
        for facet_name in results.facets:
            facet = Facet(facet_name)
            facet.facetCounts = []
            for category, hit_count, is_selected in results.facets[facet_name]:
                if (facet_name != 'Type') or ((result_types is None) or (category in result_types)):
                    facet.facetCounts.append(FacetCount(category, hit_count, is_selected))
            search.facets.append(facet)

        search.hits = []
        for hit in results:
            highlights = ""
            if "highlight" in hit.meta:
                highlights = "... ".join(hit.meta.highlight.content)
            hit = Hit(hit.id, hit.content, hit.description, hit.title, hit.type, hit.label, hit.last_updated, highlights, hit.latitude, hit.longitude)
            search.hits.append(hit)

        return SearchSchema().jsonify(search)

    def post(self):
        return self.__post__()
