import elasticsearch
import flask_restful
from flask import request, json, jsonify

from app import elastic_index, RestException, db
from app.model.resource import Resource
from app.model.study import Study

# These are actually required.
from app.model.resource_category import ResourceCategory
from app.model.study_investigator import StudyInvestigator
from app.model.study_category import StudyCategory
from app.model.user import User
from app.schema.schema import ResourceSchema, StudySchema


class RelatedResultsEndpoint(flask_restful.Resource):
    resourcesSchema = ResourceSchema(many=True)
    studiesSchema = StudySchema(many=True)

    def post(self):
        request_data = request.get_json()
        try:
            is_resource = 'resource_id' in request_data.keys()
            item_id = request_data['resource_id'] if is_resource else request_data['study_id']
            model = Resource if is_resource else Study
            item = db.session.query(model).filter_by(id=item_id).first()
            results = elastic_index.more_like_this(item, max_hits=30)
        except elasticsearch.ElasticsearchException as e:
            raise RestException(RestException.ELASTIC_ERROR, details=json.dumps(e))

        resource_ids = []
        study_ids = []
        max_length = 3
        for hit in results:
            if hit.type == 'study':
                same_study = ((not is_resource) and (item_id == hit.id))
                if not same_study and len(study_ids) < max_length:
                    study_ids.append(hit.id)
            else:
                same_resource = (is_resource and (item_id == hit.id))
                if not same_resource and len(resource_ids) < max_length:
                    resource_ids.append(hit.id)

        related_resources = db.session.query(Resource).filter(Resource.id.in_(resource_ids))
        related_studies = db.session.query(Study).filter(Study.id.in_(study_ids))

        return jsonify({
            'resources': self.resourcesSchema.dump(related_resources),
            'studies': self.studiesSchema.dump(related_studies),
        })
