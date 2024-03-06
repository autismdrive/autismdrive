import datetime
import random

from flask import json
from sqlalchemy import cast, Integer, select
from sqlalchemy.orm import joinedload

from app.email_service import EmailService
from app.enums import Relationship, Permission, Role, StudyUserStatus
from app.models import EmailLog, User, UserFavorite
from app.models import StudyUser
from app.rest_exception import RestException
from fixtures.fixure_utils import fake
from tests.base_test import BaseTest


class TestUser(BaseTest):
    def _verify_email(self, user: User):
        user.email_verified = True
        self.session.add(user)
        self.session.commit()
        self.session.close()

    def test_user_basics(self):
        u_email = fake.email()
        self.construct_user(email=u_email)
        u = self.session.query(User).first()
        self.assertIsNotNone(u)
        u_id = u.id
        headers = self.logged_in_headers(u.id)
        rv = self.client.get(
            "/api/user/%i" % u_id, follow_redirects=True, content_type="application/json", headers=headers
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], u_id)
        self.assertEqual(response["email"], u_email)

    def test_modify_user_basics(self):
        old_email = fake.email()
        self.construct_user(email=old_email)
        u = (
            self.session.execute(select(User).options(joinedload(User.participants)).filter(User.email == old_email))
            .unique()
            .scalar_one_or_none()
        )
        self.assertIsNotNone(u)
        u_id = u.id
        admin_headers = self.logged_in_headers()
        user_headers = self.logged_in_headers(u.id)
        self.session.close()

        # A user should be able to access and modify their user record, with the exception of making themselves Admin
        rv = self.client.get("/api/user/%i" % u_id, content_type="application/json", headers=user_headers)
        self.assert_success(rv)
        response = rv.json
        new_email = fake.email()
        response["email"] = new_email
        orig_date = response["last_updated"]
        rv = self.client.put(
            "/api/user/%i" % u_id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=user_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(new_email, response["email"])

        # Only Admin users can make other admin users
        response["role"] = "admin"
        rv = self.client.put(
            "/api/user/%i" % u_id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=admin_headers,
        )
        self.assert_success(rv)

        rv = self.client.get("/api/user/%i" % u_id, content_type="application/json", headers=user_headers)
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(new_email, response["email"])
        self.assertEqual(response["role"], "admin")
        self.assertNotEqual(orig_date, response["last_updated"])

    def test_delete_user(self):
        u = self.construct_user()
        u_id = u.id

        rv = self.client.get("api/user/%i" % u_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.get("api/user/%i" % u_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.client.delete("api/user/%i" % u_id, content_type="application/json", headers=None)
        self.assertEqual(401, rv.status_code)
        rv = self.client.delete("api/user/%i" % u_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.client.get("api/user/%i" % u_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.get("api/user/%i" % u_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_user(self):
        user = {"email": "tara@spiders.org"}
        rv = self.client.post(
            "api/user",
            data=self.jsonify(user),
            content_type="application/json",
            headers=self.logged_in_headers(),
            follow_redirects=True,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["email"], "tara@spiders.org")
        self.assertIsNotNone(response["id"])

    def test_create_user_with_bad_role(self):
        user = {"email": "tara@spiders.org", "role": "web_weaver"}

        # post should change unknown role to 'user'
        rv = self.client.post(
            "/api/user",
            data=self.jsonify(user),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["role"], "user")

    def test_non_admin_cannot_create_admin_user(self):
        u = self.construct_user()
        u_id = u.id
        u_email = u.email
        non_admin_headers = self.logged_in_headers(user_id=u.id)
        admin_headers = self.logged_in_headers()

        # post should make role 'user'
        new_admin_user = {"email": "tara@spiders.org", "role": "admin"}
        rv = self.client.post(
            "/api/user",
            data=self.jsonify(new_admin_user),
            content_type="application/json",
            follow_redirects=True,
            headers=non_admin_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["role"], "user")
        new_id = response["id"]

        # If non-admin user tries to change their own role, the system should keep role as 'user'
        rv = self.client.put(
            "/api/user/%i" % u_id,
            data=self.jsonify({"email": u_email, "role": "admin"}),
            content_type="application/json",
            follow_redirects=True,
            headers=non_admin_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["role"], "user")

        # If admin user changes the role, the system should allow them to make role 'admin'
        rv = self.client.put(
            "/api/user/%i" % new_id,
            data=self.jsonify(new_admin_user),
            content_type="application/json",
            follow_redirects=True,
            headers=admin_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["role"], "admin")

    def test_create_user_with_bad_password(self, id=8, email="tyrion@got.com", role=Role.user):
        data = {"id": id, "email": email}
        rv = self.client.post(
            "/api/user",
            data=self.jsonify(data),
            follow_redirects=True,
            headers=self.logged_in_headers(),
            content_type="application/json",
        )
        self.assert_success(rv)
        user = self.session.query(User).filter_by(id=cast(id, Integer)).first()
        user.role = role

        with self.assertRaises(RestException):
            # Should raise exception
            user.password = "badpass"

    def test_create_user_with_password(
        self, user_id: int = None, email: str = None, role: Role = None, password: str = None
    ) -> User:
        role = role or Role.user
        password = password or fake.password(length=32)
        user_id = user_id or random.randint(10000, 99999)
        email = email or fake.email()
        data = {"id": user_id, "email": email}
        admin_headers = self.logged_in_headers()

        rv = self.client.post(
            "/api/user",
            data=self.jsonify(data),
            follow_redirects=True,
            headers=admin_headers,
            content_type="application/json",
        )
        self.assert_success(rv)

        user_to_update = (
            self.session.execute(select(User).options(joinedload(User.participants)).filter_by(id=user_id))
            .unique()
            .scalar_one()
        )

        self.assertIsNotNone(user_to_update)
        self.assertIsNotNone(user_to_update.token_url)

        user_to_update.role = role
        user_to_update.password = password

        self.session.add(user_to_update)
        self.session.commit()
        self.session.close()

        rv = self.client.get(f"/api/user/{user_id}", content_type="application/json", headers=admin_headers)
        self.assert_success(rv)
        response = rv.json

        db_user = (
            self.session.execute(select(User).options(joinedload(User.participants)).filter_by(id=user_id))
            .unique()
            .scalar_one()
        )

        self.assertEqual(email, response["email"])
        self.assertEqual(role.name, response["role"])
        self.assertTrue(User.is_correct_password(user_id=user_id, plaintext=password))
        self.session.close()

        return db_user

    def test_login_user(self):
        user_email = fake.email()
        user_password = fake.password(length=32)
        user_id = random.randint(10000, 99999)
        user = self.test_create_user_with_password(user_id=user_id, email=user_email, password=user_password)
        data = {"email": user_email, "password": user_password}

        # Login shouldn't work with email not yet verified
        rv = self.client.post("/api/login_password", data=self.jsonify(data), content_type="application/json")
        self.assertEqual(400, rv.status_code)

        # Set email_verified to True so login will work
        self._verify_email(user)

        rv = self.client.post("/api/login_password", data=self.jsonify(data), content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertIsNotNone(response["token"])

        return user

    def test_get_current_user(self):
        """Test for the current user status"""
        user = self.test_login_user()

        # Now get the user back.
        response = self.client.get(
            "/api/session", headers=dict(Authorization=f"Bearer {User.encode_auth_token(user_id=user.id)}")
        )
        self.assert_success(response)
        return json.loads(response.data.decode())

    def test_register_sends_email(self):
        message_count = len(EmailService.TEST_MESSAGES)
        self.test_create_user_with_password()
        self.assertGreater(len(EmailService.TEST_MESSAGES), message_count)
        self.assertEqual("Autism DRIVE: Confirm Email", self.decode(EmailService.TEST_MESSAGES[-1]["subject"]))

        logs = self.session.query(EmailLog).all()
        self.assertIsNotNone(logs[-1].tracking_code)

    def test_forgot_password_sends_email(self):
        user = self.test_create_user_with_password(user_id=10101, email="forgot_password_sends_email@test.com")
        message_count = len(EmailService.TEST_MESSAGES)
        data = {"email": user.email}
        rv = self.client.post("/api/forgot_password", data=self.jsonify(data), content_type="application/json")
        self.assert_success(rv)
        self.assertGreater(len(EmailService.TEST_MESSAGES), message_count)
        self.assertEqual("Autism DRIVE: Password Reset Email", self.decode(EmailService.TEST_MESSAGES[-1]["subject"]))

        logs = self.session.query(EmailLog).all()
        self.assertIsNotNone(logs[-1].tracking_code)

    def test_enrolled_vs_inquiry_studies_by_user(self):
        u = self.construct_user(email="u1@sartography.com")
        s1 = self.construct_study(title="Super Study")
        s2 = self.construct_study(title="Amazing Study")
        s3 = self.construct_study(title="Phenomenal Study")
        su1 = StudyUser(study=s1, user=u, status=StudyUserStatus.inquiry_sent)
        su2 = StudyUser(study=s3, user=u, status=StudyUserStatus.inquiry_sent)
        su3 = StudyUser(study=s2, user=u, status=StudyUserStatus.enrolled)
        self.session.add_all([su1, su2, su3])
        self.session.commit()

        rv = self.client.get(
            "/api/user/%i/inquiry/study" % u.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(2, len(response))
        self.assertNotEqual(s2.id, response[0]["study_id"])
        self.assertNotEqual(s2.id, response[1]["study_id"])
        rv = self.client.get(
            "/api/user/%i/enrolled/study" % u.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(s2.id, response[0]["study_id"])

    def test_get_user_by_study(self):
        u = self.construct_user()
        s = self.construct_study()
        su = StudyUser(study=s, user=u, status=StudyUserStatus.inquiry_sent)
        self.session.add(su)
        self.session.commit()
        rv = self.client.get(
            "/api/study/%i/user" % s.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(su.id, response[0]["id"])
        self.assertEqual(u.id, response[0]["user"]["id"])
        self.assertEqual(u.email, response[0]["user"]["email"])

    def test_add_user_to_study(self):
        u = self.construct_user()
        s = self.construct_study()

        us_data = {"study_id": s.id, "user_id": u.id}

        rv = self.client.post(
            "/api/study_user",
            data=self.jsonify(us_data),
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(u.id, response["user_id"])
        self.assertEqual(s.id, response["study_id"])

    def test_set_all_users_on_study(self):
        u1 = self.construct_user()
        u2 = self.construct_user()
        u3 = self.construct_user()
        s = self.construct_study()

        us_data = [
            {"user_id": u1.id},
            {"user_id": u2.id},
            {"user_id": u3.id},
        ]
        rv = self.client.post(
            "/api/study/%i/user" % s.id,
            data=self.jsonify(us_data),
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(3, len(response))

        us_data = [{"user_id": u1.id}]
        rv = self.client.post(
            "/api/study/%i/user" % s.id,
            data=self.jsonify(us_data),
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))

    def test_remove_user_from_study(self):
        self.test_add_user_to_study()
        rv = self.client.delete("/api/study_user/%i" % 1, headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.client.get(
            "/api/study/%i/user" % 1, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(0, len(response))

    def test_user_ids_are_not_sequential(self):
        u1 = self.construct_user(email="hopper@strangerthings.org")
        u2 = self.construct_user(email="eleven@strangerthings.org")
        u3 = self.construct_user(email="murray@strangerthings.org")

        self.assertNotEqual(u1.id + 1, u2.id)
        self.assertNotEqual(u2.id + 1, u3.id)

    def test_get_user_permissions(self):
        admin = self.construct_user(role=Role.admin, email="admin@sartography.com")
        test = self.construct_user(role=Role.test, email="test@sartography.com")
        researcher = self.construct_user(role=Role.researcher, email="researcher@sartography.com")
        editor = self.construct_user(role=Role.editor, email="editor@sartography.com")
        user = self.construct_user(role=Role.user, email="user@sartography.com")

        self.assertEqual(admin.role.permissions(), list(Permission))
        self.assertEqual(
            researcher.role.permissions(),
            [
                Permission.user_detail_admin,
            ],
        )
        self.assertEqual(
            editor.role.permissions(),
            [Permission.create_resource, Permission.edit_resource, Permission.delete_resource],
        )
        self.assertEqual(user.role.permissions(), [])

        self.assertTrue(Permission.user_roles in admin.role.permissions())
        self.assertFalse(Permission.user_roles in test.role.permissions())
        self.assertFalse(Permission.delete_user in test.role.permissions())
        self.assertTrue(Permission.user_detail_admin in researcher.role.permissions())
        self.assertTrue(Permission.create_resource in editor.role.permissions())
        self.assertTrue(Permission.user_roles not in user.role.permissions())
        self.assertTrue(Permission.user_roles not in editor.role.permissions())
        self.assertTrue(Permission.user_roles not in researcher.role.permissions())

    def test_login_tracks_login_date(self):
        user_email = fake.email()
        user_password = fake.password(length=32)
        user_id = random.randint(10000, 99999)
        time_before_create = datetime.datetime.utcnow()
        user = self.test_create_user_with_password(user_id=user_id, email=user_email, password=user_password)
        last_login = user.last_login
        self.assertAlmostEqual(time_before_create, last_login, delta=datetime.timedelta(seconds=10))
        data = {"email": user_email, "password": user_password}

        # Set email_verified to True so login will work
        user.email_verified = True
        self.session.add(user)
        self.session.commit()
        self.session.close()

        rv1 = self.client.post("/api/login_password", data=self.jsonify(data), content_type="application/json")
        self.assert_success(rv1)
        response_1 = rv1.json
        self.assertIsNotNone(response_1["last_login"])
        time_after_1st_login = response_1["last_login"]

        rv2 = self.client.post("/api/login_password", data=self.jsonify(data), content_type="application/json")
        self.assert_success(rv2)
        response_2 = rv2.json
        self.assertIsNotNone(response_2["last_login"])
        time_after_2nd_login = response_2["last_login"]
        self.assertGreater(time_after_2nd_login, time_after_1st_login)

    def test_get_favorites_by_user(self):
        u = self.construct_user()
        r = self.construct_resource()
        c = self.construct_category()
        fav1 = UserFavorite(resource_id=r.id, user=u, type="resource")
        fav2 = UserFavorite(category_id=c.id, user=u, type="category")
        self.session.add_all([fav1, fav2])
        self.session.commit()
        rv = self.client.get(
            "/api/user/%i/favorite" % u.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(2, len(response))
        self.assertEqual(r.id, response[0]["resource_id"])
        self.assertEqual("resource", response[0]["type"])
        self.assertEqual(c.id, response[1]["category_id"])
        self.assertEqual("category", response[1]["type"])

    def test_user_favorite_types(self):
        u = self.construct_user(email="u1@sartography.com")
        r = self.construct_resource()
        c = self.construct_category(name="cat1")
        c2 = self.construct_category(name="cat2")
        fav1 = UserFavorite(resource_id=r.id, user=u, type="resource")
        fav2 = UserFavorite(category_id=c.id, user=u, type="category")
        fav3 = UserFavorite(category_id=c2.id, user=u, type="category")
        fav4 = UserFavorite(age_range="adult", user=u, type="age_range")
        fav5 = UserFavorite(age_range="aging", user=u, type="age_range")
        fav6 = UserFavorite(age_range="transition", user=u, type="age_range")
        fav7 = UserFavorite(language="arabic", user=u, type="language")
        fav8 = UserFavorite(covid19_category="edu-tainment", user=u, type="covid19_category")
        self.session.add_all([fav1, fav2, fav3, fav4, fav5, fav6, fav7, fav8])
        self.session.commit()
        rv = self.client.get(
            "/api/user/%i/favorite" % u.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(8, len(response))
        rv = self.client.get(
            "/api/user/%i/favorite/resource" % u.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(fav1.id, response[0]["id"])
        rv = self.client.get(
            "/api/user/%i/favorite/category" % u.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(2, len(response))
        self.assertEqual(fav2.id, response[0]["id"])
        rv = self.client.get(
            "/api/user/%i/favorite/age_range" % u.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(3, len(response))
        self.assertEqual(fav4.id, response[0]["id"])
        rv = self.client.get(
            "/api/user/%i/favorite/language" % u.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(fav7.id, response[0]["id"])
        rv = self.client.get(
            "/api/user/%i/favorite/covid19_category" % u.id,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(fav8.id, response[0]["id"])

    def test_add_favorite_to_user(self):
        u = self.construct_user()
        r = self.construct_resource()

        fav_data = [{"resource_id": r.id, "user_id": u.id, "type": "resource"}]

        rv = self.client.post(
            "/api/user_favorite",
            data=self.jsonify(fav_data),
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(u.id, response[0]["user_id"])
        self.assertEqual(r.id, response[0]["resource_id"])

    def test_remove_favorite_from_user(self):
        self.test_add_favorite_to_user()
        rv = self.client.delete("/api/user_favorite/%i" % 1, headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.client.get(
            "/api/user/%i/favorite" % 1, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(0, len(response))

    def test_delete_user_deletes_favorites(self):
        u = self.construct_user()
        r = self.construct_resource()

        fav_data = [
            {"resource_id": r.id, "user_id": u.id, "type": "resource"},
            {"age_range": "adult", "user_id": u.id, "type": "age_range"},
        ]

        rv = self.client.post(
            "/api/user_favorite",
            data=self.jsonify(fav_data),
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(2, len(response))
        self.assertEqual(u.id, response[0]["user_id"])

        rv = self.client.delete("api/user/%i" % u.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.client.get("/api/user_favorite", content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(0, len(response))

    def test_user_participant_count(self):
        u1 = self.construct_user(email="1@sartography.com")
        u2 = self.construct_user(email="2@sartography.com")
        u3 = self.construct_user(email="3@sartography.com")
        self.construct_participant(user_id=u1.id, relationship=Relationship.self_guardian)
        self.construct_participant(user_id=u1.id, relationship=Relationship.dependent)
        self.construct_participant(user_id=u2.id, relationship=Relationship.self_participant)

        rv = self.client.get("api/user/%i" % u1.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(2, response["participant_count"])

        rv = self.client.get("api/user/%i" % u2.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, response["participant_count"])

        rv = self.client.get("api/user/%i" % u3.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(0, response["participant_count"])

    def test_user_created_password(self):
        pass_user = self.test_create_user_with_password()
        self.assertEqual(pass_user.created_password(), True)
        non_pass_user = self.construct_user()
        self.assertEqual(non_pass_user.created_password(), False)

    def test_user_identity(self):
        u = self.construct_user(email="superuser@sartography.com")
        self.construct_participant(user_id=u.id, relationship=Relationship.self_guardian)
        self.assertEqual(u.identity(), "self_guardian")
        u2 = self.construct_user(email="superuser2@sartography.com")
        self.construct_participant(user_id=u2.id, relationship=Relationship.self_professional)
        self.assertEqual(u2.identity(), "self_professional")

    def test_percent_self_registration_complete(self):
        u = self.construct_user(email="prof@sartography.com")
        p = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant)
        iq = self.get_identification_questionnaire(p.id)
        self.client.post(
            "api/flow/self_intake/identification_questionnaire",
            data=self.jsonify(iq),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(u.id),
        )

        self.assertGreater(u.percent_self_registration_complete(), 0)

    def test_user_participant_count_new_enum(self):
        u1 = self.construct_user(email="1@sartography.com")
        u4 = self.construct_user(email="4@sartography.com")
        self.construct_participant(user_id=u1.id, relationship=Relationship.self_guardian)
        self.construct_participant(user_id=u4.id, relationship=Relationship.self_interested)

        rv = self.client.get("api/user/%i" % u1.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, response["participant_count"])

        rv = self.client.get("api/user/%i" % u4.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, response["participant_count"])
