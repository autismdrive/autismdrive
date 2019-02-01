# Set environment variable to testing before loading.
# IMPORTANT - Environment must be loaded before app, models, etc....
import os

os.environ["APP_CONFIG_FILE"] = '../config/testing.py'


from app.model.progress_log import ProgressLog
from app.question_service import QuestionService
import re
import json
import base64
import quopri
import random
import string
import datetime
import unittest
from app import db, app
from app.model.user import User
from app.model.study import Study
from app.email_service import TEST_MESSAGES
from app.model.category import Category
from app.model.resource import StarResource
from app.model.training import Training
from app.model.email_log import EmailLog
from app.model.organization import Organization
from app.model.participant import Participant
from app.model.user_participant import UserParticipant
from app.model.study_category import StudyCategory
from app.model.resource_category import ResourceCategory
from app.model.training_category import TrainingCategory
from app.model.questionnaires.contact_questionnaire import ContactQuestionnaire
from app.model.questionnaires.demographics_questionnaire import DemographicsQuestionnaire
from app.model.questionnaires.evaluation_history_questionnaire import EvaluationHistoryQuestionnaire

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

        endpoints = [
            ('api.categorybyresourceendpoint', '/api/resource/<resource_id>/category'),
            ('api.categorybystudyendpoint', '/api/study/<study_id>/category'),
            ('api.categorybytrainingendpoint', '/api/training/<training_id>/category'),
            ('api.categoryendpoint', '/api/category/<id>'),
            ('api.categorylistendpoint', '/api/category'),
            ('api.questionnaireendpoint', '/api/q/<name>/<id>'),
            ('api.organizationendpoint', '/api/organization/<id>'),
            ('api.organizationlistendpoint', '/api/organization'),
            ('api.resourcebycategoryendpoint', '/api/category/<category_id>/resource'),
            ('api.resourcecategoryendpoint', '/api/resource_category/<id>'),
            ('api.resourcecategorylistendpoint', '/api/resource_category'),
            ('api.resourceendpoint', '/api/resource/<id>'),
            ('api.resourcelistendpoint', '/api/resource'),
            ('api.rootcategorylistendpoint', '/api/category/root'),
            ('api.sessionendpoint', '/api/session'),
            ('api.studybycategoryendpoint', '/api/category/<category_id>/study'),
            ('api.studycategoryendpoint', '/api/study_category/<id>'),
            ('api.studycategorylistendpoint', '/api/study_category'),
            ('api.studyendpoint', '/api/study/<id>'),
            ('api.studylistendpoint', '/api/study'),
            ('api.trainingbycategoryendpoint', '/api/category/<category_id>/training'),
            ('api.trainingcategoryendpoint', '/api/training_category/<id>'),
            ('api.trainingcategorylistendpoint', '/api/training_category'),
            ('api.trainingendpoint', '/api/training/<id>'),
            ('api.traininglistendpoint', '/api/training'),
            ('api.userendpoint', '/api/user/<id>'),
            ('api.userlistendpoint', '/api/user'),
            ('auth.forgot_password', '/api/forgot_password'),
            ('auth.login_password', '/api/login_password'),
            ('auth.reset_password', '/api/reset_password'),
        ]

        for endpoint in endpoints:
            self.assertEqual(response[endpoint[0]], endpoint[1])

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

    def construct_category(self, name="Ultimakers", parent=None):

        category = Category(name=name)
        if parent is not None:
            category.parent = parent
        db.session.add(category)
        db.session.commit()

        db_category = db.session.query(Category).filter_by(name=category.name).first()
        self.assertIsNotNone(db_category.id)
        return db_category

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

    def construct_participant(self, first_name="Wayne", last_name="Boro", user=None, relationship=None):
        participant = Participant(first_name=first_name, last_name=last_name)

        if user is not None and relationship is not None:
            r = UserParticipant(participant=participant, user = user, relationship=relationship)
            db.session.add(r)

        db.session.add(participant)
        db.session.commit()

        db_participant = db.session.query(Participant).filter_by(last_name=participant.last_name).first()
        self.assertEqual(db_participant.first_name, participant.first_name)
        return db_participant

    def construct_contact_questionnaire(self, phone="123-456-7890", zip=55678, marketing_channel="Zine Ad",
                                        participant=None, user=None):

        cq = ContactQuestionnaire(phone=phone, zip=zip,
                                  marketing_channel=marketing_channel)
        if participant is None:
            cq.participant_id = self.construct_participant().id
        else:
            cq.participant_id = participant.id

        if user is None:
            cq.user_id = self.construct_user().id
        else:
            cq.user_id = user.id

        db.session.add(cq)
        db.session.commit()

        db_cq = db.session.query(ContactQuestionnaire).filter_by(zip=cq.zip).first()
        self.assertEqual(db_cq.phone, cq.phone)
        return db_cq

    def construct_demographics_questionnaire(self, birth_sex="intersex", gender_identity="intersex",
                                             race_ethnicity="raceBlack", participant=None, user=None):

        dq = DemographicsQuestionnaire(birth_sex=birth_sex, gender_identity=gender_identity,
                                       race_ethnicity=race_ethnicity)
        if participant is None:
            dq.participant_id = self.construct_participant(first_name="Trina", last_name="Frina").id
        else:
            dq.participant_id = participant.id

        if user is None:
            dq.user_id = self.construct_user(email="user@study.com").id
        else:
            dq.user_id = user.id

        db.session.add(dq)
        db.session.commit()

        db_dq = db.session.query(DemographicsQuestionnaire).filter_by(birth_sex=dq.birth_sex).first()
        self.assertEqual(db_dq.gender_identity, dq.gender_identity)
        return db_dq

    def construct_evaluation_history_questionnaire(self, self_identifies_autistic=True, has_autism_diagnosis=True,
                                                   years_old_at_first_diagnosis=7, who_diagnosed="pediatrician",
                                                   participant=None, user=None):

        ehq = EvaluationHistoryQuestionnaire(self_identifies_autistic=self_identifies_autistic,
                                             has_autism_diagnosis=has_autism_diagnosis,
                                             years_old_at_first_diagnosis=years_old_at_first_diagnosis,
                                             who_diagnosed=who_diagnosed)
        if participant is None:
            ehq.participant_id = self.construct_participant(last_name="Silamona").id
        else:
            ehq.participant_id = participant.id

        if user is None:
            ehq.user_id = self.construct_user(email="user@study.com").id
        else:
            ehq.user_id = user.id

        db.session.add(ehq)
        db.session.commit()

        db_ehq = db.session.query(EvaluationHistoryQuestionnaire).filter_by(
            years_old_at_first_diagnosis=ehq.years_old_at_first_diagnosis).first()
        self.assertEqual(db_ehq.who_diagnosed, ehq.who_diagnosed)
        return db_ehq

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
        rv = self.app.get('api/resource/%i' % r_id, content_type="application/json")
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
        rv = self.app.get('api/training/%i' % t_id, content_type="application/json")
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
        rv = self.app.get('api/organization/%i' % o_id, content_type="application/json")
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

    def test_category_basics(self):
        self.construct_category()
        c = db.session.query(Category).first()
        self.assertIsNotNone(c)
        c_id = c.id
        c.parent = self.construct_category(name="3d Printers")
        rv = self.app.get('/api/category/%i' % c_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], c_id)
        self.assertEqual(response["name"], 'Ultimakers')
        self.assertEqual(response["parent"]["name"], '3d Printers')

    def test_modify_category_basics(self):
        self.construct_category()
        c = db.session.query(Category).first()
        self.assertIsNotNone(c)
        c_id = c.id
        c.parent = self.construct_category(name="3d Printers")
        rv = self.app.get('/api/category/%i' % c_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['name'] = 'JellyBoxes'
        new_parent = self.construct_category(name="Strange Kitchen Gadgets")
        response['parent_id'] = new_parent.id
        rv = self.app.put('/api/category/%i' % c_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/category/%i' % c_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'JellyBoxes')
        self.assertEqual(response['parent']['name'], 'Strange Kitchen Gadgets')

    def test_delete_category(self):
        c = self.construct_category()
        c_id = c.id
        rv = self.app.get('api/category/%i' % c_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/category/%i' % c_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/category/%i' % c_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_category(self):
        category = {'name': "My Favorite Things"}
        rv = self.app.post('api/category', data=json.dumps(category), content_type="application/json",
                           follow_redirects=True)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'My Favorite Things')
        self.assertIsNotNone(response['id'])

    def test_category_has_links(self):
        self.construct_category()
        rv = self.app.get(
            '/api/category/1',
            follow_redirects=True,
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["_links"]["self"], '/api/category/1')
        self.assertEqual(response["_links"]["collection"], '/api/category')

    def test_category_has_children(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent=c1)
        rv = self.app.get(
            '/api/category/1',
            follow_redirects=True,
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["children"][0]['id'], 2)
        self.assertEqual(response["children"][0]['name'], "I'm the kid")

    def test_category_has_parents_and_that_parent_has_no_children(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent=c1)
        c3 = self.construct_category(name="I'm the grand kid", parent=c2)
        rv = self.app.get(
            '/api/category/3',
            follow_redirects=True,
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["parent"]['id'], 2)
        self.assertNotIn("children", response["parent"])

    def test_category_depth_is_limited(self):
        c1 = self.construct_category()
        c2 = self.construct_category(
            name="I'm the kid", parent=c1)
        c3 = self.construct_category(
            name="I'm the grand kid",
            parent=c2)
        c4 = self.construct_category(
            name="I'm the great grand kid",
            parent=c3)

        rv = self.app.get(
            '/api/category',
            follow_redirects=True,
            content_type="application/json")

        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))

        self.assertEqual(1, len(response))
        self.assertEqual(1, len(response[0]["children"]))

    def test_get_resource_by_category(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c)
        db.session.add(cr)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/resource' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(r.id, response[0]["id"])
        self.assertEqual(r.description, response[0]["resource"]["description"])

    def test_get_resource_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c)
        cr2 = ResourceCategory(resource=r, category=c2)
        db.session.add_all([cr, cr2])
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/resource' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(r.id, response[0]["id"])
        self.assertEqual(2,
                         len(response[0]["resource"]["resource_categories"]))
        self.assertEqual(
            "c1", response[0]["resource"]["resource_categories"][0]["category"]
            ["name"])

    def test_category_resource_count(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c)
        db.session.add(cr)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["resource_count"])

    def test_get_category_by_resource(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c)
        db.session.add(cr)
        db.session.commit()
        rv = self.app.get(
            '/api/resource/%i/category' % r.id,
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_resource(self):
        c = self.construct_category()
        r = self.construct_resource()

        rc_data = {"resource_id": r.id, "category_id": c.id}

        rv = self.app.post(
            '/api/resource_category',
            data=json.dumps(rc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(r.id, response["resource_id"])

    def test_set_all_categories_on_resource(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        r = self.construct_resource()

        rc_data = [
            {
                "category_id": c1.id
            },
            {
                "category_id": c2.id
            },
            {
                "category_id": c3.id
            },
        ]
        rv = self.app.post(
            '/api/resource/%i/category' % r.id,
            data=json.dumps(rc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        rc_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/resource/%i/category' % r.id,
            data=json.dumps(rc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_resource(self):
        self.test_add_category_to_resource()
        rv = self.app.delete('/api/resource_category/%i' % 1)
        self.assertSuccess(rv)
        rv = self.app.get(
            '/api/resource/%i/category' % 1, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_get_study_by_category(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        db.session.add(cs)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/study' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(s.id, response[0]["id"])
        self.assertEqual(s.description, response[0]["study"]["description"])

    def test_get_study_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        cs2 = StudyCategory(study=s, category=c2)
        db.session.add_all([cs, cs2])
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/study' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(s.id, response[0]["id"])
        self.assertEqual(2,
                         len(response[0]["study"]["study_categories"]))
        self.assertEqual(
            "c1", response[0]["study"]["study_categories"][0]["category"]
            ["name"])

    def test_category_study_count(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        db.session.add(cs)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["study_count"])

    def test_get_category_by_study(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        db.session.add(cs)
        db.session.commit()
        rv = self.app.get(
            '/api/study/%i/category' % s.id,
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_study(self):
        c = self.construct_category()
        s = self.construct_study()

        sc_data = {"study_id": s.id, "category_id": c.id}

        rv = self.app.post(
            '/api/study_category',
            data=json.dumps(sc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(s.id, response["study_id"])

    def test_set_all_categories_on_study(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        s = self.construct_study()

        sc_data = [
            {
                "category_id": c1.id
            },
            {
                "category_id": c2.id
            },
            {
                "category_id": c3.id
            },
        ]
        rv = self.app.post(
            '/api/study/%i/category' % s.id,
            data=json.dumps(sc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        sc_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/study/%i/category' % s.id,
            data=json.dumps(sc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_study(self):
        self.test_add_category_to_study()
        rv = self.app.delete('/api/study_category/%i' % 1)
        self.assertSuccess(rv)
        rv = self.app.get(
            '/api/study/%i/category' % 1, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_get_training_by_category(self):
        c = self.construct_category()
        t = self.construct_training()
        ct = TrainingCategory(training=t, category=c)
        db.session.add(ct)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/training' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(t.id, response[0]["id"])
        self.assertEqual(t.description, response[0]["training"]["description"])

    def test_get_training_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        t = self.construct_training()
        ct = TrainingCategory(training=t, category=c)
        ct2 = TrainingCategory(training=t, category=c2)
        db.session.add_all([ct, ct2])
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/training' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(t.id, response[0]["id"])
        self.assertEqual(2,
                         len(response[0]["training"]["training_categories"]))
        self.assertEqual(
            "c1", response[0]["training"]["training_categories"][0]["category"]
            ["name"])

    def test_category_training_count(self):
        c = self.construct_category()
        t = self.construct_training()
        ct = TrainingCategory(training=t, category=c)
        db.session.add(ct)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["training_count"])

    def test_get_category_by_training(self):
        c = self.construct_category()
        t = self.construct_training()
        ct = TrainingCategory(training=t, category=c)
        db.session.add(ct)
        db.session.commit()
        rv = self.app.get(
            '/api/training/%i/category' % t.id,
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_training(self):
        c = self.construct_category()
        t = self.construct_training()

        tc_data = {"training_id": t.id, "category_id": c.id}

        rv = self.app.post(
            '/api/training_category',
            data=json.dumps(tc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(t.id, response["training_id"])

    def test_set_all_categories_on_training(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        t = self.construct_training()

        tc_data = [
            {
                "category_id": c1.id
            },
            {
                "category_id": c2.id
            },
            {
                "category_id": c3.id
            },
        ]
        rv = self.app.post(
            '/api/training/%i/category' % t.id,
            data=json.dumps(tc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        tc_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/training/%i/category' % t.id,
            data=json.dumps(tc_data),
            content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_training(self):
        self.test_add_category_to_training()
        rv = self.app.delete('/api/training_category/%i' % 1)
        self.assertSuccess(rv)
        rv = self.app.get(
            '/api/training/%i/category' % 1, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_user_basics(self):
        self.construct_user()
        u = db.session.query(User).first()
        self.assertIsNotNone(u)
        u_id = u.id
        headers = self.logged_in_headers(u)
        rv = self.app.get('/api/user/%i' % u_id,
                          follow_redirects=True,
                          content_type="application/json", headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], u_id)
        self.assertEqual(response["first_name"], 'Stan')
        self.assertEqual(response["email"], 'stan@staunton.com')

    def test_modify_user_basics(self):
        self.construct_user()
        u = db.session.query(User).first()
        headers = self.logged_in_headers(u)
        self.assertIsNotNone(u)
        rv = self.app.get('/api/user/%i' % u.id, content_type="application/json", headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        response['first_name'] = 'Edwarardo'
        response['last_name'] = 'Lemonado'
        response['role'] = 'Owner'
        response['email'] = 'ed@edwardos.com'
        orig_date = response['last_updated']
        rv = self.app.put('/api/user/%i' % u.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=headers)
        self.assertSuccess(rv)
        rv = self.app.get('/api/user/%i' % u.id, content_type="application/json", headers=headers)
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

        rv = self.app.get('api/user/%i' % u_id, content_type="application/json")
        self.assertEquals(401, rv.status_code)
        rv = self.app.get('api/user/%i' % u_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)

        rv = self.app.delete('api/user/%i' % u_id, content_type="application/json", headers=None)
        self.assertEquals(401, rv.status_code)
        rv = self.app.delete('api/user/%i' % u_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)

        rv = self.app.get('api/user/%i' % u_id, content_type="application/json")
        self.assertEquals(401, rv.status_code)
        rv = self.app.get('api/user/%i' % u_id, content_type="application/json", headers=self.logged_in_headers())
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
        existing_user = None
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

    def test_participant_basics(self):
        self.construct_participant()
        p = db.session.query(Participant).first()
        self.assertIsNotNone(p)
        p_id = p.id
        rv = self.app.get('/api/participant/%i' % p_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], p_id)
        self.assertEqual(response["first_name"], p.first_name)
        self.assertEqual(response["last_name"], p.last_name)

    def test_modify_participant_you_do_not_own(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship="self")
        good_headers = self.logged_in_headers(u)

        p = db.session.query(Participant).first()
        odd_user = User(
                first_name="Frankie No good",
                email="frankie@badfella.fr",
                password="h@corleet",
                email_verified=True,
                role="User")
        participant = {'first_name': "Lil' Johnny", 'last_name': "Tables"}
        rv = self.app.put('/api/participant/%i' % p.id, data=json.dumps(participant), content_type="application/json",
                          follow_redirects=True)
        self.assertEqual(401, rv.status_code, "you have to be logged in to edit participant.")
        rv = self.app.put('/api/participant/%i' % p.id, data=json.dumps(participant), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers(odd_user))
        self.assertEqual(400, rv.status_code, "you have to have a relationship with the user to do stuff.")
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual("unrelated_participant", response['code'])
        rv = self.app.put('/api/participant/%i' % p.id, data=json.dumps(participant), content_type="application/json",
                          follow_redirects=True, headers=good_headers)
        self.assertEqual(200, rv.status_code, "The owner can edit the user.")

    def test_modify_participant_you_do_own(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship="self")
        headers = self.logged_in_headers(u)
        participant = {'first_name': "My brand new", 'last_name': "name"}
        rv = self.app.put('/api/participant/%i' % p.id, data=json.dumps(participant), content_type="application/json",
                          follow_redirects=True, headers=headers)
        self.assertSuccess(rv)
        p = db.session.query(Participant).filter_by(id=p.id).first()
        self.assertEqual("My brand new", p.first_name)


    def test_modify_participant_basics_admin(self):
        self.construct_participant()
        p = db.session.query(Participant).first()
        self.assertIsNotNone(p)
        p_id = p.id
        rv = self.app.get('/api/participant/%i' % p_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        response['first_name'] = 'Edwarardo'
        response['last_name'] = 'Better'
        orig_date = response['last_updated']
        rv = self.app.put('/api/participant/%i' % p_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assertSuccess(rv)
        rv = self.app.get('/api/participant/%i' % p_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['first_name'], 'Edwarardo')
        self.assertEqual(response['last_name'], 'Better')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_participant(self):
        p = self.construct_participant()
        p_id = p.id
        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json")
        self.assertEquals(401, rv.status_code)
        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)

        rv = self.app.delete('api/participant/%i' % p_id, content_type="application/json")
        self.assertEquals(401, rv.status_code)
        rv = self.app.delete('api/participant/%i' % p_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)

        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json")
        self.assertEquals(401, rv.status_code)
        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_participant(self):

        participant = {'first_name': "Dorothy", 'last_name': "Edwards"}
        rv = self.app.post('/api/session/participant/dependent', data=json.dumps(participant), content_type="application/json",
                           follow_redirects=True)
        self.assertEquals(401, rv.status_code, "you can't create a participant without an account.")

        rv = self.app.post(
            '/api/session/participant/dependent', data=json.dumps(participant),
            content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)

        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response["participant_id"])
        self.assertIsNotNone(response["user_id"])
        self.assertEquals("dependent", response["relationship"])
        self.assertTrue("participant" in response)
        self.assertEquals("Dorothy", response["participant"]["first_name"])
        self.assertEquals("Edwards", response["participant"]["last_name"])


    def test_get_participant_by_user(self):
        u = self.construct_user()
        p = self.construct_participant()
        up = UserParticipant(user=u, participant=p, relationship="Self")
        db.session.add(up)
        db.session.commit()
        rv = self.app.get(
            '/api/user/%i' % u.id,
            content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(u.id, response['id'])
        self.assertEqual(1, len(response['participants']))
        self.assertEqual(p.first_name, response['participants'][0]["participant"]["first_name"])


    def test_contact_questionnaire_basics(self):
        self.construct_contact_questionnaire()
        cq = db.session.query(ContactQuestionnaire).first()
        self.assertIsNotNone(cq)
        cq_id = cq.id
        rv = self.app.get('/api/q/contact_questionnaire/%i' % cq_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], cq_id)
        self.assertEqual(response["phone"], cq.phone)
        self.assertEqual(response["marketing_channel"], cq.marketing_channel)

    def test_modify_contact_questionnaire_basics(self):
        self.construct_contact_questionnaire()
        cq = db.session.query(ContactQuestionnaire).first()
        self.assertIsNotNone(cq)
        cq_id = cq.id
        rv = self.app.get('/api/q/contact_questionnaire/%i' % cq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['phone'] = '123-456-7890'
        response['zip'] = 22345
        response['marketing_channel'] = 'flyer'
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/contact_questionnaire/%i' % cq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/contact_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['phone'], '123-456-7890')
        self.assertEqual(response['zip'], 22345)
        self.assertEqual(response['marketing_channel'], 'flyer')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_contact_questionnaire(self):
        cq = self.construct_contact_questionnaire()
        cq_id = cq.id
        rv = self.app.get('api/q/contact_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/contact_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/contact_questionnaire/%i' % cq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_contact_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship="self")
        headers = self.logged_in_headers(u)

        contact_questionnaire = {'phone': "123-456-7890", 'marketing_channel': "Subway sign", 'participant_id': p.id}
        rv = self.app.post('api/flow/intake/contact_questionnaire', data=json.dumps(contact_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['phone'], '123-456-7890')
        self.assertEqual(response['marketing_channel'], 'Subway sign')
        self.assertIsNotNone(response['id'])

    def test_demographics_questionnaire_basics(self):
        self.construct_demographics_questionnaire()
        dq = db.session.query(DemographicsQuestionnaire).first()
        self.assertIsNotNone(dq)
        dq_id = dq.id
        rv = self.app.get('/api/q/demographics_questionnaire/%i' % dq_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], dq_id)
        self.assertEqual(response["birth_sex"], dq.birth_sex)
        self.assertEqual(response["gender_identity"], dq.gender_identity)

    def test_modify_demographics_questionnaire_basics(self):
        self.construct_demographics_questionnaire()
        dq = db.session.query(DemographicsQuestionnaire).first()
        self.assertIsNotNone(dq)
        dq_id = dq.id
        rv = self.app.get('/api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['gender_identity'] = 'genderOther'
        response['race_ethnicity'] = 'raceOther'
        u2 = self.construct_user(email="rainbows@rainy.com")
        response['user_id'] = u2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/demographics_questionnaire/%i' % dq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['gender_identity'], 'genderOther')
        self.assertEqual(response['race_ethnicity'], 'raceOther')
        self.assertEqual(response['user_id'], u2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_demographics_questionnaire(self):
        dq = self.construct_demographics_questionnaire()
        dq_id = dq.id
        rv = self.app.get('api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/demographics_questionnaire/%i' % dq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_demographics_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship="self")
        headers = self.logged_in_headers(u)

        demographics_questionnaire = {'birth_sex': "female", 'gender_identity': "genderOther", 'participant_id': p.id}
        rv = self.app.post('api/flow/intake/demographics_questionnaire', data=json.dumps(demographics_questionnaire),
                           content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['birth_sex'], 'female')
        self.assertEqual(response['gender_identity'], 'genderOther')
        self.assertIsNotNone(response['id'])

    def test_evaluation_history_questionnaire_basics(self):
        self.construct_evaluation_history_questionnaire()
        ehq = db.session.query(EvaluationHistoryQuestionnaire).first()
        self.assertIsNotNone(ehq)
        ehq_id = ehq.id
        rv = self.app.get('/api/q/evaluation_history_questionnaire/%i' % ehq_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], ehq_id)
        self.assertEqual(response["self_identifies_autistic"], ehq.self_identifies_autistic)
        self.assertEqual(response["years_old_at_first_diagnosis"], ehq.years_old_at_first_diagnosis)

    def test_modify_evaluation_history_questionnaire_basics(self):
        self.construct_evaluation_history_questionnaire()
        ehq = db.session.query(EvaluationHistoryQuestionnaire).first()
        self.assertIsNotNone(ehq)
        ehq_id = ehq.id
        rv = self.app.get('/api/q/evaluation_history_questionnaire/%i' % ehq_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['self_identifies_autistic'] = False
        response['years_old_at_first_diagnosis'] = 12
        response['who_diagnosed'] = 'healthTeam'
        orig_date = response['last_updated']
        rv = self.app.put('/api/q/evaluation_history_questionnaire/%i' % ehq_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get('/api/q/evaluation_history_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_identifies_autistic'], False)
        self.assertEqual(response['years_old_at_first_diagnosis'], 12)
        self.assertEqual(response['who_diagnosed'], 'healthTeam')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_evaluation_history_questionnaire(self):
        ehq = self.construct_evaluation_history_questionnaire()
        ehq_id = ehq.id
        rv = self.app.get('api/q/evaluation_history_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.delete('api/q/evaluation_history_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertSuccess(rv)

        rv = self.app.get('api/q/evaluation_history_questionnaire/%i' % ehq_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_evaluation_history_questionnaire(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship="self")
        headers = self.logged_in_headers(u)

        evaluation_history_questionnaire = {'self_identifies_autistic': True, 'years_old_at_first_diagnosis': 5,
                                            'participant_id': p.id}
        rv = self.app.post('api/flow/intake/evaluation_history_questionnaire',
                           data=json.dumps(evaluation_history_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=headers)
        self.assertSuccess(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['self_identifies_autistic'], True)
        self.assertEqual(response['years_old_at_first_diagnosis'], 5)
        self.assertIsNotNone(response['id'])

    def test_questionnare_post_fails_if_flow_does_not_exist(self):
        evaluation_history_questionnaire = {'self_identifies_autistic': True, 'years_old_at_first_diagnosis': 5}
        rv = self.app.post('api/flow/noSuchFlow/evaluation_history_questionnaire',
                           data=json.dumps(evaluation_history_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code,
                          "This endpoint should require that the flow exists and that the question is in the flow.")
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response)
        self.assertEqual("Unknown path.", response["message"],
                          "There should be a clear error message explaining what went wrong.")

    def test_questionnare_post_fails_if_question_not_in_flow(self):
        evaluation_history_questionnaire = {'self_identifies_autistic': True, 'years_old_at_first_diagnosis': 5}
        rv = self.app.post('api/flow/intake/guardian_demographics_questionnaire',
                           data=json.dumps(evaluation_history_questionnaire), content_type="application/json",
                           follow_redirects=True,
                           headers=self.logged_in_headers())
        self.assertEqual(400, rv.status_code,
                          "This endpoint should require that the flow exists and that the question is in the flow.")
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response)
        self.assertEqual("not_in_the_flow", response["code"],
                          "There should be a clear error message explaining what went wrong.")

    def test_questionnare_post_fails_if_not_logged_in(self):
        cq = {'first_name': "Darah", 'marketing_channel': "Subway sign"}
        rv = self.app.post('api/flow/intake/contact_questionnaire', data=json.dumps(cq), content_type="application/json",
                           follow_redirects=True)
        self.assertEqual(401, rv.status_code)
        pass

    def test_questionnaire_post_fails_if_user_not_connected_to_participant(self):
        cq = {'first_name': "Darah", 'marketing_channel': "Subway sign"}
        rv = self.app.post('api/flow/intake/contact_questionnaire', data=json.dumps(cq), content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers())
        self.assertEqual(400, rv.status_code,
                          "This endpoint should require a participant id that is associated with current user.")
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response)
        self.assertEqual("Unable to save the provided object.", response["message"],
                          "There should be a clear error message explaining what went wrong.")


    def test_questionnionare_post_creates_log_record(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship="self")
        headers = self.logged_in_headers(u)

        cq = {'first_name': "Darah", 'marketing_channel': "Subway sign", 'participant_id': p.id}
        rv = self.app.post('api/flow/intake/contact_questionnaire', data=json.dumps(cq), content_type="application/json",
                           follow_redirects=True, headers=headers)
        self.assertSuccess(rv)
        log = db.session.query(ProgressLog).all()
        self.assertIsNotNone(log)
        self.assertTrue(len(log) > 0)

    def test_flow_endpoint(self):
        # It should be possible to get a list of available flows
        rv = self.app.get('api/flow', content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(200, rv.status_code)
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)

    def test_intake_flow_with_user(self):
        self.construct_contact_questionnaire()
        rv = self.app.get('api/flow/intake', content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(200, rv.status_code)
        response = json.loads(rv.get_data(as_text=True))
        self.assertIsNotNone(response)
        self.assertEqual('intake', response['name'])
        self.assertIsNotNone(response['steps'])
        self.assertTrue(len(response['steps']) > 0)
        self.assertEqual('contact_questionnaire', response['steps'][0]['name'])
        self.assertEqual(QuestionService.TYPE_IDENTIFYING, response['steps'][0]['type'])
        self.assertEqual('unknown', response['steps'][0]['status'])
    # { "name": "Intake Process",
    #   "estimate_minutes": "20",
    #   "steps": [
    #       {
    #         "name": "contact",
    #         "type": "identifying",
    #         "status": "complete"
    #         "date_completed": 2009-12-11h11:12:15
    #       },
