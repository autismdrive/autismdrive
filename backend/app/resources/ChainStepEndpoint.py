import flask_restful

from app.model.chain_step import ChainStep
from app import RestException, db
from app.schema.chain_step_schema import ChainStepSchema


class ChainStepEndpoint(flask_restful.Resource):
    """Provides latitude and longitude coordinates for the given zip code."""
    schema = ChainStepSchema()

    def get(self, chain_step_id):
        chain_step = db.session.query(ChainStep).filter_by(id=int(chain_step_id)).first()
        if chain_step is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(chain_step)


class ChainStepListEndpoint(flask_restful.Resource):
    """Provides latitude and longitude coordinates for the given zip code."""
    schema = ChainStepSchema(many=True)

    def get(self):
        chain_steps = db.session.query(ChainStep).all()
        if chain_steps is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(chain_steps)
