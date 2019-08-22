import elasticsearch
import flask_restful
from flask import request, json

from app import elastic_index, RestException
from app.model.search import Facet, FacetCount, Hit
from app.schema.schema import SearchSchema
from typing import List, Dict


class SearchEndpoint(flask_restful.Resource):
    def _post(self, result_types: List[str] = None):
        request_data: Dict = request.get_json()
        print('request_data before', request_data)

        if request_data is not None and request_data['filters'] is not None and result_types is not None:
            filters: List[dict] = list(request_data['filters'])

            if len(filters) > 0:
                for f in filters:
                    if f['field'] == 'Type':
                        has_types = len(f['value']) > 0 and set(f['value']).issubset(set(result_types))
                        if not has_types:  # Filter is empty or contains an item not in result_types
                            f['value'] = list(result_types)
            else:
                request_data['filters'] = [{'field': 'Type', 'value': list(result_types)}]

        print('request_data after', request_data)

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
            for category, hit_count, is_selected in results.facets[
                    facet_name]:
                facet.facetCounts.append(
                    FacetCount(category, hit_count, is_selected))
            search.facets.append(facet)

        search.hits = []
        for hit in results:
            highlights = ""
            if "highlight" in hit.meta:
                highlights = "... ".join(hit.meta.highlight.content)
            hit = Hit(hit.id, hit.content, hit.description, hit.title, hit.type, hit.label, hit.last_updated, highlights, hit.latitude, hit.longitude)
            search.hits.append(hit)

        search_results = SearchSchema().jsonify(search)

        print('search_results: ', search_results)
        return search_results

    def post(self):
        return self._post()
