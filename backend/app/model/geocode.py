from app import app, db
from app.model.zip_code import ZipCode
from sqlalchemy.sql.expression import func
import googlemaps


class Geocode:

    @staticmethod
    def get_geocode(address_dict):

        if 'TESTING' in app.config and app.config['TESTING']:
            z = db.session.query(ZipCode).order_by(func.random()).first()
            print("TEST:  Pretending to get the geocode and setting lat/lng to  %s - %s" % (z.latitude, z.longitude))
            return {'lat': z.latitude, 'lng': z.longitude}

        else:
            api_key = app.config.get('GOOGLE_MAPS_API_KEY')
            gmaps = googlemaps.Client(key=api_key)
            lat = None
            lng = None

            # Check that location has at least a zip code
            if address_dict['zip']:

                # Look up the latitude and longitude using Google Maps API
                address = ''
                for value in address_dict:
                    if address_dict[value] is not None:
                        address = address + " " + address_dict[value]
                geocode_result = gmaps.geocode(address)

                if geocode_result is not None:
                    if geocode_result[0] is not None:
                        loc = geocode_result[0]['geometry']['location']
                        lat = loc['lat']
                        lng = loc['lng']
                        print(address_dict, loc)

            return {'lat': lat, 'lng': lng}
