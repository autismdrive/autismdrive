import elasticsearch
import flask_restful
from flask import request

from app import elastic_index, RestException
from app.model.resource import StarResource
from app.model.study import Study
from app.model.training import Training
from app.model.search import Facet, FacetCount, Filter, Search
from app.resources.schema import SearchSchema, StarResourceSchema, StudySchema, TrainingSchema


class SearchEndpoint(flask_restful.Resource):
    def post(self):
        request_data = request.get_json()
        search, errors = SearchSchema().load(request_data)

        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        try:
            results = elastic_index.search_resources(search)
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

        resources = []
        studies = []
        trainings = []
        for hit in results:
            if hit.type == "Resource":
                resource = StarResource.query.filter_by(id=hit.id).first()
                if resource is not None:
                    resources.append(resource)
            elif hit.type == "Study":
                study = Study.query.filter_by(id=hit.id).first()
                if study is not None:
                    studies.append(study)
            elif hit.type == "Training":
                training = Training.query.filter_by(id=hit.id).first()
                if training is not None:
                    trainings.append(training)
        search.resources = StarResourceSchema().dump(resources, many=True).data
        search.resources.extend(StudySchema().dump(studies, many=True).data)
        search.resources.extend(TrainingSchema().dump(trainings, many=True).data)
        return SearchSchema().jsonify(search)
