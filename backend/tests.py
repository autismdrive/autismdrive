# Set environment variable to testing before loading.
# IMPORTANT - Environment must be loaded before app, models, etc....
import os
os.environ["APP_CONFIG_FILE"] = '../config/testing.py'

import unittest
import json
import random
import string

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
                           image="assets/image.svg", image_caption="An inspiring photograph of great renown",
                           organization="UVA", street_address1="123 Some Pl", street_address2="Apt. 45",
                           city="Stauntonville", state="QX", zip="99775", county="Augustamarle", phone="555-555-5555",
                           website="http://stardrive.org"):

        resource = StarResource(title=title, description=description, image=image, image_caption=image_caption,
                                organization=organization, street_address1=street_address1,
                                street_address2=street_address2, city=city, state=state, zip=zip, county=county,
                                phone=phone, website=website)
        db.session.add(resource)
        db.session.commit()
        return resource

    def construct_study(self, title="Fantastic Study", description="A study that will go down in history",
                        researcher_description="Fantastic people work on this fantastic study. You should be impressed",
                        participant_description="Even your pet hamster could benefit from participating in this study",
                        outcomes="You can expect to have your own rainbow following you around after participating",
                        enrollment_date="2019-01-20 00:00:00", current_enrolled="54", total_participants="5000",
                        study_start="2019-02-01 00:00:00", study_end="2019-03-31 00:00:00"):

        study = Study(title=title, description=description, researcher_description=researcher_description,
                      participant_description=participant_description, outcomes=outcomes,
                      enrollment_date=enrollment_date, current_enrolled=current_enrolled,
                      total_participants=total_participants, study_start=study_start, study_end=study_end)
        db.session.add(study)
        db.session.commit()
        return study

    def construct_training(self, title="Best Training", description="A training to end all trainings",
                           outcomes="Increased intelligence and the ability to do magic tricks.",
                           image="assets/image.png", image_caption="One of the magic tricks you will learn"):

        training= Training(title=title, description=description, outcomes=outcomes, image=image,
                           image_caption=image_caption)
        db.session.add(training)
        db.session.commit()
        return training

    def construct_user(self, first_name="Stan", last_name="Ton", email="stan@staunton.com", role="Self"):

        user = User(first_name=first_name, last_name=last_name, email=email, role=role)
        db.session.add(user)
        db.session.commit()
        return user

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
        response['outcomes'] = 'Better fluids for you and your car, Duh.'
        response['total_participants'] = '2'
        orig_date = response['last_updated']
        rv = self.app.put('/api/study/%i' % s_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/study/%i' % s_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['outcomes'], 'Better fluids for you and your car, Duh.')
        self.assertEqual(response['total_participants'], 2)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_study(self):
        s = self.construct_study()
        s_id = s.id
        rv = self.app.get('api/study/%i' % s_id, content_type="applicaiton/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/study/%i' % s_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/study/%i' % s_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_study(self):
        study = {'title':"Study of Studies", 'outcomes':"This study will change your life."}
        rv = self.app.post('api/study', data=json.dumps(study), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Study of Studies')
        self.assertEqual(response['outcomes'], 'This study will change your life.')
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
        response['outcomes'] = 'Better fluids for you and your car, Duh.'
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
        self.assertEqual(response['outcomes'], 'Better fluids for you and your car, Duh.')
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
        training = {'title':"Training of Trainings", 'outcomes':"This training will change your life."}
        rv = self.app.post('api/training', data=json.dumps(training), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Training of Trainings')
        self.assertEqual(response['outcomes'], 'This training will change your life.')
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
