import datetime

import flask_restful
from flask import request, g
from marshmallow import ValidationError

from app import RestException, db, elastic_index, auth
from app.model.event import Event
from app.model.location import Location
from app.model.resource_change_log import ResourceChangeLog
from app.model.geocode import Geocode
from app.schema.schema import LocationSchema
from app.model.role import Permission
from app.wrappers import requires_permission


class LocationEndpoint(flask_restful.Resource):

    schema = LocationSchema()

    def get(self, id):
        model = db.session.query(Location).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_permission(Permission.delete_resource)
    def delete(self, id):
        location = db.session.query(Location).filter_by(id=id).first()
        location_id = location.id
        location_title = location.title

        if location is not None:
            elastic_index.remove_document(location, 'Location')

        db.session.query(Event).filter_by(id=id).delete()
        db.session.query(Location).filter_by(id=id).delete()
        db.session.commit()
        self.log_update(location_id=location_id, location_title=location_title, change_type='delete')
        return None

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Location).filter_by(id=id).first()
        if instance.zip != request_data['zip'] \
                or instance.street_address1 != request_data['street_address1'] \
                or instance.latitude is None:
            address_dict = {'street': request_data['street_address1'], 'city': request_data['city'],
                            'state': request_data['state'], 'zip': request_data['zip']}
            geocode = Geocode.get_geocode(address_dict=address_dict)
            request_data['latitude'] = geocode['lat']
            request_data['longitude'] = geocode['lng']

        try:
            updated = self.schema.load(request_data, instance=instance)
        except Exception as errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)

        updated.last_updated = datetime.datetime.utcnow()
        db.session.add(updated)
        db.session.commit()
        elastic_index.update_document(updated, 'Location', latitude=updated.latitude, longitude=updated.longitude)
        self.log_update(location_id=updated.id, location_title=updated.title, change_type='edit')
        return self.schema.dump(updated)

    @staticmethod
    def log_update(location_id, location_title, change_type):
        log = ResourceChangeLog(resource_id=location_id, resource_title=location_title, user_id=g.user.id,
                                user_email=g.user.email, type=change_type)
        db.session.add(log)
        db.session.commit()


class LocationListEndpoint(flask_restful.Resource):

    locationsSchema = LocationSchema(many=True)
    locationSchema = LocationSchema()

    def get(self):
        locations = db.session.query(Location).all()
        return self.locationsSchema.dump(locations)

    @auth.login_required
    @requires_permission(Permission.create_resource)
    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.locationSchema.load(request_data)
            address_dict = {'street': load_result.street_address1, 'city': load_result.city,
                            'state': load_result.state, 'zip': load_result.zip}
            geocode = Geocode.get_geocode(address_dict=address_dict)
            load_result.latitude = geocode['lat']
            load_result.longitude = geocode['lng']
            db.session.add(load_result)
            db.session.commit()
            elastic_index.add_document(load_result, 'Location', latitude=load_result.latitude, longitude=load_result.longitude)
            self.log_update(location_id=load_result.id, location_title=load_result.title, change_type='create')
            return self.locationSchema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)

    @staticmethod
    def log_update(location_id, location_title, change_type):
        log = ResourceChangeLog(resource_id=location_id, resource_title=location_title, user_id=g.user.id,
                                user_email=g.user.email, type=change_type)
        db.session.add(log)
        db.session.commit()
