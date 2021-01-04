import datetime

import flask_restful
from flask import request

from app import RestException, db, auth
from app.model.chain_step import ChainStep
from app.model.role import Permission
from app.schema.chain_step_schema import ChainStepSchema
from app.wrappers import requires_permission


class ChainStepEndpoint(flask_restful.Resource):
    """SkillSTAR Chain Step"""
    schema = ChainStepSchema()

    def get(self, chain_step_id):
        chain_step = db.session.query(ChainStep).filter_by(id=int(chain_step_id)).first()
        if chain_step is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(chain_step)

    @auth.login_required
    @requires_permission(Permission.data_admin)
    def put(self, chain_step_id):
        """Modifies an existing Chain Step, or adds one if none exists."""
        request_data = request.get_json()
        instance = db.session.query(ChainStep).filter_by(id=chain_step_id).first()
        try:
            if instance is None:
                # New step
                updated_step = self.schema.load(request_data)
                updated_step.name = 'toothbrushing_' + f'{(updated_step.id + 1):02}'
            else:
                updated_step = self.schema.load(request_data, instance=instance, session=db.session)
        except Exception as e:
            raise RestException(RestException.INVALID_OBJECT, details=e)
        updated_step.last_updated = datetime.datetime.utcnow()
        db.session.add(updated_step)
        db.session.commit()
        return self.schema.dump(updated_step)


class ChainStepListEndpoint(flask_restful.Resource):
    """SkillSTAR Chain Steps"""
    schema = ChainStepSchema(many=True)

    def get(self):
        chain_steps = db.session.query(ChainStep).all()
        if chain_steps is None:
            raise RestException(RestException.NOT_FOUND)

        sorted_steps = sorted(chain_steps, key=lambda i: i['id'])
        return self.schema.dump(sorted_steps)
