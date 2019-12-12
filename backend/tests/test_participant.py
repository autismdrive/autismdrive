import unittest

from flask import json

from app.model.participant import Relationship, Participant
from tests.base_test_questionnaire import BaseTestQuestionnaire
from app import db


class TestParticipant(BaseTestQuestionnaire, unittest.TestCase):

    def test_participant_relationships(self):
        u = self.construct_user()
        participant = self.construct_participant(user=u, relationship=Relationship.self_participant)
        guardian = self.construct_participant(user=u, relationship=Relationship.self_guardian)
        dependent = self.construct_participant(user=u, relationship=Relationship.dependent)
        professional = self.construct_participant(user=u, relationship=Relationship.self_professional)
        rv = self.app.get('/api/user/%i' % u.id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], u.id)
        self.assertEqual(len(response["participants"]), 4)
        self.assertEqual(response["participants"][0]["id"], participant.id)
        self.assertEqual(response["participants"][0]["relationship"], 'self_participant')
        self.assertEqual(response["participants"][1]["id"], guardian.id)
        self.assertEqual(response["participants"][1]["relationship"], 'self_guardian')
        self.assertEqual(response["participants"][2]["id"], dependent.id)
        self.assertEqual(response["participants"][2]["relationship"], 'dependent')
        self.assertEqual(response["participants"][3]["id"], professional.id)
        self.assertEqual(response["participants"][3]["relationship"], 'self_professional')

    def test_participant_basics(self):
        self.construct_participant(user=self.construct_user(), relationship=Relationship.dependent)
        p = db.session.query(Participant).first()
        self.assertIsNotNone(p)
        p_id = p.id
        rv = self.app.get('/api/participant/%i' % p_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], p_id)
        self.assertEqual(response["relationship"], p.relationship.name)

    def test_modify_participant_you_do_not_own(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        good_headers = self.logged_in_headers(u)

        p = db.session.query(Participant).first()
        odd_user = self.construct_user(email='frankie@badfella.rf')
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
        p = self.construct_participant(user=u, relationship=Relationship.self_guardian)
        headers = self.logged_in_headers(u)
        participant = {'id': 567}
        rv = self.app.put('/api/participant/%i' % p.id, data=json.dumps(participant), content_type="application/json",
                          follow_redirects=True, headers=headers)
        self.assert_success(rv)
        p = db.session.query(Participant).filter_by(id=p.id).first()
        self.assertEqual(567, p.id)

    def test_modify_participant_basics_admin(self):
        self.construct_participant(user=self.construct_user(), relationship=Relationship.dependent)
        user2 = self.construct_user(email="theotherguy@stuff.com")
        logged_in_headers = self.logged_in_headers()
        p = db.session.query(Participant).first()
        self.assertIsNotNone(p)
        p_id = p.id
        rv = self.app.get('/api/participant/%i' % p_id, content_type="application/json",
                          headers=logged_in_headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        response['user_id'] = user2.id
        orig_date = response['last_updated']
        rv = self.app.put('/api/participant/%i' % p_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=logged_in_headers)
        self.assert_success(rv)
        rv = self.app.get('/api/participant/%i' % p_id, content_type="application/json",
                          headers=logged_in_headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['user_id'], user2.id)
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_participant(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.dependent)
        p_id = p.id
        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/participant/%i' % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.app.delete('api/participant/%i' % p_id, content_type="application/json",
                             headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.app.get('api/participant/%i' % p_id, content_type="application/json",
                          headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_participant(self):
        p = {'id': 7, 'relationship': 'self_participant'}
        rv = self.app.post('/api/session/participant', data=json.dumps(p), content_type="application/json",
                           follow_redirects=True)
        self.assertEqual(401, rv.status_code, "you can't create a participant without an account.")

        rv = self.app.post(
            '/api/session/participant', data=json.dumps(p),
            content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        participant = db.session.query(Participant).filter_by(id=p['id']).first()

        self.assertIsNotNone(participant.id)
        self.assertIsNotNone(participant.user_id)

    def test_create_participant_to_have_bad_relationship(self):
        participant = {'id': 234, 'relationship': 'free_loader'}
        rv = self.app.post('/api/session/participant', data=json.dumps(participant),
                           content_type="application/json", follow_redirects=True, headers=self.logged_in_headers())
        self.assertEqual(400, rv.status_code, "you can't create a participant using an invalid relationship")
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["code"], "unknown_relationship")

    def test_get_participant_by_user(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        db.session.commit()
        rv = self.app.get(
            '/api/user/%i' % u.id,
            content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(u.id, response['id'])
        self.assertEqual(1, len(response['participants']))
        self.assertEqual(p.relationship.name, response['participants'][0]["relationship"])

    def test_participant_ids_are_not_sequential(self):
        u = self.construct_user()
        p1 = self.construct_participant(user=u, relationship=Relationship.self_participant)
        p2 = self.construct_participant(user=u, relationship=Relationship.dependent)
        p3 = self.construct_participant(user=u, relationship=Relationship.dependent)

        self.assertNotEqual(p1.id + 1, p2.id)
        self.assertNotEqual(p2.id + 1, p3.id)

    def test_user_participant_list(self):
        u1 = self.construct_user(email='test1@sartography.com')
        u2 = self.construct_user(email='test2@sartography.com')
        self.construct_participant(user=u1, relationship=Relationship.self_participant)
        self.construct_participant(user=u2, relationship=Relationship.self_participant)
        self.construct_participant(user=u1, relationship=Relationship.self_guardian)
        self.construct_participant(user=u1, relationship=Relationship.dependent)
        self.construct_participant(user=u2, relationship=Relationship.self_professional)
        rv = self.app.get(
            '/api/user_participant',
            content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(2, response['num_self_participants'])
        self.assertEqual(1, response['num_self_guardians'])
        self.assertIsNotNone(response['user_participants'])
        self.assertIsNotNone(response['num_dependents'])
        self.assertIsNotNone(response['num_self_professionals'])
        self.assertIsNotNone(response['all_participants'])

    def test_participant_percent_complete(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)

        rv = self.app.get(
            '/api/participant',
            content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, response[0]['percent_complete'])

        iq = {
            'first_name': "Darah",
            'middle_name': "Soo",
            'last_name': "Ubway",
            'is_first_name_preferred': True,
            'birthdate': '02/02/2002',
            'birth_city': 'Staunton',
            'birth_state': 'VA',
            'is_english_primary': True,
            'participant_id': p.id
        }
        self.app.post('api/flow/self_intake/identification_questionnaire', data=json.dumps(iq),
                           content_type="application/json",
                           follow_redirects=True, headers=self.logged_in_headers(u))

        rv = self.app.get(
            '/api/participant',
            content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertGreater(response[0]['percent_complete'], 0)

    def test_participant_name(self):
        p = self.construct_participant(user=self.construct_user(), relationship=Relationship.self_participant)
        rv = self.app.get(
            '/api/participant',
            content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response[0]['name'], '')

        self.construct_identification_questionnaire(first_name='Felicity', nickname="City", participant=p)
        rv = self.app.get(
            '/api/participant',
            content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response[0]['name'], 'City')
