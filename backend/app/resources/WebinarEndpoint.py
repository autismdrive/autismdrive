import datetime

import flask_restful
from flask import request, g
from marshmallow import ValidationError

from app import RestException, db, elastic_index, auth
from app.model.webinar import Webinar
from app.model.resource_change_log import ResourceChangeLog
from app.model.geocode import Geocode
from app.model.webinar_user import WebinarUser
from app.schema.schema import WebinarSchema
from app.model.role import Permission
from app.wrappers import requires_permission


class WebinarEndpoint(flask_restful.Resource):

    schema = WebinarSchema()

    def get(self, id):
        model = db.session.query(Webinar).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_permission(Permission.delete_resource)
    def delete(self, id):
        webinar = db.session.query(Webinar).filter_by(id=id).first()
        webinar_id = webinar.id
        webinar_title = webinar.title

        if webinar is not None:
            elastic_index.remove_document(webinar)

        db.session.query(WebinarUser).filter_by(webinar_id=id).delete()
        db.session.query(Webinar).filter_by(id=id).delete()
        db.session.commit()
        self.log_update(webinar_id=webinar_id, webinar_title=webinar_title, change_type='delete')
        return None

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(Webinar).filter_by(id=id).first()
        if instance.zip != request_data['zip'] \
                or instance.street_address1 != request_data['street_address1']\
                or instance.latitude is None:
            address_dict = {'street': request_data['street_address1'], 'city': request_data['city'],
                            'state': request_data['state'], 'zip': request_data['zip']}
            geocode = Geocode.get_geocode(address_dict=address_dict)
            request_data['latitude'] = geocode['lat']
            request_data['longitude'] = geocode['lng']
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.now()
        db.session.add(updated)
        db.session.commit()
        elastic_index.update_document(updated, latitude=updated.latitude, longitude=updated.longitude)
        self.log_update(webinar_id=updated.id, webinar_title=updated.title, change_type='edit')
        return self.schema.dump(updated)

    @staticmethod
    def log_update(webinar_id, webinar_title, change_type):
        log = ResourceChangeLog(resource_id=webinar_id, resource_title=webinar_title, user_id=g.user.id,
                                user_email=g.user.email, type=change_type)
        db.session.add(log)
        db.session.commit()


class WebinarListEndpoint(flask_restful.Resource):

    webinarsSchema = WebinarSchema(many=True)
    webinarSchema = WebinarSchema()

    def get(self):
        webinars = db.session.query(Webinar).all()
        return self.webinarsSchema.dump(webinars)

    @auth.login_required
    @requires_permission(Permission.create_resource)
    def post(self):
        request_data = request.get_json()
        try:
            load_result = self.webinarSchema.load(request_data).data
            address_dict = {'street': load_result.street_address1, 'city': load_result.city,
                            'state': load_result.state, 'zip': load_result.zip}
            geocode = Geocode.get_geocode(address_dict=address_dict)
            load_result.latitude = geocode['lat']
            load_result.longitude = geocode['lng']
            db.session.add(load_result)
            db.session.commit()
            elastic_index.add_document(load_result, latitude=load_result.latitude, longitude=load_result.longitude)
            self.log_update(webinar_id=load_result.id, webinar_title=load_result.title, change_type='create')
            return self.webinarSchema.dump(load_result)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=load_result.errors)

    @staticmethod
    def log_update(webinar_id, webinar_title, change_type):
        log = ResourceChangeLog(resource_id=webinar_id, resource_title=webinar_title, user_id=g.user.id,
                                user_email=g.user.email, type=change_type)
        db.session.add(log)
        db.session.commit()
