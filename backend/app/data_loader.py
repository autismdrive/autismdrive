import csv
import os

import googlemaps
from sqlalchemy import Sequence

from app.elastic_index import elastic_index
from app.enums import Status
from config.load import settings
from .database import session


class DataLoader:
    category_file: str
    event_file: str
    location_file: str
    resource_file: str
    study_file: str
    user_file: str
    participant_file: str
    user_participant_file: str
    zip_code_coords_file: str
    chain_steps_file: str
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
        self.chain_steps_file = directory + "/chain_steps.csv"
        print("Data loader initialized")

    def load_categories(self):
        from .models import Category

        with open(self.category_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                parent = (
                    self.get_category_by_name(category_name=row[1].strip(), create_missing=True) if row[1] else None
                )
                category = self.get_category_by_name(category_name=row[0].strip(), parent=parent, create_missing=True)
                session.add(category)
                session.commit()

        print("Categories loaded.  There are now %i categories in the database." % session.query(Category).count())

    def load_events(self):
        from .models import AgeRange
        from .models import EventUser
        from .models import Event
        from .models import ResourceCategory
        from .models import Resource

        with open(self.event_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                org = row[5] if row[5] else None
                geocode = self.get_geocode(
                    address_dict={"street": row[8], "city": row[10], "state": row[11], "zip": row[12]},
                    lat_long_dict={"lat": row[15], "lng": row[16]},
                )
                event = Event(
                    title=row[0],
                    description=row[1],
                    date=row[2],
                    time=row[3],
                    ticket_cost=row[4],
                    organization_name=org,
                    primary_contact=row[6],
                    location_name=row[7],
                    street_address1=row[8],
                    street_address2=row[9],
                    city=row[10],
                    state=row[11],
                    zip=row[12],
                    website=row[13],
                    phone=row[14],
                    latitude=geocode["lat"],
                    longitude=geocode["lng"],
                    ages=[],
                    is_draft=False,
                    webinar_link=row[29],
                    post_survey_link=row[30],
                    max_users=None,
                    registered_users=[],
                    includes_registration=True,
                    is_uva_education_content=True,
                )
                self.__increment_id_sequence(Resource)

                if isinstance(row[31], int):
                    event.max_users = row[31]

                for i in range(26, 28):
                    if row[i]:
                        event.ages.extend(AgeRange.get_age_range_for_csv_data(row[i]))

                session.add(event)
                session.commit()

                for i in range(17, 25):
                    if row[i] and row[i] != "":
                        category = self.get_category_by_name(row[i].strip())
                        event_id = event.id
                        category_id = category.id
                        session.add(ResourceCategory(resource_id=event_id, category_id=category_id, type="event"))

                session.add(EventUser(event_id=event.id, user_id=1))
                session.add(EventUser(event_id=event.id, user_id=2))
                session.add(EventUser(event_id=event.id, user_id=4))
                session.add(EventUser(event_id=event.id, user_id=5))

        session.commit()
        print("Events loaded.  There are now %i events in the database." % session.query(Event).count())
        print(
            "There are now %i links between events and categories in the database."
            % session.query(ResourceCategory).filter(ResourceCategory.type == "event").count()
        )
        print("There are now %i links between events and users in the database." % session.query(EventUser).count())

    def load_locations(self):
        from .models import AgeRange
        from .models import Location
        from .models import ResourceCategory
        from .models import Resource

        with open(self.location_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers

            for row in reader:
                org = row[5] if row[5] else row[1]

                geocode = self.get_geocode(
                    address_dict={"street": row[8], "city": row[10], "state": row[11], "zip": row[12]},
                    lat_long_dict={"lat": row[17], "lng": row[18]},
                )

                location = Location(
                    title=row[1],
                    description=row[2],
                    primary_contact=row[6],
                    organization_name=org,
                    street_address1=row[8],
                    street_address2=row[9],
                    city=row[10],
                    state=row[11],
                    zip=row[12],
                    website=row[14],
                    email=row[15],
                    phone=row[16],
                    latitude=geocode["lat"],
                    longitude=geocode["lng"],
                    ages=[],
                    is_draft=False,
                )

                self.__increment_id_sequence(Resource)

                for i in range(29, len(row)):
                    if row[i]:
                        location.ages.extend(AgeRange.get_age_range_for_csv_data(row[i]))

                session.add(location)
                session.commit()

                for i in range(19, 28):
                    if row[i] and row[i] != "":
                        category = self.get_category_by_name(row[i].strip())
                        location_id = location.id
                        category_id = category.id
                        session.add(ResourceCategory(resource_id=location_id, category_id=category_id, type="location"))

        session.commit()
        print(
            "Locations loaded.  There are now %i locations in the database."
            % session.query(Location).filter(Location.type == "location").count()
        )
        print(
            "There are now %i links between locations and categories in the database."
            % session.query(ResourceCategory).filter(ResourceCategory.type == "location").count()
        )

    def load_resources(self):
        from .models import AgeRange
        from .models import ResourceCategory
        from .models import Resource

        with open(self.resource_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                org = row[4] if row[4] else None
                resource = Resource(
                    title=row[0],
                    description=row[1],
                    organization_name=org,
                    website=row[5],
                    phone=row[6],
                    ages=[],
                    is_draft=False,
                )

                self.__increment_id_sequence(Resource)

                for i in range(15, len(row)):
                    if row[i]:
                        resource.ages.extend(AgeRange.get_age_range_for_csv_data(row[i]))

                session.add(resource)
                session.commit()

                for i in range(7, 14):
                    if row[i] and row[i] != "":
                        category = self.get_category_by_name(row[i].strip())
                        resource_id = resource.id
                        category_id = category.id
                        session.add(ResourceCategory(resource_id=resource_id, category_id=category_id, type="resource"))

        session.commit()
        print(
            "Resources loaded.  There are now %i resources in the database."
            % session.query(Resource).filter(Resource.type == "resource").count()
        )
        print(
            "There are now %i links between resources and categories in the database."
            % session.query(ResourceCategory).filter(ResourceCategory.type == "resource").count()
        )

    def load_studies(self):
        from .models import AgeRange
        from .models import Investigator
        from .models import StudyCategory
        from .models import StudyInvestigator
        from .models import Study

        with open(self.study_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                org = row[4] if row[4] else None
                study = Study(
                    title=row[0],
                    description=row[1],
                    participant_description=row[2],
                    benefit_description=row[3],
                    organization_name=org,
                    location=row[5],
                    short_title=row[6],
                    short_description=row[7],
                    image_url=row[8],
                    coordinator_email=row[22],
                    eligibility_url=row[23],
                    ages=[],
                )

                if row[9].strip() == "Currently Enrolling":
                    study.status = Status.currently_enrolling
                elif row[9].strip() == "Study In Progress":
                    study.status = Status.study_in_progress
                elif row[9].strip() == "Results Being Analyzed":
                    study.status = Status.results_being_analyzed
                elif row[9].strip() == "Study Results Published":
                    study.status = Status.study_results_published

                for i in range(31, len(row)):
                    if row[i]:
                        study.ages.extend(AgeRange.get_age_range_for_csv_data(row[i]))

                session.add(study)
                session.commit()
                self.__increment_id_sequence(Study)

                for i in range(24, 31):
                    if row[i] and row[i] != "":
                        category = self.get_category_by_name(row[i].strip())
                        study_id = study.id
                        category_id = category.id
                        study_category = StudyCategory(study_id=study_id, category_id=category_id)
                        session.add(study_category)

                session.commit()

                for i in [10, 14, 18]:
                    if row[i]:
                        investigator = session.query(Investigator).filter(Investigator.name == row[i]).first()
                        if investigator is None:
                            investigator = Investigator(
                                name=row[i], title=row[i + 1], organization_name=row[i + 2], bio_link=row[i + 3]
                            )
                        session.add(investigator)
                        session.commit()
                        study_investigator = StudyInvestigator(study_id=study.id, investigator_id=investigator.id)
                        session.add(study_investigator)
                        session.commit()
            print("Studies loaded.  There are now %i studies in the database." % session.query(Study).count())
            print(
                "There are now %i links between studies and categories in the database."
                % session.query(StudyCategory).count()
            )
            print("There are now %i study investigators in the database." % session.query(Investigator).count())
        session.commit()

    def load_users(self):
        from .models import User

        with open(self.user_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                user = User(id=row[0], email=row[1], role=row[3], email_verified=True)
                user.password = row[2]
                session.add(user)
            print("Users loaded.  There are now %i users in the database." % session.query(User).count())
        session.commit()

    def load_participants(self):
        from .models import Participant

        with open(self.participant_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                participant = Participant(id=row[0], user_id=row[1], relationship=row[2])
                session.add(participant)
                # Users no longer have an id_sequence but are randomly assigned., safe to not increment this.
                # self.__increment_id_sequence(Participant)
            print(
                "Participants loaded.  There are now %i participants in the database."
                % session.query(Participant).count()
            )
        session.commit()

    def load_zip_codes(self):
        from .models import ZipCode

        items = []
        with open(self.zip_code_coords_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                items.append(ZipCode(id=row[0], latitude=row[1], longitude=row[2]))

        session.bulk_save_objects(items)
        session.commit()
        print("ZIP codes loaded.  There are now %i ZIP codes in the database." % session.query(ZipCode).count())

    def load_partial_zip_codes(self):
        from .models import ZipCode

        items = []
        with open(self.zip_code_coords_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            for _ in range(43000):  # skip the first 43000 rows
                next(reader)
            for row in reader:
                items.append(ZipCode(id=row[0], latitude=row[1], longitude=row[2]))

        session.bulk_save_objects(items)
        session.commit()
        print("ZIP codes loaded.  There are now %i ZIP codes in the database." % session.query(ZipCode).count())

    def load_chain_steps(self):
        from .models import ChainStep

        items = []
        with open(self.chain_steps_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=csv.excel.delimiter, quotechar=csv.excel.quotechar)
            next(reader, None)  # skip the headers
            for row in reader:
                items.append(ChainStep(id=row[0], name=row[1], instruction=row[2]))

        session.bulk_save_objects(items)
        session.commit()
        print(
            "SkillSTAR Chain Steps loaded.  There are now %i SkillSTAR Chain Steps in the database."
            % session.query(ChainStep).count()
        )

    def get_category_by_name(self, category_name, parent=None, create_missing=False):
        from .models import Category

        category = session.query(Category).filter(Category.name == category_name).first()
        if category is None:
            if create_missing:
                category = Category(name=category_name, parent=parent)
                session.add(category)
                session.commit()
            else:
                raise (Exception("This category is not defined: " + category_name))
        return category

    def get_geocode(self, address_dict, lat_long_dict):
        api_key = settings.GOOGLE_MAPS_API_KEY
        gmaps = googlemaps.Client(key=api_key)
        lat = None
        lng = None

        # Check that location has at least a zip code
        if address_dict["zip"]:

            # Use stored latitude & longitude, if available
            if "" not in lat_long_dict.values():
                lat = lat_long_dict["lat"]
                lng = lat_long_dict["lng"]

            # Otherwise, look it up using Google Maps API
            else:
                address = " ".join(address_dict.values())
                geocode_result = gmaps.geocode(address)

                if geocode_result is not None:
                    if geocode_result[0] is not None:
                        loc = geocode_result[0]["geometry"]["location"]
                        lat = loc["lat"]
                        lng = loc["lng"]
                        print(address_dict, loc)

        return {"lat": lat, "lng": lng}

    def build_index(self):
        from .models import Resource
        from .models import Study

        elastic_index.load_documents(
            resources=session.query(Resource).filter(Resource.type == "resource").all(),
            events=session.query(Resource).filter(Resource.type == "event").all(),
            locations=session.query(Resource).filter(Resource.type == "location").all(),
            studies=session.query(Study).all(),
        )

    def clear_index(self):
        print("Clearing the index")
        elastic_index.clear()

    def clear(self):
        from .database import clear_db

        clear_db()

    def clear_resources(self):
        from .models import AdminNote
        from .models import Category
        from .models import ChainStep
        from .models import EventUser
        from .models import Event
        from .models import Investigator
        from .models import Location
        from app.models import ChainSessionStep
        from .models import ResourceCategory
        from .models import Resource
        from .models import StudyUser
        from .models import StudyCategory
        from .models import StudyInvestigator
        from .models import Study
        from .models import UserFavorite
        from .models import ZipCode

        session.query(AdminNote).delete()
        session.query(ResourceCategory).delete()
        session.query(UserFavorite).delete()
        session.query(EventUser).delete()
        session.query(StudyUser).delete()
        session.query(StudyCategory).delete()
        session.query(StudyInvestigator).delete()
        session.query(Category).delete()
        session.query(Investigator).delete()
        session.query(Event).delete()
        session.query(Location).delete()
        session.query(Resource).delete()
        session.query(Study).delete()
        session.query(ZipCode).delete()

        num_steps = session.query(ChainSessionStep).count()
        if num_steps == 0:
            session.query(ChainStep).delete()

        session.commit()

    def __increment_id_sequence(self, model):
        session.execute(Sequence(model.__tablename__ + "_id_seq"))


data_loader = DataLoader()
