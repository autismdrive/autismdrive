# Set environment variable to testing before loading.
# IMPORTANT - Environment must be loaded before app, models, etc....
import os

from app.model.email_log import EmailLog
from app.model.event import Event
from app.model.investigator import Investigator
from app.model.step_log import StepLog
from app.model.study import Study, Status
from app.model.study_category import StudyCategory
from app.model.study_investigator import StudyInvestigator

os.environ["TESTING"] = "true"

from flask import json

from app import app, db, elastic_index
from app.model.category import Category
from app.model.resource_category import ResourceCategory
from app.model.location import Location
from app.model.organization import Organization
from app.model.participant import Participant
from app.model.resource import Resource
from app.model.user import User, Role


def clean_db(db):
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())


class BaseTest:

    auths = {}

    @classmethod
    def setUpClass(cls):
        cls.ctx = app.test_request_context()
        cls.app = app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        db.session.remove()

    def setUp(self):
        self.ctx.push()
        clean_db(db)
        self.auths = {}

    def tearDown(self):
        db.session.rollback()
        self.ctx.pop()


    def logged_in_headers(self, user=None):

        # If no user is provided, generate a dummy Admin user
        if not user:
            existing_user = self.construct_user(email="admin@star.org", role=Role.admin)
        else:
            existing_user = User.query.filter_by(id=user.id).first()

        if existing_user.id in self.auths:
            return self.auths[existing_user.id]

        data = {
            'email': existing_user.email,
            'password': existing_user.password
        }

        rv = self.app.post(
            '/api/login_password',
            data=json.dumps(data),
            content_type="application/json")

        self.auths[existing_user.id] = dict(
            Authorization='Bearer ' + existing_user.encode_auth_token().decode())

        return self.auths[existing_user.id]

    def assert_success(self, rv, msg=""):
        try:
            data = json.loads(rv.get_data(as_text=True))
            self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                            "BAD Response: %i. \n %s" %
                            (rv.status_code, json.dumps(data)) + ". " + msg)
        except:
            self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                            "BAD Response: %i." % rv.status_code + ". " + msg)

    def construct_user(self, email="stan@staunton.com", role=Role.user):

        db_user = db.session.query(User).filter_by(email=email).first()
        if db_user:
            return db_user
        user = User(email=email, role=role)
        db.session.add(user)
        db_user = db.session.query(User).filter_by(email=user.email).first()
        self.assertEqual(db_user.email, user.email)
        return db_user

    def construct_participant(self, user, relationship):

        participant = Participant(user=user, relationship=relationship)
        db.session.add(participant)
        db.session.commit()
#        db_participant = db.session.query(Participant).filter_by(id=participant.id).first()
#        self.assertEqual(db_participant.relationship, participant.relationship)
        return participant

    def construct_organization(self, name="Staunton Makerspace",
                               description="A place full of surprise, delight, and amazing people. And tools. Lots of exciting tools."):

        organization = Organization(name=name, description=description)
        db.session.add(organization)

        db_org = db.session.query(Organization).filter_by(name=organization.name).first()
        self.assertEqual(db_org.description, organization.description)
        self.assertIsNotNone(db_org.id)
        return db_org

    def construct_category(self, name="Ultimakers", parent=None):

        category = Category(name=name)
        if parent is not None:
            category.parent = parent
        db.session.add(category)

        db_category = db.session.query(Category).filter_by(name=category.name).first()
        self.assertIsNotNone(db_category.id)
        return db_category

    def construct_resource(self, title="A+ Resource", description="A delightful Resource destined to create rejoicing",
                           phone="555-555-5555", website="http://stardrive.org"):

        resource = Resource(title=title, description=description, phone=phone, website=website)
        resource.organization_id = self.construct_organization().id
        db.session.add(resource)

        db_resource = db.session.query(Resource).filter_by(title=resource.title).first()
        self.assertEqual(db_resource.website, resource.website)
        elastic_index.add_document(db_resource, 'Resource')
        return db_resource

    def construct_location(self, title="A+ location", description="A delightful location destined to create rejoicing",
                           street_address1="123 Some Pl", street_address2="Apt. 45",
                           city="Stauntonville", state="QX", zip="99775", phone="555-555-5555",
                           website="http://stardrive.org", latitude=38.98765, longitude=-93.12345):

        location = Location(title=title, description=description, street_address1=street_address1, street_address2=street_address2, city=city,
                                state=state, zip=zip,phone=phone, website=website, latitude=latitude, longitude=longitude)
        location.organization_id = self.construct_organization().id
        db.session.add(location)
        db.session.commit()

        db_location = db.session.query(Location).filter_by(title=location.title).first()
        self.assertEqual(db_location.website, location.website)
        elastic_index.add_document(db_location, True, latitude=latitude, longitude=longitude)
        return db_location

    def construct_location_category(self, location_id, category_name):
        c = self.construct_category(name=category_name)
        rc = ResourceCategory(resource_id=location_id, category=c, type='location')
        db.session.add(rc)
        db.session.commit()
        return c

    def construct_study_category(self, study_id, category_name):
        c = self.construct_category(name=category_name)
        sc = StudyCategory(study_id=study_id, category=c)
        db.session.add(sc)
        db.session.commit()
        return c

    def construct_study(self, title="Fantastic Study", description="A study that will go down in history",
                        participant_description="Even your pet hamster could benefit from participating in this study",
                        benefit_description="You can expect to have your own rainbow following you around afterwards"):

        study = Study(title=title, description=description, participant_description=participant_description,
                      benefit_description=benefit_description, status=Status.currently_enrolling)
        study.organization_id = self.construct_organization().id
        db.session.add(study)
        db.session.commit()

        db_study = db.session.query(Study).filter_by(title=study.title).first()
        self.assertEqual(db_study.description, description)
        elastic_index.add_document(db_study, 'Study')
        return db_study

    def construct_investigator(self, name="Judith Wonder", title="Ph.D., Assistant Professor of Mereology"):

        investigator = Investigator(name=name, title=title)
        investigator.organization_id = self.construct_organization().id
        db.session.add(investigator)
        db.session.commit()

        db_inv = db.session.query(Investigator).filter_by(name=investigator.name).first()
        self.assertEqual(db_inv.title, investigator.title)
        return db_inv

    def construct_event(self, title="A+ Event", description="A delightful event destined to create rejoicing",
                           street_address1="123 Some Pl", street_address2="Apt. 45",
                           city="Stauntonville", state="QX", zip="99775", phone="555-555-5555",
                           website="http://stardrive.org"):

        event = Event(title=title, description=description, street_address1=street_address1, street_address2=street_address2, city=city,
                                state=state, zip=zip, phone=phone, website=website)
        event.organization_id = self.construct_organization().id
        db.session.add(event)

        db_event = db.session.query(Event).filter_by(title=event.title).first()
        self.assertEqual(db_event.website, event.website)
        elastic_index.add_document(db_event, 'Event')
        return db_event

    def construct_everything(self):
        self.construct_all_questionnaires()
        cat = self.construct_category()
        org = self.construct_organization()
        self.construct_resource()
        study = self.construct_study()
        location = self.construct_location()
        event = self.construct_event()
        self.construct_location_category(location.id, cat.name)
        self.construct_study_category(study.id, cat.name)
        investigator = Investigator(name="Sam I am", organization_id=org.id)
        db.session.add(StudyInvestigator(study = study, investigator = investigator))
        db.session.add(investigator)
        db.session.add(EmailLog())
        db.session.add(StepLog())
        db.session.commit()
