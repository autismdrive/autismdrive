from flask import request
from flask.views import MethodView
from sqlalchemy import Integer, cast
from sqlalchemy.exc import IntegrityError

from app.auth import auth
from app.database import session
from app.enums import Permission
from app.models import ChainSessionStep, ChainStep
from app.rest_exception import RestException
from app.schemas import SchemaRegistry
from app.utils import utcnow
from app.wrappers import requires_permission


class ChainStepEndpoint(MethodView):
    """SkillSTAR Chain Step"""

    schema = SchemaRegistry.ChainStepSchema()

    def get(self, chain_step_id):
        chain_step = session.query(ChainStep).filter_by(id=int(chain_step_id)).first()
        if chain_step is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(chain_step)

    @auth.login_required
    @requires_permission(Permission.edit_study)
    def put(self, chain_step_id):
        """Modifies an existing Chain Step, or adds one if none exists."""
        request_data = request.get_json()
        instance = session.query(ChainStep).filter_by(id=cast(chain_step_id, Integer)).first()
        try:
            if instance is None:
                # New step
                updated_step = self.schema.load(request_data)
                updated_step.name = "toothbrushing_" + f"{(updated_step.id + 1):02}"
            else:
                updated_step = self.schema.load(request_data, instance=instance, session=session)
        except Exception as e:
            raise RestException(RestException.INVALID_OBJECT, details=e)
        updated_step.last_updated = utcnow()
        session.add(updated_step)
        session.commit()
        return self.schema.dump(updated_step)

    @auth.login_required
    @requires_permission(Permission.edit_study)
    def delete(self, chain_step_id):
        """Deletes existing Chain Step, but only if there are no Chain Session Steps that refer to it."""
        chain_session_step = (
            session.query(ChainSessionStep)
            .filter(ChainSessionStep.chain_step_id == cast(chain_step_id, Integer))
            .first()
        )

        if chain_session_step is not None:
            raise RestException(
                RestException.CAN_NOT_DELETE,
                details="Cannot delete a Chain Step that has Chain Session data referring to it.",
            )

        try:
            session.query(ChainStep).filter_by(id=cast(chain_step_id, Integer)).delete()
            session.commit()
        except IntegrityError:
            raise RestException(RestException.CAN_NOT_DELETE)
        return "", 204


class ChainStepListEndpoint(MethodView):
    """SkillSTAR Chain Steps"""

    schema = SchemaRegistry.ChainStepSchema(many=True)

    def get(self):
        chain_steps = session.query(ChainStep).all()
        if chain_steps is None:
            raise RestException(RestException.NOT_FOUND)

        sorted_steps = sorted(chain_steps, key=lambda chain_step: chain_step.id)
        return self.schema.dump(sorted_steps)
