import elasticsearch
import flask_restful
from flask import request

from app import elastic_index, RestException
from app.model.search import Facet, FacetCount, Hit
from app.resources.schema import SearchSchema


class SearchEndpoint(flask_restful.Resource):
    def post(self):
        request_data = request.get_json()
        search, errors = SearchSchema().load(request_data)

        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        try:
            results = elastic_index.search(search)
        except elasticsearch.ElasticsearchException as e:
            raise RestException(RestException.ELASTIC_ERROR)

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
            highlights = "";
            if "highlight" in hit.meta:
                highlights = "...".join(hit.meta.highlight.content)
            hit = Hit(hit.id, hit.content, hit.title, hit.type, hit.last_updated, highlights)
            search.hits.append(hit)

        return SearchSchema().jsonify(search)
