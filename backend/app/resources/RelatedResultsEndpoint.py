import elasticsearch
import flask_restful
from flask import request, json, jsonify
from sqlalchemy import cast, Integer, select

from app.database import session
from app.elastic_index import elastic_index
from app.models import Resource, Study
from app.resources.ResourceEndpoint import add_joins_to_statement as add_resource_joins
from app.resources.StudyEndpoint import add_joins_to_statement as add_study_joins
from app.rest_exception import RestException
from app.schemas import SchemaRegistry


class RelatedResultsEndpoint(flask_restful.Resource):
    resources_schema = SchemaRegistry.ResourceSchema(many=True)
    studies_schema = SchemaRegistry.StudySchema(many=True)

    def post(self):
        request_data = request.get_json()
        try:
            is_resource = "resource_id" in request_data.keys()
            item_id = request_data["resource_id"] if is_resource else request_data["study_id"]
            model = Resource if is_resource else Study
            item = session.query(model).filter_by(id=cast(item_id, Integer)).first()
            results = elastic_index.more_like_this(item, max_hits=30)
        except elasticsearch.ElasticsearchException as e:
            raise RestException(RestException.ELASTIC_ERROR, details=json.dumps(e))

        resource_ids = []
        study_ids = []
        max_length = 3
        for hit in results:
            if hit.type == "study":
                same_study = (not is_resource) and (item_id == hit.id)
                if not same_study and len(study_ids) < max_length:
                    study_ids.append(hit.id)
            else:
                same_resource = is_resource and (item_id == hit.id)
                if not same_resource and len(resource_ids) < max_length:
                    resource_ids.append(hit.id)

        resource_statement = add_resource_joins(select(Resource)).filter(Resource.id.in_(resource_ids))
        related_resources = session.execute(resource_statement).unique().scalars().all()

        resource_statement = add_study_joins(select(Study)).filter(Study.id.in_(study_ids))
        related_studies = session.execute(resource_statement).unique().scalars().all()

        return jsonify(
            {
                "resources": self.resources_schema.dump(related_resources),
                "studies": self.studies_schema.dump(related_studies),
            }
        )
