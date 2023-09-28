import flask_restful

from app.database import session
from app.model.zip_code import ZipCode
from app.rest_exception import RestException
from app.schema.schema import ZipCodeSchema


class ZipCodeCoordsEndpoint(flask_restful.Resource):
    """Provides latitude and longitude coordinates for the given zip code."""

    schema = ZipCodeSchema()

    def get(self, id):
        z = session.query(ZipCode).filter_by(id=int(id)).first()
        if z is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(z)
