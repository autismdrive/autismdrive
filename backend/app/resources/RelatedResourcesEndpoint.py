import elasticsearch
import flask_restful
from flask import json

from app import elastic_index, RestException, db
from app.model.resource import Resource

# These are actually required.
from app.model.resource_category import ResourceCategory
from app.model.study import Study
from app.model.study_investigator import StudyInvestigator
from app.model.study_category import StudyCategory
from app.model.user import User
from app.schema.schema import ResourceSchema


class RelatedResourcesEndpoint(flask_restful.Resource):

    schema = ResourceSchema(many=True)

    def get(self, id):

        try:
            resource = db.session.query(Resource).filter_by(id=id).first()
            # Overwrite the result types if requested.
            results = elastic_index.more_like_this(resource)
        except elasticsearch.ElasticsearchException as e:
            raise RestException(RestException.ELASTIC_ERROR, details=json.dumps(e.info))

        resource_ids = (hit.id for hit in results)
        related_resources = db.session.query(Resource).filter(Resource.id.in_(resource_ids))

        return self.schema.jsonify(related_resources)

