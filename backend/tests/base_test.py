import base64
import datetime
import os
import quopri
import re
from inspect import getsourcefile
from json import JSONEncoder
from typing import MutableMapping, Unpack, TypedDict, get_type_hints
from unittest import TestCase

from flask import json
from flask.ctx import RequestContext
from flask.testing import FlaskClient
from sqlalchemy import cast, Integer, select
from sqlalchemy.orm import scoped_session, close_all_sessions, joinedload
from werkzeug.test import TestResponse

from app.api_app import APIApp
from app.create_app import create_app
from app.data_loader import DataLoader
from app.elastic_index import ElasticIndex
from app.enums import Role
from app.models import (
    AdminNote,
    Category,
    ChainStep,
    EmailLog,
    Resource,
    Location,
    Event,
    Study,
    StudyInvestigator,
    StudyCategory,
)
from app.models import EventUser
from app.models import Investigator
from app.models import Participant
from app.models import ResourceCategory
from app.models import ResourceChangeLog
from app.models import StepLog
from app.models import StudyUser
from app.models import User
from app.models import UserFavorite
from app.models import UserMeta
from app.models import ZipCode
from fixtures.fixure_utils import fake
from fixtures.location import MockLocationWithLatLong
from fixtures.resource import MockResource
from fixtures.study import MockStudy

os.environ.setdefault("ENV_NAME", "testing")
os.putenv("ENV_NAME", "testing")


class ResourceParams(TypedDict):
    pass


class EventParams(TypedDict):
    pass


class LocationParams(TypedDict):
    pass


class StudyParams(TypedDict):
    pass


ResourceParams.__annotations__ = {k: v.__args__[0] for k, v in get_type_hints(Resource).items()}
EventParams.__annotations__ = {k: v.__args__[0] for k, v in get_type_hints(Event).items()}
LocationParams.__annotations__ = {k: v.__args__[0] for k, v in get_type_hints(Location).items()}
StudyParams.__annotations__ = {k: v.__args__[0] for k, v in get_type_hints(Study).items()}


