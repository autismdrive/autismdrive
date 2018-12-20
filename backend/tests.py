# Set environment variable to testing before loading.
# IMPORTANT - Environment must be loaded before app, models, etc....
import os
os.environ["APP_CONFIG_FILE"] = '../config/testing.py'

import unittest
import json
import random
import string
import re
import base64
import quopri
import datetime

from app.email_service import TEST_MESSAGES
from app.model.email_log import EmailLog
from app.model.organization import Organization
from app.model.resource import StarResource
from app.model.study import Study
from app.model.training import Training
from app.model.user import User
from app import app, db


class TestCase(unittest.TestCase):

    def setUp(self):
        self.ctx = app.test_request_context()
        self.app = app.test_client()
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.ctx.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # elastic_index.clear()
        self.ctx.pop()

    def assertSuccess(self, rv):
        try:
            data = json.loads(rv.get_data(as_text=True))
            self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                            "BAD Response: %i. \n %s" %
                            (rv.status_code, json.dumps(data)))
        except:
            self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                            "BAD Response: %i." % rv.status_code)

    def randomString(self):
        char_set = string.ascii_uppercase + string.digits
        return ''.join(random.sample(char_set * 6, 6))

    def test_base_endpoint(self):
        rv = self.app.get('/',
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertTrue("_links" in response)
        self.assertTrue("resources" in response['_links'])
        self.assertTrue("studies" in response['_links'])
        self.assertTrue("trainings" in response['_links'])
        self.assertTrue("users" in response['_links'])

    def construct_resource(self, title="A+ Resource", description="A delightful Resource destined to create rejoicing",
                           image_url="assets/image.svg", image_caption="An inspiring photograph of great renown",
                           street_address1="123 Some Pl", street_address2="Apt. 45",
                           city="Stauntonville", state="QX", zip="99775", county="Augustamarle", phone="555-555-5555",
                           website="http://stardrive.org"):

        resource = StarResource(title=title, description=description, image_url=image_url, image_caption=image_caption,
                                street_address1=street_address1, street_address2=street_address2, city=city,
                                state=state, zip=zip, county=county, phone=phone, website=website)
        resource.organization_id = self.construct_organization().id
        db.session.add(resource)
        db.session.commit()

        db_resource = db.session.query(StarResource).filter_by(title=resource.title).first()
        self.assertEqual(db_resource.website, resource.website)
        return db_resource

    def construct_study(self, title="Fantastic Study", description="A study that will go down in history",
                        researcher_description="Fantastic people work on this fantastic study. You should be impressed",
                        participant_description="Even your pet hamster could benefit from participating in this study",
                        outcomes_description="You can expect to have your own rainbow following you around after participating",
                        enrollment_start_date=datetime.date(2019, 1, 20), current_num_participants="54", max_num_participants="5000",
                        start_date=datetime.date(2019, 2, 1), end_date=datetime.date(2019, 3, 31)):

        study = Study(title=title, description=description, researcher_description=researcher_description,
                      participant_description=participant_description, outcomes_description=outcomes_description,
                      enrollment_start_date=enrollment_start_date, current_num_participants=current_num_participants,
                      max_num_participants=max_num_participants, start_date=start_date, end_date=end_date)
        study.organization_id = self.construct_organization().id
        db.session.add(study)
        db.session.commit()

        db_study = db.session.query(Study).filter_by(title=study.title).first()
        self.assertEqual(db_study.description, study.description)
        return db_study

    def construct_training(self, title="Best Training", description="A training to end all trainings",
                           outcomes_description="Increased intelligence and the ability to do magic tricks.",
                           image_url="assets/image.png", image_caption="One of the magic tricks you will learn"):

        training = Training(title=title, description=description, outcomes_description=outcomes_description, image_url=image_url,
                            image_caption=image_caption)
        training.organization_id = self.construct_organization().id
        db.session.add(training)
        db.session.commit()

        db_training = db.session.query(Training).filter_by(title=training.title).first()
        self.assertEqual(db_training.outcomes_description, training.outcomes_description)
        return db_training

    def construct_organization(self, name="Staunton Makerspace", description="A place full of surprise, delight, and amazing people. And tools. Lots of exciting tools."):

        organization = Organization(name=name, description=description)
        db.session.add(organization)
        db.session.commit()

        db_org = db.session.query(Organization).filter_by(name=organization.name).first()
        self.assertEqual(db_org.description, organization.description)
        return db_org

    def construct_user(self, first_name="Stan", last_name="Ton", email="stan@staunton.com", role="Self"):

        user = User(first_name=first_name, last_name=last_name, email=email, role=role)
        db.session.add(user)
        db.session.commit()

        db_user = db.session.query(User).filter_by(email=user.email).first()
        self.assertEqual(db_user.first_name, user.first_name)
        return db_user

    def construct_admin_user(self, first_name="Rich", last_name="Mond", email="rmond@virginia.gov", role="Admin"):

        user = User(first_name=first_name, last_name=last_name, email=email, role=role)
        db.session.add(user)
        db.session.commit()

        db_user = db.session.query(User).filter_by(email=user.email).first()
        self.assertEqual(db_user.first_name, user.first_name)
        return db_user

    def test_resource_basics(self):
        self.construct_resource()
        r = db.session.query(StarResource).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/resource/%i' % r_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], r_id)
        self.assertEqual(response["title"], 'A+ Resource')
        self.assertEqual(response["description"], 'A delightful Resource destined to create rejoicing')

    def test_modify_resource_basics(self):
        self.construct_resource()
        r = db.session.query(StarResource).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.app.get('/api/resource/%i' % r_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        response['website'] = 'http://sartography.com'
        response['county'] = 'Rockingbridge'
        response['image_caption'] = 'Daniel GG Dog Da Funk-a-funka'
        orig_date = response['last_updated']
        rv = self.app.put('/api/resource/%i' % r_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/resource/%i' % r_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['website'], 'http://sartography.com')
        self.assertEqual(response['county'], 'Rockingbridge')
        self.assertEqual(response['image_caption'], 'Daniel GG Dog Da Funk-a-funka')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_resource(self):
        r = self.construct_resource()
        r_id = r.id
        rv = self.app.get('api/resource/%i' % r_id, content_type="applicaiton/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/resource/%i' % r_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/resource/%i' % r_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_resource(self):
        resource = {'title':"Resource of Resources", 'description':"You need this resource in your life."}
        rv = self.app.post('api/resource', data=json.dumps(resource), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Resource of Resources')
        self.assertEqual(response['description'], 'You need this resource in your life.')
        self.assertIsNotNone(response['id'])

    def test_study_basics(self):
        self.construct_study()
        s = db.session.query(Study).first()
        self.assertIsNotNone(s)
        s_id = s.id
        rv = self.app.get('/api/study/%i' % s_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], s_id)
        self.assertEqual(response["title"], 'Fantastic Study')
        self.assertEqual(response["description"], 'A study that will go down in history')

    def test_modify_study_basics(self):
        self.construct_study()
        s = db.session.query(Study).first()
        self.assertIsNotNone(s)
        s_id = s.id
        rv = self.app.get('/api/study/%i' % s_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        response['outcomes_description'] = 'Better fluids for you and your car, Duh.'
        response['max_num_participants'] = '2'
        orig_date = response['last_updated']
        rv = self.app.put('/api/study/%i' % s_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/study/%i' % s_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['outcomes_description'], 'Better fluids for you and your car, Duh.')
        self.assertEqual(response['max_num_participants'], 2)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_study(self):
        s = self.construct_study()
        s_id = s.id
        rv = self.app.get('api/study/%i' % s_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/study/%i' % s_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/study/%i' % s_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_study(self):
        study = {'title':"Study of Studies", 'outcomes_description':"This study will change your life."}
        rv = self.app.post('api/study', data=json.dumps(study), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Study of Studies')
        self.assertEqual(response['outcomes_description'], 'This study will change your life.')
        self.assertIsNotNone(response['id'])

    def test_training_basics(self):
        self.construct_training()
        t = db.session.query(Training).first()
        self.assertIsNotNone(t)
        t_id = t.id
        rv = self.app.get('/api/training/%i' % t_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], t_id)
        self.assertEqual(response["title"], 'Best Training')
        self.assertEqual(response["description"], 'A training to end all trainings')

    def test_modify_training_basics(self):
        self.construct_training()
        t = db.session.query(Training).first()
        self.assertIsNotNone(t)
        t_id = t.id
        rv = self.app.get('/api/training/%i' % t_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        response['outcomes_description'] = 'Better fluids for you and your car, Duh.'
        response['image_caption'] = 'A nice cool glass of lemonade'
        orig_date = response['last_updated']
        rv = self.app.put('/api/training/%i' % t_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/training/%i' % t_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['outcomes_description'], 'Better fluids for you and your car, Duh.')
        self.assertEqual(response['image_caption'], 'A nice cool glass of lemonade')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_training(self):
        t = self.construct_training()
        t_id = t.id
        rv = self.app.get('api/training/%i' % t_id, content_type="applicaiton/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/training/%i' % t_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/training/%i' % t_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_training(self):
        training = {'title':"Training of Trainings", 'outcomes_description':"This training will change your life."}
        rv = self.app.post('api/training', data=json.dumps(training), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Training of Trainings')
        self.assertEqual(response['outcomes_description'], 'This training will change your life.')
        self.assertIsNotNone(response['id'])


    def test_organization_basics(self):
        self.construct_organization()
        o = db.session.query(Organization).first()
        self.assertIsNotNone(o)
        o_id = o.id
        rv = self.app.get('/api/organization/%i' % o_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], o_id)
        self.assertEqual(response["name"], 'Staunton Makerspace')
        self.assertEqual(response["description"], 'A place full of surprise, delight, and amazing people. And tools. Lots of exciting tools.')

    def test_modify_organization_basics(self):
        self.construct_organization()
        o = db.session.query(Organization).first()
        self.assertIsNotNone(o)
        o_id = o.id
        rv = self.app.get('/api/organization/%i' % o_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['name'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        orig_date = response['last_updated']
        rv = self.app.put('/api/organization/%i' % o_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/organization/%i' % o_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_organization(self):
        o = self.construct_organization()
        o_id = o.id
        rv = self.app.get('api/organization/%i' % o_id, content_type="applicaiton/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/organization/%i' % o_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/organization/%i' % o_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_organization(self):
        organization = {'name':"Organization of Champions", 'description':"All the best people, all the time."}
        rv = self.app.post('api/organization', data=json.dumps(organization), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'Organization of Champions')
        self.assertEqual(response['description'], 'All the best people, all the time.')
        self.assertIsNotNone(response['id'])

    def test_user_basics(self):
        self.construct_user()
        u = db.session.query(User).first()
        self.assertIsNotNone(u)
        u_id = u.id
        rv = self.app.get('/api/user/%i' % u_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], u_id)
        self.assertEqual(response["first_name"], 'Stan')
        self.assertEqual(response["email"], 'stan@staunton.com')

    def test_modify_user_basics(self):
        self.construct_user()
        u = db.session.query(User).first()
        self.assertIsNotNone(u)
        u_id = u.id
        rv = self.app.get('/api/user/%i' % u_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['first_name'] = 'Edwarardo'
        response['last_name'] = 'Lemonado'
        response['role'] = 'Owner'
        response['email'] = 'ed@edwardos.com'
        orig_date = response['last_updated']
        rv = self.app.put('/api/user/%i' % u_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/user/%i' % u_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['first_name'], 'Edwarardo')
        self.assertEqual(response['last_name'], 'Lemonado')
        self.assertEqual(response['role'], 'Owner')
        self.assertEqual(response['email'], 'ed@edwardos.com')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_user(self):
        u = self.construct_user()
        u_id = u.id
        rv = self.app.get('api/user/%i' % u_id, content_type="applicaiton/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/user/%i' % u_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/user/%i' % u_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_user(self):
        user = {'first_name':"Tarantella", 'last_name':"Arachnia", 'role':"Widow", 'email':"tara@spiders.org"}
        rv = self.app.post('api/user', data=json.dumps(user), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['first_name'], 'Tarantella')
        self.assertEqual(response['last_name'], 'Arachnia')
        self.assertEqual(response['role'], 'Widow')
        self.assertIsNotNone(response['id'])

    def logged_in_headers(self, user=None):
        # If no user is provided, generate a dummy Admin user
        if not user:
            user = User(
                id=7,
                first_name="Admin",
                email="admin@admin.org",
                password="myPass457",
                email_verified=True,
                role="Admin")

        # Add user if it's not already in database
        if user.id:
            existing_user = User.query.filter_by(id=user.id).first()
        if not existing_user and user.email:
            existing_user = User.query.filter_by(email=user.email).first()

        if not existing_user:
            db.session.add(user)
            db.session.commit()

        data = {
            'email': user.email,
            'password': 'myPass457'
        }

        rv = self.app.post(
            '/api/login_password',
            data=json.dumps(data),
            content_type="application/json")

        db_user = User.query.filter_by(email=user.email).first()
        return dict(
            Authorization='Bearer ' + db_user.encode_auth_token().decode())

    def test_create_user_with_password(self, first_name="Peter", id=8,
                                       email="tyrion@got.com", role="User", password="peterpass"):
        data = {
            "first_name": first_name,
            "id": id,
            "email": email,
            "role": role
        }
        rv = self.app.post(
            '/api/user',
            data=json.dumps(data),
            follow_redirects=True,
            headers=self.logged_in_headers(),
            content_type="application/json")
        self.assertSuccess(rv)
        user = User.query.filter_by(id=id).first()
        user.password = password
        db.session.add(user)
        db.session.commit()

        rv = self.app.get(
            '/api/user/%i' % user.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(first_name, response["first_name"])
        self.assertEqual(email, response["email"])
        self.assertEqual(role, response["role"])
        self.assertEqual(True, user.is_correct_password(password))

        return user

    def test_login_user(self):
        user = self.test_create_user_with_password()
        data = {"email": "tyrion@got.com", "password": "peterpass"}
        # Login shouldn't work with email not yet verified
        rv = self.app.post(
            '/api/login_password',
            data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(400, rv.status_code)

        user.email_verified = True
        rv = self.app.post(
            '/api/login_password',
            data=json.dumps(data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response["token"])

        return user

    def test_get_current_user(self):
        """ Test for the current user status """
        user = self.test_login_user()

        # Now get the user back.
        response = self.app.get(
            '/api/session',
            headers=dict(
                Authorization='Bearer ' + user.encode_auth_token().decode()))
        self.assertSuccess(response)
        return json.loads(response.data.decode())

    def decode(self, encoded_words):
        """
        Useful for checking the content of email messages
        (which we store in an array for testing)
        """
        encoded_word_regex = r'=\?{1}(.+)\?{1}([b|q])\?{1}(.+)\?{1}='
        charset, encoding, encoded_text = re.match(encoded_word_regex,
                                                   encoded_words).groups()
        if encoding is 'b':
            byte_string = base64.b64decode(encoded_text)
        elif encoding is 'q':
            byte_string = quopri.decodestring(encoded_text)
        text = byte_string.decode(charset)
        text = text.replace("_", " ")
        return text

    def test_register_sends_email(self):
        message_count = len(TEST_MESSAGES)
        self.test_create_user_with_password()
        self.assertGreater(len(TEST_MESSAGES), message_count)
        self.assertEqual("STAR Drive: Confirm Email",
                         self.decode(TEST_MESSAGES[-1]['subject']))

        logs = EmailLog.query.all()
        self.assertIsNotNone(logs[-1].tracking_code)

    def test_forgot_password_sends_email(self):
        user = self.test_create_user_with_password()
        message_count = len(TEST_MESSAGES)
        data = {"email": user.email}
        rv = self.app.post(
            '/api/forgot_password',
            data=json.dumps(data),
            content_type="application/json")
        self.assertSuccess(rv)
        self.assertGreater(len(TEST_MESSAGES), message_count)
        self.assertEqual("STAR Drive: Password Reset Email",
                         self.decode(TEST_MESSAGES[-1]['subject']))

        logs = EmailLog.query.all()
        self.assertIsNotNone(logs[-1].tracking_code)

    def test_get_current_user(self):
        """ Test for the current user status """
        self.test_create_user_with_password(id=9)

        user = User.query.filter_by(id=9).first()

        # Now get the user back.
        response = self.app.get(
            '/api/session',
            headers=dict(
                Authorization='Bearer ' + user.encode_auth_token().decode()))
        self.assertSuccess(response)
        return json.loads(response.data.decode())