import flask_restful

from app.model.zip_code import ZipCode
from app import RestException, db
from app.schema.schema import ZipCodeSchema


class ZipCodeCoordsEndpoint(flask_restful.Resource):
    """Provides latitude and longitude coordinates for the given zip code."""
    schema = ZipCodeSchema()

    def get(self, zip_code):
        z = db.session.query(ZipCode).filter_by(zip_code=int(zip_code)).first()
        if z is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(z)