class DateTimeEncoder(JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

        if isinstance(obj, MutableMapping):
            for key, value in list(obj.items()):
                if isinstance(value, (datetime.date, datetime.datetime)):
                    obj[key] = value.isoformat()

        return super().encode(obj)


class BaseTest(TestCase):
    auths = {}
    app: APIApp
    ctx: RequestContext
    client: FlaskClient
    session: scoped_session
    elastic_index: ElasticIndex

    @classmethod
    def setUpClass(cls):
        from config.testing import settings

        cls.reset_db()
        cls.reset_indices()

        _app = create_app(settings)

        cls.app = _app
        cls.ctx = _app.test_request_context()
        cls.ctx.push()

        cls.session = _app.session
        cls.elastic_index = _app.elastic_index
        cls.client = _app.test_client()

        current_dir = os.path.dirname(getsourcefile(lambda: 0))
        cls.loader = DataLoader(directory=current_dir + "/../example_data")

    @classmethod
    def tearDownClass(cls):
        cls.reset_db()
        cls.reset_indices()
        cls.ctx.pop()

    def setUp(self):
        self.reset_db()
        self.reset_indices()
        self.auths = {}

    def tearDown(self):
        self.session.rollback()
        close_all_sessions()
        self.elastic_index.connection.close()

    @classmethod
    def reset_indices(cls):
        cls.elastic_index = ElasticIndex()
        cls.elastic_index.clear()

    @classmethod
    def reset_db(cls):
        from app.database import clear_db

        # Clear out any tables that may have been created
        clear_db()

    def logged_in_headers(self, user_id: int = None, password: str = None) -> dict[str, str]:

        # If no user is provided, generate a dummy Admin user
        if user_id is not None and user_id in self.auths:
            return self.auths[user_id]

        if user_id is None:
            new_user = self.construct_user(email="admin@star.org", role=Role.admin)
            user_id = new_user.id

        db_user = (
            self.session.execute(select(User).options(joinedload(User.participants)).filter_by(id=user_id))
            .unique()
            .scalar_one()
        )
        self.assertIsNotNone(db_user)
        self.session.close()

        password = password or fake.password(length=32)
        token = self.login_user(user_id, password)

        self.auths[user_id] = dict(Authorization=f"Bearer {token}")
        self.assertIn(token, self.auths[user_id]["Authorization"])
        return self.auths[user_id]

    def login_user(self, user_id: int, password: str):
        user = (
            self.session.execute(select(User).options(joinedload(User.participants)).filter_by(id=user_id))
            .unique()
            .scalar_one()
        )
        user_email = user.email
        user.email_verified = True
        user.password = password
        self.session.add(user)
        self.session.commit()
        self.session.close()

        data = {"email": user_email, "password": password}
        rv = self.client.post("/api/login_password", data=self.jsonify(data), content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertIsNotNone(response["token"])

        return response["token"]

    def decode(self, encoded_words):
        """
        Useful for checking the content of email messages
        (which we store in an array for testing)
        """
        encoded_word_regex = r"=\?{1}(.+)\?{1}([b|q])\?{1}(.+)\?{1}="
        charset, encoding, encoded_text = re.match(encoded_word_regex, encoded_words).groups()
        if encoding == "b":
            byte_string = base64.b64decode(encoded_text)
        elif encoding == "q":
            byte_string = quopri.decodestring(encoded_text)
        text = byte_string.decode(charset)
        text = text.replace("_", " ")
        return text

    def jsonify(self, data):
        """
        Returns given data as JSON string, converting dates to ISO format.
        """

        # Convert the object to a dict first if possible
        if not isinstance(data, dict) and hasattr(data, "__dict__"):
            data = data.__dict__

        return json.dumps(data, cls=DateTimeEncoder)

    def assert_success(self, rv: TestResponse, msg=""):
        try:
            data = rv.json
            self.assertTrue(
                200 <= rv.status_code < 300,
                f"BAD Response: {rv.status_code}. \n {self.jsonify(data)}. {msg}",
            )
        except:
            self.assertTrue(200 <= rv.status_code < 300, f"BAD Response: {rv.status_code}. {msg}")

    def construct_user(
        self, email=None, role=Role.user, last_login: datetime.datetime | str = datetime.datetime.now()
    ) -> User:
        email = email or fake.email()
        if isinstance(last_login, str):
            last_login = datetime.datetime.strptime(last_login, "%m/%d/%y %H:%M")
        db_user = (
            self.session.execute(select(User).options(joinedload(User.participants)).filter(User.email == email))
            .unique()
            .scalar_one_or_none()
        )
        if db_user:
            return db_user
        user = User(email=email, role=role, last_login=last_login)
        self.session.add(user)
        self.session.commit()
        db_user = (
            self.session.execute(select(User).options(joinedload(User.participants)).filter(User.email == email))
            .unique()
            .scalar_one_or_none()
        )
        self.assertEqual(db_user.email, user.email)

        self.session.close()
        return db_user

    def construct_participant(self, user_id: int, relationship):
        participant = Participant(user_id=user_id, relationship=relationship)
        self.session.add(participant)
        self.session.commit()

        participant_id = participant.id
        db_participant = (
            self.session.execute(
                select(Participant)
                .options(joinedload(Participant.identification), joinedload(Participant.contact))
                .filter_by(id=participant_id)
                .filter_by(user_id=user_id)
            )
            .unique()
            .scalar_one()
        )
        self.assertEqual(db_participant.relationship, participant.relationship)
        self.session.close()

        return db_participant

    def construct_usermeta(self, user):
        usermeta = UserMeta(id=user.id)
        self.session.add(usermeta)
        self.session.commit()
        return usermeta

    def construct_admin_note(
        self, user, resource, note="I think all sorts of things about this resource and I'm telling you now."
    ):
        admin_note = AdminNote(user_id=user.id, resource_id=resource.id, note=note)
        self.session.add(admin_note)
        self.session.commit()
        db_admin_note = self.session.query(AdminNote).filter_by(id=admin_note.id).first()
        self.assertEqual(db_admin_note.note, admin_note.note)
        return db_admin_note

    def construct_category(self, name="Ultimakers", parent_id: int = None) -> Category:
        category = Category(name=name)
        if parent_id is not None:
            category.parent_id = parent_id
        self.session.add(category)
        self.session.commit()
        category_id = category.id
        self.session.close()

        db_category = (
            self.session.execute(select(Category).options(joinedload(Category.parent)).filter_by(id=category_id))
            .unique()
            .scalar_one()
        )
        self.assertIsNotNone(db_category.id)
        self.assertEqual(db_category.name, name)
        self.session.close()
        return db_category

    def construct_resource(
        self,
        **kwargs: Unpack[ResourceParams],
    ):
        mock_resource = MockResource()

        # Override any fields that were passed in
        for key in ResourceParams.__annotations__.keys():
            if key in kwargs and kwargs[key] is not None:
                mock_resource.__setattr__(key, kwargs[key])

        resource = Resource(**mock_resource.__dict__)
        self.session.add(resource)
        self.session.commit()
        resource_id = resource.id
        category_ids = [c.id for c in resource.categories]
        self.session.close()

        for category_id in category_ids:
            rc = ResourceCategory(resource_id=resource_id, category_id=category_id, type="resource")
            self.session.add(rc)

        self.session.commit()
        self.session.close()

        db_resource = self.session.execute(select(Resource).filter(Resource.id == resource_id)).unique().scalar_one()
        self.assertEqual(db_resource.website, resource.website)

        self.elastic_index.add_document(db_resource)
        return db_resource

    def construct_location(
        self,
        **kwargs: Unpack[LocationParams],
    ):
        mock_location = MockLocationWithLatLong()

        # Override any fields that were passed in
        for key in LocationParams.__annotations__.keys():
            if key in kwargs and kwargs[key] is not None:
                mock_location.__setattr__(key, kwargs[key])

        location = Location(**mock_location.__dict__)
        self.session.add(location)
        self.session.commit()
        location_id = location.id
        category_ids = [c.id for c in location.categories]
        self.session.close()

        for category_id in category_ids:
            rc = ResourceCategory(location_id=location_id, category_id=category_id, type="location")
            self.session.add(rc)

        self.session.commit()
        self.session.close()

        db_location = (
            self.session.execute(
                select(Location)
                .options(joinedload(Location.categories), joinedload(Location.resource_categories))
                .filter(Location.id == location_id)
            )
            .unique()
            .scalar_one()
        )
        self.assertEqual(db_location.website, location.website)

        self.elastic_index.add_document(
            document=db_location, latitude=db_location.latitude, longitude=db_location.longitude
        )
        return db_location

    def construct_location_category(self, location_id, category_name):
        c = self.construct_category(name=category_name)
        c_id = c.id
        rc = ResourceCategory(resource_id=location_id, category_id=c_id, type="location")
        self.session.add(rc)
        self.session.commit()
        self.session.close()

        db_c = (
            self.session.execute(
                select(Category)
                .options(joinedload(Category.parent), joinedload(Category.children))
                .filter(Category.id == c_id)
            )
            .unique()
            .scalar_one()
        )
        self.assertEqual(db_c.name, category_name)
        self.session.close()
        return db_c

    def construct_study_category(self, study_id, category_name):
        c = self.construct_category(name=category_name)
        sc = StudyCategory(study_id=study_id, category=c)
        self.session.add(sc)
        self.session.commit()
        return c

    def construct_study(
        self,
        **kwargs: Unpack[StudyParams],
    ):
        mock_study = MockStudy()

        # Override any fields that were passed in
        for key in StudyParams.__annotations__.keys():
            if key in kwargs and kwargs[key] is not None:
                mock_study.__setattr__(key, kwargs[key])

        study = Study(**mock_study.__dict__)
        self.session.add(study)
        self.session.commit()
        study_id = study.id
        category_ids = [c.id for c in study.categories]
        self.session.close()

        for category_id in category_ids:
            rc = StudyCategory(study_id=study_id, category_id=category_id)
            self.session.add(rc)

        self.session.commit()
        self.session.close()

        db_study: Study = self.session.execute(select(Study).filter(Study.id == study_id)).unique().scalars().first()
        self.assertEqual(db_study.eligibility_url, study.eligibility_url)

        self.elastic_index.add_document(db_study)
        self.assertEqual(len(db_study.categories), len(category_ids))

        return db_study

    def construct_investigator(self, name="Judith Wonder", title="Ph.D., Assistant Professor of Mereology"):

        investigator = Investigator(name=name, title=title)
        investigator.organization_name = "Investigator Org"
        self.session.add(investigator)
        self.session.commit()

        db_inv = self.session.query(Investigator).filter_by(name=investigator.name).first()
        self.assertEqual(db_inv.title, investigator.title)
        return db_inv

    def construct_event(
        self,
        title="A+ Event",
        description="A delightful event destined to create rejoicing",
        street_address1="123 Some Pl",
        street_address2="Apt. 45",
        is_draft=False,
        city="Stauntonville",
        state="QX",
        zip="99775",
        phone="555-555-5555",
        website="http://stardrive.org",
        date=datetime.datetime.now() + datetime.timedelta(days=7),
        organization_name="Event Org",
        post_survey_link="http://stardrive.org/survey",
        webinar_link="http://stardrive.org/event",
        includes_registration=True,
        max_users=35,
        registered_users=None,
        post_event_description=None,
    ):

        if registered_users is None:
            registered_users = [
                self.construct_user(email="e1@sartography.com"),
                self.construct_user("e2@sartography.com"),
            ]
        event = Event(
            title=title,
            description=description,
            street_address1=street_address1,
            street_address2=street_address2,
            city=city,
            state=state,
            zip=zip,
            phone=phone,
            website=website,
            date=date,
            is_draft=is_draft,
            organization_name=organization_name,
            webinar_link=webinar_link,
            post_survey_link=post_survey_link,
            includes_registration=includes_registration,
            max_users=max_users,
            post_event_description=post_event_description,
        )
        self.session.add(event)
        self.session.commit()

        db_event = self.session.query(Event).filter(Event.id == event.id).first()
        self.session.close()

        self.assertEqual(db_event.website, event.website)
        self.assertEqual(db_event.type, "event")

        for user in registered_users:
            eu = EventUser(event_id=db_event.id, user_id=user.id)
            self.session.add(eu)

        self.session.commit()
        self.session.close()

        db_event = self.session.query(Event).filter(Event.id == event.id).first()
        self.elastic_index.add_document(db_event)
        return db_event

    def construct_zip_code(self, id=24401, latitude=38.146216, longitude=-79.07625):
        z = ZipCode(id=id, latitude=latitude, longitude=longitude)
        self.session.add(z)
        self.session.commit()

        db_z = self.session.query(ZipCode).filter_by(id=cast(id, Integer)).first()
        self.assertEqual(db_z.id, z.id)
        self.assertEqual(db_z.latitude, z.latitude)
        self.assertEqual(db_z.longitude, z.longitude)
        return db_z

    def construct_chain_steps(self):
        num_steps = self.session.query(ChainStep).count()

        if num_steps == 0:
            self.construct_chain_step(id=0, name="time_warp_01", instruction="Jump to the left")
            self.construct_chain_step(id=1, name="time_warp_02", instruction="Step to the right")
            self.construct_chain_step(id=2, name="time_warp_03", instruction="Put your hands on your hips")
            self.construct_chain_step(id=3, name="time_warp_04", instruction="Pull your knees in tight")

        return self.session.query(ChainStep).all()

    def construct_chain_step(
        self, id=0, name="time_warp_01", instruction="Jump to the left", last_updated=datetime.datetime.utcnow()
    ):
        self.session.add(ChainStep(id=id, name=name, instruction=instruction, last_updated=last_updated))
        self.session.commit()
        return self.session.query(ChainStep).filter(ChainStep.id == cast(id, Integer)).first()

    def construct_everything(self):
        questionnaires = None
        if hasattr(self, "construct_all_questionnaires"):
            questionnaires = self.construct_all_questionnaires()
        cat = self.construct_category()
        resource = self.construct_resource(**MockResource().__dict__, categories=[cat])
        study = self.construct_study()
        location = self.construct_location()
        user = self.construct_user()
        participant = self.construct_participant(user.id, "self_participant")
        self.construct_event()
        self.construct_location_category(location.id, cat.name)
        self.construct_study_category(study.id, cat.name)
        self.construct_zip_code()
        investigator = self.construct_investigator(name="Sam I am")
        self.session.add(StudyInvestigator(study=study, investigator=investigator))
        self.session.add(StudyUser(study=study, user=self.construct_user()))
        self.session.add(AdminNote(user_id=self.construct_user().id, resource_id=self.construct_resource().id, note=""))
        self.session.add(
            UserFavorite(user_id=self.construct_user().id, type="resource", resource_id=self.construct_resource().id)
        )
        self.session.add(EmailLog(user_id=self.construct_user().id, type="test", tracking_code="test"))
        self.session.add(
            ResourceChangeLog(
                type="edit",
                user_id=user.id,
                user_email=user.email,
                resource_id=resource.id,
                resource_title=resource.title,
            )
        )
        if questionnaires and "identification" in questionnaires:
            q = questionnaires["identification"]
            self.session.add(
                StepLog(
                    questionnaire_name="Identification",
                    questionnaire_id=q.id,
                    flow="registration",
                    participant_id=participant.id,
                    user_id=participant.user_id,
                    time_on_task_ms=999999,
                )
            )
        self.session.commit()

    def get_identification_questionnaire(self, participant_id):
        return {
            "first_name": "Darah",
            "middle_name": "Soo",
            "last_name": "Ubway",
            "is_first_name_preferred": True,
            "birthdate": "2002-02-02T00:00:00.000000Z",
            "birth_city": "Staunton",
            "birth_state": "VA",
            "is_english_primary": True,
            "participant_id": participant_id,
        }
