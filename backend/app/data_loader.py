from app.model.admin_note import AdminNote
from app.model.age_range import AgeRange
from app.model.category import Category
from app.model.investigator import Investigator
from app.model.organization import Organization
from app.model.participant import Participant
from app.model.event import Event
from app.model.location import Location
from app.model.resource import Resource
from app.model.resource_category import ResourceCategory
from app.model.search import Search
from app.model.study import Study, Status
from app.model.study_category import StudyCategory
from app.model.study_investigator import StudyInvestigator
from app.model.study_user import StudyUser
from app.model.user import User
from app import app, db, elastic_index
from sqlalchemy import Sequence
import os
import csv
import googlemaps

from app.model.zip_code import ZipCode


class DataLoader:
    backend_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    default_dir = backend_path + "/example_data"

    "Loads CSV files into the database"
    file = "example_data/resources.csv"

    def __init__(self, directory=default_dir):

        self.category_file = directory + "/categories.csv"
        self.event_file = directory + "/events.csv"
        self.location_file = directory + "/locations.csv"
        self.resource_file = directory + "/resources.csv"
        self.study_file = directory + "/studies.csv"
        self.user_file = directory + "/users.csv"
        self.participant_file = directory + "/participants.csv"
        self.user_participant_file = directory + "/user_participants.csv"
        self.zip_code_coords_file = directory + "/zip_code_coords.csv"
        print("Data loader initialized")

    def load_categories(self):
        with open(self.category_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                parent = self.get_category_by_name(category_name=row[1].strip(), create_missing=True) if row[1] else None
                category = self.get_category_by_name(category_name=row[0].strip(), parent=parent, create_missing=True)
                db.session.add(category)
                db.session.commit()

        print("Categories loaded.  There are now %i categories in the database." % db.session.query(
            Category).count())

    def load_events(self):
        items = []
        with open(self.event_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                org = self.get_org_by_name(row[5]) if row[5] else None
                geocode = self.get_geocode(
                    address_dict={'street': row[8], 'city': row[10], 'state': row[11], 'zip': row[12]},
                    lat_long_dict={'lat': row[15], 'lng': row[16]}
                )
                event = Event(title=row[0], description=row[1], date=row[2], time=row[3], ticket_cost=row[4],
                              organization=org, primary_contact=row[6], location_name=row[7], street_address1=row[8],
                              street_address2=row[9], city=row[10], state=row[11], zip=row[12], website=row[13],
                              phone=row[14], latitude=geocode['lat'], longitude=geocode['lng'])
                items.append(event)
                self.__increment_id_sequence(Resource)

                for i in range(17, len(row)):
                    if row[i] and row[i] is not '':
                        category = self.get_category_by_name(row[i].strip())
                        event_id = event.id
                        category_id = category.id
                        items.append(ResourceCategory(resource_id=event_id, category_id=category_id, type='event'))

        db.session.bulk_save_objects(items)
        db.session.commit()
        print("Events loaded.  There are now %i events in the database." % db.session.query(Event).count())
        print("There are now %i links between events and categories in the database." %
              db.session.query(ResourceCategory).filter(ResourceCategory.type == 'event').count())

    def load_locations(self):
        items = []
        with open(self.location_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers

            for row in reader:
                org = self.get_org_by_name(row[5]) if row[5] else self.get_org_by_name(row[1])

                geocode = self.get_geocode(
                    address_dict={'street': row[7], 'city': row[9], 'state': row[10], 'zip': row[11]},
                    lat_long_dict={'lat': row[16], 'lng': row[17]}
                )

                location = Location(title=row[1], description=row[2], primary_contact=row[6], organization=org,
                                    street_address1=row[7], street_address2=row[8], city=row[9], state=row[10],
                                    zip=row[11], website=row[13], phone=row[15], email=row[14],
                                    latitude=geocode['lat'], longitude=geocode['lng'], ages=[])

                self.__increment_id_sequence(Resource)

                for i in range(28, len(row)):
                    if row[i]:
                        location.ages.extend(AgeRange.get_age_range_for_csv_data(row[i]))

                items.append(location)

                for i in range(18, 27):
                    if row[i] and row[i] is not '':
                        category = self.get_category_by_name(row[i].strip())
                        location_id = location.id
                        category_id = category.id
                        items.append(ResourceCategory(resource_id=location_id, category_id=category_id, type='location'))

        db.session.bulk_save_objects(items)
        db.session.commit()
        print("Locations loaded.  There are now %i locations in the database." % db.session.query(
            Location).filter(Location.type == 'location').count())
        print("There are now %i links between locations and categories in the database." %
              db.session.query(ResourceCategory).filter(ResourceCategory.type == 'location').count())

    def load_resources(self):
        items = []
        with open(self.resource_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                org = self.get_org_by_name(row[4]) if row[4] else None
                resource = Resource(title=row[0], description=row[1], organization=org, website=row[5],
                                    phone=row[6], ages=[])

                for i in range(15, len(row)):
                    if row[i]:
                        resource.ages.extend(AgeRange.get_age_range_for_csv_data(row[i]))

                items.append(resource)
                self.__increment_id_sequence(Resource)

                for i in range(7, 14):
                    if row[i] and row[i] is not '':
                        category = self.get_category_by_name(row[i].strip())
                        resource_id = resource.id
                        category_id = category.id
                        items.append(ResourceCategory(resource_id=resource_id, category_id=category_id, type='resource'))

        db.session.bulk_save_objects(items)
        db.session.commit()
        print("Resources loaded.  There are now %i resources in the database." % db.session.query(
            Resource).filter(Resource.type == 'resource').count())
        print("There are now %i links between resources and categories in the database." %
              db.session.query(ResourceCategory).filter(ResourceCategory.type == 'resource').count())

    def load_studies(self):
        with open(self.study_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                org = self.get_org_by_name(row[4]) if row[4] else None
                study = Study(title=row[0], description=row[1], participant_description=row[2],
                              benefit_description=row[3], organization=org, location=row[5],
                              short_title=row[6], short_description=row[7], image_url=row[8], coordinator_email=row[22],
                              eligibility_url=row[23], ages=[])

                if row[9].strip() == 'Currently Enrolling':
                    study.status = Status.currently_enrolling
                elif row[9].strip() == 'Study In Progress':
                    study.status = Status.study_in_progress
                elif row[9].strip() == 'Results Being Analyzed':
                    study.status = Status.results_being_analyzed
                elif row[9].strip() == 'Study Results Published':
                    study.status = Status.study_results_published

                for i in range(31, len(row)):
                    if row[i]:
                        study.ages.extend(AgeRange.get_age_range_for_csv_data(row[i]))

                db.session.add(study)
                self.__increment_id_sequence(Study)

                for i in range(24, 31):
                    if row[i] and row[i] is not '':
                        category = self.get_category_by_name(row[i].strip())
                        study_id = study.id
                        category_id = category.id
                        study_category = StudyCategory(study_id=study_id, category_id=category_id)
                        db.session.add(study_category)

                for i in [10, 14, 18]:
                    if row[i]:
                        investigator = db.session.query(Investigator).filter(Investigator.name == row[i]).first()
                        if investigator is None:
                            investigator = Investigator(name=row[i], title=row[i+1],
                                                        organization_id=self.get_org_by_name(row[i+2]).id, bio_link=row[i+3])
                        db.session.add(investigator)
                        db.session.commit()
                        study_investigator = StudyInvestigator(study_id=study.id, investigator_id=investigator.id)
                        db.session.add(study_investigator)
            print("Studies loaded.  There are now %i studies in the database." % db.session.query(
                Study).count())
            print("There are now %i links between studies and categories in the database." %
                  db.session.query(StudyCategory).count())
            print("There are now %i study investigators in the database." %
                  db.session.query(Investigator).count())
        db.session.commit()

    def load_users(self):
        with open(self.user_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                user = User(id=row[0], email=row[1], role=row[3], email_verified=True)
                user.password = row[2]
                db.session.add(user)
            print("Users loaded.  There are now %i users in the database." % db.session.query(
                User).count())
        db.session.commit()

    def load_participants(self):
        with open(self.participant_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                participant = Participant(id=row[0], user_id=row[1], relationship=row[2])
                db.session.add(participant)
                self.__increment_id_sequence(Participant)
            print("Participants loaded.  There are now %i participants in the database." % db.session.query(
                Participant).count())
        db.session.commit()

    def load_zip_codes(self):
        items = []
        with open(self.zip_code_coords_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                items.append(ZipCode(id=row[0], latitude=row[1], longitude=row[2]))

        db.session.bulk_save_objects(items)
        db.session.commit()
        print("ZIP codes loaded.  There are now %i ZIP codes in the database." % db.session.query(ZipCode).count())


    def get_org_by_name(self, org_name):
        organization = db.session.query(Organization).filter(Organization.name == org_name).first()
        if organization is None:
            organization = Organization(name=org_name)
            db.session.add(organization)
            db.session.commit()
        return organization

    def get_category_by_name(self, category_name, parent=None, create_missing=False):
        category = db.session.query(Category).filter(Category.name == category_name).first()
        if category is None:
            if create_missing:
                category = Category(name=category_name, parent=parent)
                db.session.add(category)
                db.session.commit()
            else:
                raise(Exception("This category is not defined: " + category_name))
        return category

    def get_geocode(self, address_dict, lat_long_dict):
        api_key = app.config.get('GOOGLE_MAPS_API_KEY')
        gmaps = googlemaps.Client(key=api_key)
        lat = None
        lng = None

        # Check that location has a street address
        if '' not in address_dict.values():

            # Use stored latitude & longitude, if available
            if '' not in lat_long_dict.values():
                lat = lat_long_dict['lat']
                lng = lat_long_dict['lng']

            # Otherwise, look it up using Google Maps API
            else:
                address = ' '.join(address_dict.values())
                geocode_result = gmaps.geocode(address)

                if geocode_result is not None:
                    if geocode_result[0] is not None:
                        loc = geocode_result[0]['geometry']['location']
                        lat = loc['lat']
                        lng = loc['lng']
                        print(address_dict, loc)

        return {'lat': lat, 'lng': lng}

    def build_index(self):
        elastic_index.load_documents(
            resources=db.session.query(Resource).filter(Resource.type == 'resource').all(),
            events=db.session.query(Resource).filter(Resource.type == 'event').all(),
            locations=db.session.query(Resource).filter(Resource.type == 'location').all(),
            studies=db.session.query(Study).all()
        )

    def clear_index(self):
        print("Clearing the index")
        elastic_index.clear()

    def clear(self):
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

    def clear_resources(self):
        db.session.query(AdminNote).delete()
        db.session.query(ResourceCategory).delete()
        db.session.query(StudyUser).delete()
        db.session.query(StudyCategory).delete()
        db.session.query(StudyInvestigator).delete()
        db.session.query(Category).delete()
        db.session.query(Investigator).delete()
        db.session.query(Event).delete()
        db.session.query(Location).delete()
        db.session.query(Resource).delete()
        db.session.query(Study).delete()
        db.session.query(Organization).delete()
        db.session.query(ZipCode).delete()
        db.session.commit()

    def __increment_id_sequence(self, model):
        db.session.execute(Sequence(model.__tablename__ + '_id_seq'))
