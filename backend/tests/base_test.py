# Set environment variable to testing before loading.
# IMPORTANT - Environment must be loaded before app, models, etc....
import os
os.environ["APP_CONFIG_FILE"] = '../config/testing.py'

from flask import json

from app import app, db, elastic_index
from app.model.category import Category
from app.model.organization import Organization
from app.model.participant import Participant
from app.model.resource import StarResource
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

    def assert_success(self, rv):
        try:
            data = json.loads(rv.get_data(as_text=True))
            self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                            "BAD Response: %i. \n %s" %
                            (rv.status_code, json.dumps(data)))
        except:
            self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                            "BAD Response: %i." % rv.status_code)

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

        resource = StarResource(title=title, description=description, phone=phone, website=website)
        resource.organization_id = self.construct_organization().id
        db.session.add(resource)

        db_resource = db.session.query(StarResource).filter_by(title=resource.title).first()
        self.assertEqual(db_resource.website, resource.website)
        elastic_index.add_document(db_resource, 'Resource')
        return db_resource
