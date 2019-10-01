import base64
import quopri
import re
import unittest

from flask import json

from tests.base_test import BaseTest
from app import db
from app.email_service import TEST_MESSAGES
from app.model.email_log import EmailLog
from app.model.study_user import StudyUser, StudyUserStatus
from app.model.user import User, Role


class TestUser(BaseTest, unittest.TestCase):

    def test_user_basics(self):
        self.construct_user()
        u = db.session.query(User).first()
        self.assertIsNotNone(u)
        u_id = u.id
        headers = self.logged_in_headers(u)
        rv = self.app.get('/api/user/%i' % u_id,
                          follow_redirects=True,
                          content_type="application/json", headers=headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], u_id)
        self.assertEqual(response["email"], 'stan@staunton.com')

    def test_modify_user_basics(self):
        self.construct_user()
        u = db.session.query(User).first()
        admin_headers = self.logged_in_headers()
        user_headers = self.logged_in_headers(u)
        self.assertIsNotNone(u)

        # A user should be able to access and modify their user record, with the exception of making themselves Admin
        rv = self.app.get('/api/user/%i' % u.id, content_type="application/json", headers=user_headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        response['email'] = 'ed@edwardos.com'
        orig_date = response['last_updated']
        rv = self.app.put('/api/user/%i' % u.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=user_headers)
        self.assert_success(rv)

        # Only Admin users can make other admin users
        response['role'] = 'admin'
        rv = self.app.put('/api/user/%i' % u.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=admin_headers)
        self.assert_success(rv)

        rv = self.app.get('/api/user/%i' % u.id, content_type="application/json", headers=user_headers)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['email'], 'ed@edwardos.com')
        self.assertEqual(response['role'], 'admin')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_user(self):
        u = self.construct_user()
        u_id = u.id

        rv = self.app.get('api/user/%i' % u_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.app.get('api/user/%i' % u_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/user/%i' % u_id, content_type="application/json", headers=None)
        self.assertEqual(401, rv.status_code)
        rv = self.app.delete('api/user/%i' % u_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/user/%i' % u_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.app.get('api/user/%i' % u_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_user(self):
        user = {'email': "tara@spiders.org"}
        rv = self.app.post('api/user', data=json.dumps(user), content_type="application/json",
                           headers=self.logged_in_headers(), follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['email'], 'tara@spiders.org')
        self.assertIsNotNone(response['id'])

    def test_create_user_with_bad_role(self):
        user = {'email': "tara@spiders.org", 'role': 'web_weaver'}

        # post should change unknown role to 'user'
        rv = self.app.post('/api/user', data=json.dumps(user),
                           content_type="application/json", follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['role'], 'user')

    def test_non_admin_cannot_create_admin_user(self):
        u = self.construct_user()

        # post should make role 'user'
        new_admin_user = {'email': "tara@spiders.org", 'role': 'admin'}
        rv = self.app.post('/api/user', data=json.dumps(new_admin_user),
                           content_type="application/json", follow_redirects=True, headers=self.logged_in_headers(user=u))
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['role'], 'user')
        new_id = response['id']

        # put as non-admin user should keep role as 'user'
        rv = self.app.put('/api/user/%i' % u.id, data=json.dumps({'email': u.email, 'role': 'admin'}),
                           content_type="application/json", follow_redirects=True, headers=self.logged_in_headers(user=u))
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['role'], 'user')

        # put as admin user should allow to make role 'admin'
        rv = self.app.put('/api/user/%i' % new_id, data=json.dumps(new_admin_user),
                           content_type="application/json", follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['role'], 'admin')

    def test_create_user_with_password(self, id=8, email="tyrion@got.com", role=Role.user, password="peterpass"):
        data = {
            "id": id,
            "email": email
        }
        rv = self.app.post(
            '/api/user',
            data=json.dumps(data),
            follow_redirects=True,
            headers=self.logged_in_headers(),
            content_type="application/json")
        self.assert_success(rv)
        user = User.query.filter_by(id=id).first()
        user.password = password
        user.role = role
        db.session.add(user)
        db.session.commit()

        rv = self.app.get(
            '/api/user/%i' % user.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(email, response["email"])
        self.assertEqual(role.name, response["role"])
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
        self.assert_success(rv)
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
        self.assert_success(response)
        return json.loads(response.data.decode())

    def test_register_sends_email(self):
        message_count = len(TEST_MESSAGES)
        self.test_create_user_with_password()
        self.assertGreater(len(TEST_MESSAGES), message_count)
        self.assertEqual("Autism DRIVE: Confirm Email",
                         self.decode(TEST_MESSAGES[-1]['subject']))

        logs = EmailLog.query.all()
        self.assertIsNotNone(logs[-1].tracking_code)

    def test_forgot_password_sends_email(self):
        user = self.test_create_user_with_password(id=10101, email="forgot_password_sends_email@test.com")
        message_count = len(TEST_MESSAGES)
        data = {"email": user.email}
        rv = self.app.post(
            '/api/forgot_password',
            data=json.dumps(data),
            content_type="application/json")
        self.assert_success(rv)
        self.assertGreater(len(TEST_MESSAGES), message_count)
        self.assertEqual("Autism DRIVE: Password Reset Email",
                         self.decode(TEST_MESSAGES[-1]['subject']))

        logs = EmailLog.query.all()
        self.assertIsNotNone(logs[-1].tracking_code)

    def test_get_study_by_user(self):
        u = self.construct_user()
        s = self.construct_study()
        su = StudyUser(study=s, user=u, status=StudyUserStatus.inquiry_sent)
        db.session.add(su)
        db.session.commit()
        rv = self.app.get(
            '/api/user/%i/study' % u.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(s.id, response[0]["study_id"])
        self.assertEqual(s.description, response[0]["study"]["description"])

    def test_get_study_by_user_includes_user_details(self):
        u = self.construct_user(email="c1")
        u2 = self.construct_user(email="c2")
        s = self.construct_study()
        su = StudyUser(study=s, user=u, status=StudyUserStatus.inquiry_sent)
        su2 = StudyUser(study=s, user=u2, status=StudyUserStatus.enrolled)
        db.session.add_all([su, su2])
        db.session.commit()
        rv = self.app.get(
            '/api/user/%i/study' % u.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(s.id, response[0]["study_id"])
        self.assertEqual(2,
                         len(response[0]["study"]["study_users"]))
        self.assertEqual(
            "c1", response[0]["study"]["study_users"][0]["user"]
            ["email"])

    def test_enrolled_vs_inquiry_studies_by_user(self):
        u = self.construct_user(email="u1@sartography.com")
        s1 = self.construct_study(title="Super Study")
        s2 = self.construct_study(title="Amazing Study")
        s3 = self.construct_study(title="Phenomenal Study")
        su1 = StudyUser(study=s1, user=u, status=StudyUserStatus.inquiry_sent)
        su2 = StudyUser(study=s3, user=u, status=StudyUserStatus.inquiry_sent)
        su3 = StudyUser(study=s2, user=u, status=StudyUserStatus.enrolled)
        db.session.add_all([su1, su2, su3])
        db.session.commit()
        rv = self.app.get(
            '/api/user/%i/study' % u.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))
        rv = self.app.get(
            '/api/user/%i/inquiry/study' % u.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(2, len(response))
        self.assertNotEqual(s2.id, response[0]["study_id"])
        self.assertNotEqual(s2.id, response[1]["study_id"])
        rv = self.app.get(
            '/api/user/%i/enrolled/study' % u.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(s2.id, response[0]["study_id"])

    def test_get_user_by_study(self):
        u = self.construct_user()
        s = self.construct_study()
        su = StudyUser(study=s, user=u, status=StudyUserStatus.inquiry_sent)
        db.session.add(su)
        db.session.commit()
        rv = self.app.get(
            '/api/study/%i/user' % s.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(su.id, response[0]["id"])
        self.assertEqual(u.id, response[0]["user"]["id"])
        self.assertEqual(u.email, response[0]["user"]["email"])

    def test_add_user_to_study(self):
        u = self.construct_user()
        s = self.construct_study()

        us_data = {"study_id": s.id, "user_id": u.id}

        rv = self.app.post(
            '/api/study_user',
            data=json.dumps(us_data),
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(u.id, response["user_id"])
        self.assertEqual(s.id, response["study_id"])

    def test_set_all_users_on_study(self):
        u1 = self.construct_user(email="u1@sartography.com")
        u2 = self.construct_user(email="u2@sartography.com")
        u3 = self.construct_user(email="u3@sartography.com")
        s = self.construct_study()

        us_data = [
            {
                "user_id": u1.id
            },
            {
                "user_id": u2.id
            },
            {
                "user_id": u3.id
            },
        ]
        rv = self.app.post(
            '/api/study/%i/user' % s.id,
            data=json.dumps(us_data),
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        us_data = [{"user_id": u1.id}]
        rv = self.app.post(
            '/api/study/%i/user' % s.id,
            data=json.dumps(us_data),
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_user_from_study(self):
        self.test_add_user_to_study()
        rv = self.app.delete('/api/study_user/%i' % 1,
                             headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get(
            '/api/study/%i/user' % 1,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_user_ids_are_not_sequential(self):
        u1 = self.construct_user(email="hopper@strangerthings.org")
        u2 = self.construct_user(email="eleven@strangerthings.org")
        u3 = self.construct_user(email="murray@strangerthings.org")

        self.assertNotEqual(u1.id + 1, u2.id)
        self.assertNotEqual(u2.id + 1, u3.id)
