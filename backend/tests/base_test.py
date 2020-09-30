# Set environment variable to testing before loading.
# IMPORTANT - Environment must be loaded before app, models, etc....
import base64
import datetime
import os
import quopri
import re

os.environ["TESTING"] = "true"

from app.model.email_log import EmailLog
from app.model.event import Event
from app.model.investigator import Investigator
from app.model.step_log import StepLog
from app.model.study import Study, Status
from app.model.study_category import StudyCategory
from app.model.study_investigator import StudyInvestigator
from app.model.study_user import StudyUser
from app.model.user_favorite import UserFavorite


from flask import json

from app import app, db, elastic_index
from app.model.admin_note import AdminNote
from app.model.category import Category
from app.model.resource_category import ResourceCategory
from app.model.location import Location
from app.model.participant import Participant
from app.model.resource import Resource
from app.model.resource_change_log import ResourceChangeLog
from app.model.user import User, Role
from app.model.zip_code import ZipCode

def clean_db(db):
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())


class BaseTest:

    auths = {}

    @classmethod
    def setUpClass(cls):
        app.config.from_object('config.testing')
        app.config.from_pyfile('testing.py')

        cls.ctx = app.test_request_context()
        cls.app = app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        db.session.remove()
        elastic_index.clear()

    def setUp(self):
        self.ctx.push()
        clean_db(db)
        elastic_index.clear()
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

        self.auths[existing_user.id] = dict(
            Authorization='Bearer ' + existing_user.encode_auth_token().decode())

        return self.auths[existing_user.id]

    def decode(self, encoded_words):
        """
        Useful for checking the content of email messages
        (which we store in an array for testing)
        """
        encoded_word_regex = r'=\?{1}(.+)\?{1}([b|q])\?{1}(.+)\?{1}='
        charset, encoding, encoded_text = re.match(encoded_word_regex,
                                                   encoded_words).groups()
        if encoding == 'b':
            byte_string = base64.b64decode(encoded_text)
        elif encoding == 'q':
            byte_string = quopri.decodestring(encoded_text)
        text = byte_string.decode(charset)
        text = text.replace("_", " ")
        return text

    def assert_success(self, rv, msg=""):
        try:
            data = json.loads(rv.get_data(as_text=True))
            self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                            "BAD Response: %i. \n %s" %
                            (rv.status_code, json.dumps(data)) + ". " + msg)
        except:
            self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                            "BAD Response: %i." % rv.status_code + ". " + msg)

    def construct_user(self, email="stan@staunton.com", role=Role.user, last_login=datetime.datetime.now()):

        db_user = db.session.query(User).filter_by(email=email).first()
        if db_user:
            return db_user
        user = User(email=email, role=role, last_login=last_login)
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

    def construct_admin_note(self, user, resource, id=976, note="I think all sorts of things about this resource and I'm telling you now."):
        admin_note = AdminNote(id=id, user_id=user.id, resource_id=resource.id, note=note)
        db.session.add(admin_note)
        db.session.commit()
        db_admin_note = db.session.query(AdminNote).filter_by(id=admin_note.id).first()
        self.assertEqual(db_admin_note.note, admin_note.note)
        return db_admin_note

    def construct_category(self, name="Ultimakers", parent=None):

        category = Category(name=name)
        if parent is not None:
            category.parent = parent
        db.session.add(category)

        db_category = db.session.query(Category).filter_by(name=category.name).first()
        self.assertIsNotNone(db_category.id)
        return db_category

    def construct_resource(self, title="A+ Resource", description="A delightful Resource destined to create rejoicing",
                           phone="555-555-5555", website="http://stardrive.org", is_draft=False,
                           organization_name="Some Org", categories=[], ages=[], languages=[], covid19_categories=[], is_uva_education_content=False):

        resource = Resource(title=title, description=description, phone=phone, website=website, ages=ages,
                            organization_name=organization_name, is_draft=is_draft, languages=languages,
                            covid19_categories=covid19_categories, is_uva_education_content=is_uva_education_content)
        db.session.add(resource)
        db.session.commit()
        for category in categories:
            rc = ResourceCategory(resource_id=resource.id, category=category, type='resource')
            db.session.add(rc)

        db_resource = db.session.query(Resource).filter_by(title=resource.title).first()
        self.assertEqual(db_resource.website, resource.website)

        elastic_index.add_document(db_resource, 'Resource')
        return db_resource

    def construct_location(self, title="A+ location", description="A delightful location destined to create rejoicing",
                           street_address1="123 Some Pl", street_address2="Apt. 45", is_draft=False,
                           city="Stauntonville", state="QX", zip="99775", phone="555-555-5555",
                           website="http://stardrive.org", latitude=38.98765, longitude=-93.12345,
                           organization_name="Location Org"):

        location = Location(title=title, description=description, street_address1=street_address1,
                            street_address2=street_address2, city=city, state=state, zip=zip,phone=phone,
                            website=website, latitude=latitude, longitude=longitude, is_draft=is_draft,
                            organization_name=organization_name)
        db.session.add(location)
        db.session.commit()

        db_location = db.session.query(Location).filter_by(title=location.title).first()
        self.assertEqual(db_location.website, location.website)
        elastic_index.add_document(document=db_location, flush=True, latitude=latitude, longitude=longitude)
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
                        benefit_description="You can expect to have your own rainbow following you around afterwards",
                        coordinator_email="hello@study.com", categories=[], organization_name="Study Org"):

        study = Study(title=title, description=description, participant_description=participant_description,
                      benefit_description=benefit_description, status=Status.currently_enrolling,
                      coordinator_email=coordinator_email, organization_name=organization_name)

        db.session.add(study)
        db.session.commit()
        db_study = db.session.query(Study).filter_by(title=study.title).first()
        self.assertEqual(db_study.description, description)

        for category in categories:
            sc = StudyCategory(study_id=db_study.id, category_id=category.id)
            db.session.add(sc)

        db.session.commit()
        elastic_index.add_document(db_study, 'Study')

        db_study = db.session.query(Study).filter_by(id=db_study.id).first()
        self.assertEqual(len(db_study.categories), len(categories))

        return db_study

    def construct_investigator(self, name="Judith Wonder", title="Ph.D., Assistant Professor of Mereology"):

        investigator = Investigator(name=name, title=title)
        investigator.organization_name = "Investigator Org"
        db.session.add(investigator)
        db.session.commit()

        db_inv = db.session.query(Investigator).filter_by(name=investigator.name).first()
        self.assertEqual(db_inv.title, investigator.title)
        return db_inv

    def construct_event(self, title="A+ Event", description="A delightful event destined to create rejoicing",
                        street_address1="123 Some Pl", street_address2="Apt. 45", is_draft=False, city="Stauntonville",
                        state="QX", zip="99775", phone="555-555-5555", website="http://stardrive.org",
                        date=datetime.datetime.now() + datetime.timedelta(days=7), organization_name="Event Org"):

        event = Event(title=title, description=description, street_address1=street_address1,
                      street_address2=street_address2, city=city, state=state, zip=zip, phone=phone, website=website,
                      date=date, is_draft=is_draft, organization_name=organization_name)
        db.session.add(event)

        db_event = db.session.query(Event).filter_by(title=event.title).first()
        self.assertEqual(db_event.website, event.website)
        elastic_index.add_document(db_event, 'Event')
        return db_event

    def construct_zip_code(self, id=24401, latitude=38.146216, longitude=-79.07625):
        z = ZipCode(id=id, latitude=latitude, longitude=longitude)
        db.session.add(z)
        db.session.commit()

        db_z = ZipCode.query.filter_by(id=id).first()
        self.assertEqual(db_z.id, z.id)
        self.assertEqual(db_z.latitude, z.latitude)
        self.assertEqual(db_z.longitude, z.longitude)
        return db_z

    def construct_everything(self):
        self.construct_all_questionnaires()
        cat = self.construct_category()
        self.construct_resource()
        study = self.construct_study()
        location = self.construct_location()
        event = self.construct_event()
        self.construct_location_category(location.id, cat.name)
        self.construct_study_category(study.id, cat.name)
        self.construct_zip_code()
        investigator = Investigator(name="Sam I am")
        db.session.add(StudyInvestigator(study=study, investigator=investigator))
        db.session.add(StudyUser(study=study, user=self.construct_user()))
        db.session.add(AdminNote(user_id=self.construct_user().id, resource_id=self.construct_resource().id, note=''))
        db.session.add(UserFavorite(user_id=self.construct_user().id))
        db.session.add(investigator)
        db.session.add(EmailLog())
        db.session.add(ResourceChangeLog())
        db.session.add(StepLog())
        db.session.commit()
