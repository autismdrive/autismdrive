import flask_restful

from app.database import session
from app.models import ZipCode
from app.rest_exception import RestException
from app.schemas import ZipCodeSchema


class ZipCodeCoordsEndpoint(flask_restful.Resource):
    """Provides latitude and longitude coordinates for the given zip code."""

    schema = ZipCodeSchema()

    def get(self, zip_code: int):
        z = session.query(ZipCode).filter_by(id=zip_code).first()
        if z is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(z)
