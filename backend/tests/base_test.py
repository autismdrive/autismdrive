import base64
import datetime
import os
import quopri
import re
from inspect import getsourcefile
from json import JSONEncoder
from unittest import TestCase

import click
from flask import json
from flask.ctx import RequestContext
from flask.testing import FlaskClient
from sqlalchemy.orm import scoped_session, close_all_sessions
from sqlalchemy_utils import database_exists, create_database
from werkzeug.test import TestResponse

from app.api_app import APIApp
from app.create_app import create_app
from app.data_loader import DataLoader
from app.elastic_index import elastic_index
from app.enums import Status, Role
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


class BaseTest(TestCase):
    auths = {}
    app: APIApp
    ctx: RequestContext
    client: FlaskClient
    session: scoped_session

    @classmethod
    def setUpClass(cls):
        from config.testing import settings

        _app = create_app(settings)

        cls.app = _app
        cls.ctx = _app.test_request_context()
        cls.ctx.push()

        cls.session = _app.session
        cls.client = _app.test_client()
        cls.reset_db()
        cls.reset_indices()

        from app.database import upgrade_db

        upgrade_db()

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
        from app.database import session

        session.rollback()
        close_all_sessions()

    @classmethod
    def reset_indices(cls):
        elastic_index.clear()

    @classmethod
    def reset_db(cls):
        from app.database import clear_db

        # Clear out any tables that may have been created
        clear_db()

    def logged_in_headers(self, user=None) -> dict[str, str]:

        # If no user is provided, generate a dummy Admin user
        existing_user: User
        if not user:
            existing_user = self.construct_user(email="admin@star.org", role=Role.admin)
        else:
            existing_user = self.session.query(User).filter_by(id=user.id).first()

        if existing_user.id in self.auths:
            return self.auths[existing_user.id]

        token = existing_user.encode_auth_token()
        self.assertIsNotNone(token)
        self.auths[existing_user.id] = dict(Authorization=f"Bearer {token}")
        self.assertIn(token, self.auths[existing_user.id]["Authorization"])
        return self.auths[existing_user.id]

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

        class DateTimeEncoder(JSONEncoder):
            def default(self, obj):
                if isinstance(obj, (datetime.date, datetime.datetime)):
                    return obj.isoformat()

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

    def construct_user(self, email="stan@staunton.com", role=Role.user, last_login=datetime.datetime.now()) -> User:
        db_user = self.session.query(User).filter_by(email=email).first()
        if db_user:
            return db_user
        user = User(email=email, role=role, last_login=last_login)
        self.session.add(user)
        self.session.commit()
        db_user = self.session.query(User).filter_by(email=user.email).first()
        self.assertEqual(db_user.email, user.email)
        return db_user

    def construct_participant(self, user, relationship):
        participant = Participant(user=user, relationship=relationship)
        self.session.add(participant)
        self.session.commit()
        #        db_participant = self.session.query(Participant).filter_by(id=participant.id).first()
        #        self.assertEqual(db_participant.relationship, participant.relationship)
        return participant

    def construct_usermeta(self, user):
        usermeta = UserMeta(id=user.id)
        self.session.add(usermeta)
        self.session.commit()
        return usermeta

    def construct_admin_note(
        self, user, resource, id=976, note="I think all sorts of things about this resource and I'm telling you now."
    ):
        admin_note = AdminNote(id=id, user_id=user.id, resource_id=resource.id, note=note)
        self.session.add(admin_note)
        self.session.commit()
        db_admin_note = self.session.query(AdminNote).filter_by(id=admin_note.id).first()
        self.assertEqual(db_admin_note.note, admin_note.note)
        return db_admin_note

    def construct_category(self, name="Ultimakers", parent=None):
        category = Category(name=name)
        if parent is not None:
            category.parent = parent
        self.session.add(category)
        self.session.commit()
        db_category = self.session.query(Category).filter_by(name=category.name).first()
        self.assertIsNotNone(db_category.id)
        return db_category

    def construct_resource(
        self,
        title="A+ Resource",
        description="A delightful Resource destined to create rejoicing",
        phone="555-555-5555",
        website="http://stardrive.org",
        is_draft=False,
        organization_name="Some Org",
        categories=None,
        ages=None,
        languages=None,
        covid19_categories=None,
        is_uva_education_content=False,
    ):
        categories = [] if categories is None else categories
        ages = [] if ages is None else ages
        languages = [] if languages is None else languages
        covid19_categories = [] if covid19_categories is None else covid19_categories

        resource = Resource(
            title=title,
            description=description,
            phone=phone,
            website=website,
            ages=ages,
            organization_name=organization_name,
            is_draft=is_draft,
            languages=languages,
            covid19_categories=covid19_categories,
            is_uva_education_content=is_uva_education_content,
        )
        self.session.add(resource)
        self.session.commit()
        for category in categories:
            rc = ResourceCategory(resource_id=resource.id, category=category, type="resource")
            self.session.add(rc)

        self.session.commit()
        db_resource = self.session.query(Resource).filter_by(title=resource.title).first()
        self.assertEqual(db_resource.website, resource.website)

        elastic_index.add_document(db_resource, "Resource")
        return db_resource

    def construct_location(
        self,
        title="A+ location",
        description="A delightful location destined to create rejoicing",
        street_address1="123 Some Pl",
        street_address2="Apt. 45",
        is_draft=False,
        city="Stauntonville",
        state="QX",
        zip="99775",
        phone="555-555-5555",
        website="http://stardrive.org",
        latitude=38.98765,
        longitude=-93.12345,
        organization_name="Location Org",
    ):

        location = Location(
            title=title,
            description=description,
            street_address1=street_address1,
            street_address2=street_address2,
            city=city,
            state=state,
            zip=zip,
            phone=phone,
            website=website,
            latitude=latitude,
            longitude=longitude,
            is_draft=is_draft,
            organization_name=organization_name,
        )
        self.session.add(location)
        self.session.commit()

        db_location = self.session.query(Location).filter_by(title=location.title).first()
        self.assertEqual(db_location.website, location.website)
        elastic_index.add_document(document=db_location, flush=True, latitude=latitude, longitude=longitude)
        return db_location

    def construct_location_category(self, location_id, category_name):
        c = self.construct_category(name=category_name)
        rc = ResourceCategory(resource_id=location_id, category=c, type="location")
        self.session.add(rc)
        self.session.commit()
        return c

    def construct_study_category(self, study_id, category_name):
        c = self.construct_category(name=category_name)
        sc = StudyCategory(study_id=study_id, category=c)
        self.session.add(sc)
        self.session.commit()
        return c

    def construct_study(
        self,
        title="Fantastic Study",
        description="A study that will go down in history",
        participant_description="Even your pet hamster could benefit from participating in this study",
        benefit_description="You can expect to have your own rainbow following you around afterwards",
        coordinator_email="hello@study.com",
        categories=None,
        organization_name="Study Org",
    ):
        categories = [] if categories is None else categories

        study = Study(
            title=title,
            description=description,
            participant_description=participant_description,
            benefit_description=benefit_description,
            status=Status.currently_enrolling,
            coordinator_email=coordinator_email,
            organization_name=organization_name,
        )

        self.session.add(study)
        self.session.commit()
        db_study = self.session.query(Study).filter_by(title=study.title).first()
        self.assertEqual(db_study.description, description)

        for category in categories:
            sc = StudyCategory(study_id=db_study.id, category_id=category.id)
            self.session.add(sc)

        self.session.commit()
        elastic_index.add_document(db_study, "Study")

        db_study = self.session.query(Study).filter_by(id=db_study.id).first()
        self.assertEqual(len(db_study.categories), len(categories))

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

        db_event = self.session.query(Event).filter_by(title=event.title).first()
        self.assertEqual(db_event.website, event.website)

        for user in registered_users:
            eu = EventUser(event_id=db_event.id, user_id=user.id)
            self.session.add(eu)

        self.session.commit()

        elastic_index.add_document(db_event, "Event")
        return db_event

    def construct_zip_code(self, id=24401, latitude=38.146216, longitude=-79.07625):
        z = ZipCode(id=id, latitude=latitude, longitude=longitude)
        self.session.add(z)
        self.session.commit()

        db_z = self.session.query(ZipCode).filter_by(id=id).first()
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
        self, id=0, name="time_warp_01", instruction="Jump to the left", last_updated=datetime.datetime.now()
    ):
        self.session.add(ChainStep(id=id, name=name, instruction=instruction, last_updated=last_updated))
        self.session.commit()
        return self.session.query(ChainStep).filter(ChainStep.id == id).first()

    def construct_everything(self):
        if hasattr(self, "construct_all_questionnaires"):
            self.construct_all_questionnaires()
        cat = self.construct_category()
        self.construct_resource()
        study = self.construct_study()
        location = self.construct_location()
        self.construct_event()
        self.construct_location_category(location.id, cat.name)
        self.construct_study_category(study.id, cat.name)
        self.construct_zip_code()
        investigator = Investigator(name="Sam I am")
        self.session.add(StudyInvestigator(study=study, investigator=investigator))
        self.session.add(StudyUser(study=study, user=self.construct_user()))
        self.session.add(AdminNote(user_id=self.construct_user().id, resource_id=self.construct_resource().id, note=""))
        self.session.add(UserFavorite(user_id=self.construct_user().id))
        self.session.add(investigator)
        self.session.add(EmailLog())
        self.session.add(ResourceChangeLog())
        self.session.add(StepLog())
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
