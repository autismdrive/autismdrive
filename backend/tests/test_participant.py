import datetime
from http import HTTPStatus

from tests.base_test_questionnaire import BaseTestQuestionnaire  # isort:skip
from flask import json

from app.enums import Relationship
from app.models import Participant, UserMeta
from app.schemas import SchemaRegistry
from tests.fixtures.fixture_utils import fake


class TestParticipant(BaseTestQuestionnaire):
    def test_participant_relationships(self):
        u = self.default_user
        u_id = u.id
        headers = self.logged_in_headers(user_id=u_id)
        participant = self.construct_participant(user_id=u_id, relationship=Relationship.self_participant)
        guardian = self.construct_participant(user_id=u_id, relationship=Relationship.self_guardian)
        dependent = self.construct_participant(user_id=u_id, relationship=Relationship.dependent)
        professional = self.construct_participant(user_id=u_id, relationship=Relationship.self_professional)
        interested = self.construct_participant(user_id=u_id, relationship=Relationship.self_interested)
        rv = self.client.get(
            "/api/user/%i" % u_id,
            follow_redirects=True,
            content_type="application/json",
            headers=headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], u_id)
        self.assertEqual(len(response["participants"]), 5)
        for user_participant in response["participants"]:
            up_id = user_participant["id"]
            match user_participant["relationship"]:
                case "self_participant":
                    self.assertEqual(up_id, participant.id)
                case "self_guardian":
                    self.assertEqual(up_id, guardian.id)
                case "dependent":
                    self.assertEqual(up_id, dependent.id)
                case "self_professional":
                    self.assertEqual(up_id, professional.id)
                case "self_interested":
                    self.assertEqual(up_id, interested.id)

    def test_participant_basics(self):
        u = self.default_user
        self.construct_participant(user_id=u.id, relationship=Relationship.dependent)
        p = self.session.query(Participant).first()
        self.assertIsNotNone(p)
        p_id = p.id
        rv = self.client.get(
            "/api/participant/%i" % p_id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], p_id)
        self.assertEqual(response["relationship"], p.relationship.name)

    def test_modify_participant_you_do_not_own(self):
        u = self.construct_user(email=fake.email())
        p = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant)
        good_headers = self.logged_in_headers(u.id)

        db_p = self.session.query(Participant).filter(Participant.id == p.id).first()
        self.assertIsNotNone(db_p)

        # Unrecognized fields should be ignored.
        participant = {"bad_field_1": fake.bs(), "bad_field_2": fake.paragraph()}

        # Anonymous user should not be able to edit a participant.
        rv = self.client.put(
            "/api/participant/%i" % p.id,
            data=self.jsonify(participant),
            content_type="application/json",
            follow_redirects=True,
        )
        self.assertEqual(401, rv.status_code, "you have to be logged in to edit participant.")

        # An unrelated logged-in user should not be able to edit someone else's participant.
        bad_user = self.construct_user(email=fake.email())
        rv = self.client.put(
            "/api/participant/%i" % p.id,
            data=self.jsonify(participant),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(bad_user.id),
        )
        self.assertEqual(400, rv.status_code, "you have to have a relationship with the user to do stuff.")
        response = rv.json
        self.assertEqual("unrelated_participant", response["code"])

        # A logged-in user should be able to edit their own participant.
        rv = self.client.put(
            "/api/participant/%i" % p.id,
            data=self.jsonify(participant),
            content_type="application/json",
            follow_redirects=True,
            headers=good_headers,
        )
        self.assertEqual(200, rv.status_code, "The owner can edit the user.")

    def test_modify_participant_you_do_own(self):
        u = self.construct_user(email=fake.email())
        p = self.construct_participant(user_id=u.id, relationship=Relationship.self_guardian)
        participant_id = p.id
        headers = self.logged_in_headers(u.id)
        participant = {"id": participant_id}
        rv = self.client.put(
            "/api/participant/%i" % p.id,
            data=self.jsonify(participant),
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)
        db_p = self.session.query(Participant).filter_by(id=participant_id).first()
        self.assertEqual(participant_id, db_p.id)

    def test_modify_participant_basics_admin(self):
        # User 1
        user1 = self.construct_user(email=fake.email())
        u1_id = user1.id
        u1_headers = self.logged_in_headers(user_id=u1_id)

        # User 2
        user2 = self.construct_user(email=fake.email())
        u2_id = user2.id
        u2_headers = self.logged_in_headers(user_id=u2_id)

        # Participant is originally created by User 1
        self.construct_participant(user_id=u1_id, relationship=Relationship.dependent)
        p = self.session.query(Participant).filter(Participant.user_id == u1_id).first()
        self.assertIsNotNone(p)
        p_id = p.id
        rv1 = self.client.get(
            f"/api/participant/{p_id}",
            content_type="application/json",
            headers=u1_headers,  # Log in as User 1
        )
        self.assert_success(rv1)

        # User 2 should not be able to see the Participant
        rv_no_access1 = self.client.get(
            f"/api/participant/{p_id}",
            content_type="application/json",
            headers=u2_headers,  # Log in as User 2
        )
        self.assertEqual(400, rv_no_access1.status_code)
        resp_no_access1 = rv_no_access1.json
        self.assertEqual(resp_no_access1["code"], "unrelated_participant")

        # User 1 should NOT be able to change the user linked to their Participant
        rv1_dict = rv1.json
        rv1_dict["user_id"] = u2_id
        orig_date = rv1_dict["last_updated"]
        modified_json = self.jsonify(rv1_dict)
        rv_no_access2 = self.client.put(
            f"/api/participant/{p_id}",
            data=modified_json,
            content_type="application/json",
            follow_redirects=True,
            headers=u1_headers,  # Log in as User 1
        )
        self.assertEqual(HTTPStatus.FORBIDDEN, rv_no_access2.status_code)
        resp_no_access2 = rv_no_access2.json
        self.assertEqual(resp_no_access2["code"], "permission_denied")

        # Admin should be able to link a Participant to a different User
        rv2 = self.client.put(
            f"/api/participant/{p_id}",
            data=modified_json,
            content_type="application/json",
            follow_redirects=True,
            headers=self.default_admin_logged_in_headers,  # Log in as Admin
        )
        self.assert_success(rv2)
        rv2_dict = rv2.json
        self.assertEqual(rv2_dict["user_id"], u2_id)
        self.assertGreater(
            datetime.datetime.fromisoformat(rv2_dict["last_updated"]), datetime.datetime.fromisoformat(orig_date)
        )

        # User 2 should be able to see the Participant now
        rv3 = self.client.get(f"/api/participant/{p_id}", content_type="application/json", headers=u2_headers)
        self.assert_success(rv3)
        rv3_dict = rv3.json
        self.assertEqual(rv3_dict["user_id"], u2_id)
        self.assertNotEqual(orig_date, rv3_dict["last_updated"])

        # User 1 should not be able to see the Participant now
        rv_no_access3 = self.client.get(f"/api/participant/{p_id}", content_type="application/json", headers=u1_headers)
        self.assertEqual(400, rv_no_access3.status_code)
        resp_no_access3 = rv_no_access3.json
        self.assertEqual(resp_no_access3["code"], "unrelated_participant")

    def test_delete_participant(self):
        u = self.default_user
        p = self.construct_participant(user_id=u.id, relationship=Relationship.dependent)
        admin_headers = self.default_logged_in_headers
        p_id = p.id
        rv = self.client.get("api/participant/%i" % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.get("api/participant/%i" % p_id, content_type="application/json", headers=admin_headers)
        self.assert_success(rv)

        rv = self.client.delete("api/participant/%i" % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.delete("api/participant/%i" % p_id, content_type="application/json", headers=admin_headers)
        self.assert_success(rv)

        rv = self.client.get("api/participant/%i" % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.get("api/participant/%i" % p_id, content_type="application/json", headers=admin_headers)
        self.assertEqual(404, rv.status_code)

    def test_create_participant(self):
        p = {"id": 7, "relationship": "self_participant"}
        rv = self.client.post(
            "/api/session/participant", data=self.jsonify(p), content_type="application/json", follow_redirects=True
        )
        self.assertEqual(401, rv.status_code, "you can't create a participant without an account.")

        rv = self.client.post(
            "/api/session/participant",
            data=self.jsonify(p),
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)

        participant = self.session.query(Participant).filter_by(id=p["id"]).first()

        self.assertIsNotNone(participant.id)
        self.assertIsNotNone(participant.user_id)

    def test_create_participant_to_have_bad_relationship(self):
        participant = {"id": 234, "relationship": "free_loader"}
        rv = self.client.post(
            "/api/session/participant",
            data=self.jsonify(participant),
            content_type="application/json",
            follow_redirects=True,
            headers=self.default_logged_in_headers,
        )
        self.assertEqual(400, rv.status_code, "you can't create a participant using an invalid relationship")
        response = rv.json
        self.assertEqual(response["code"], "unknown_relationship")

    def test_create_participant_to_have_invalid_relationship(self):
        u = self.default_user
        p = {"id": 10, "relationship": "self_guardian", "user_id": u.id}
        rv = self.client.post(
            "/api/session/participant",
            data=self.jsonify(p),
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)

        p_bad = {"id": 10, "relationship": "self_guardian", "user_id": u.id}
        rv_bad = self.client.post(
            "/api/session/participant",
            data=self.jsonify(p_bad),
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )

        self.assertEqual(400, rv_bad.status_code, "You may not edit another users account.")
        response = json.loads(rv_bad.get_data(as_text=True))
        self.assertEqual(response["code"], "permission_denied")

    def test_get_participant_by_user(self):
        u = self.default_user
        p = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant)
        self.session.commit()
        rv = self.client.get(
            "/api/user/%i" % u.id, content_type="application/json", headers=self.default_logged_in_headers
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(u.id, response["id"])
        self.assertEqual(1, len(response["participants"]))
        self.assertEqual(p.relationship.name, response["participants"][0]["relationship"])

    def test_participant_ids_are_not_sequential(self):
        u = self.default_user
        p1 = self.construct_participant(user_id=u.id, relationship=Relationship.self_participant)
        p2 = self.construct_participant(user_id=u.id, relationship=Relationship.dependent)
        p3 = self.construct_participant(user_id=u.id, relationship=Relationship.dependent)

        self.assertNotEqual(p1.id + 1, p2.id)
        self.assertNotEqual(p2.id + 1, p3.id)

    def test_participant_admin_list(self):
        u1 = self.construct_user(email=fake.email())
        u2 = self.construct_user(email=fake.email())
        self.construct_participant(user_id=u1.id, relationship=Relationship.self_participant)
        self.construct_participant(user_id=u2.id, relationship=Relationship.self_participant)
        self.construct_participant(user_id=u1.id, relationship=Relationship.self_guardian)
        self.construct_participant(user_id=u1.id, relationship=Relationship.dependent)
        self.construct_participant(user_id=u2.id, relationship=Relationship.self_professional)
        rv = self.client.get(
            "/api/participant_admin_list", content_type="application/json", headers=self.default_logged_in_headers
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(2, response["num_self_participants"])
        self.assertEqual(1, response["num_self_guardians"])
        self.assertIsNotNone(response["num_dependents"])
        self.assertIsNotNone(response["num_self_professionals"])
        self.assertIsNotNone(response["all_participants"])

    def test_participant_percent_complete(self):
        u, p = self.construct_user_and_participant(relationship=Relationship.self_participant)
        u_id = u.id
        p_id = p.id
        user_headers = self.logged_in_headers(user_id=u_id)
        admin_headers = self.default_logged_in_headers

        rv = self.client.get("/api/participant", content_type="application/json", headers=admin_headers)
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(0, response[0]["percent_complete"])

        iq = self.get_identification_questionnaire(p_id)
        self.client.post(
            "api/flow/self_intake/identification_questionnaire",
            data=self.jsonify(iq),
            content_type="application/json",
            follow_redirects=True,
            headers=user_headers,
        )

        rv = self.client.get("/api/participant", content_type="application/json", headers=admin_headers)
        self.assert_success(rv)
        response = rv.json
        self.assertGreater(response[0]["percent_complete"], 0)

    def test_participant_name(self):
        u, p = self.construct_user_and_participant(relationship=Relationship.self_participant)
        u_id = u.id
        p_id = p.id
        admin_headers = self.default_logged_in_headers
        self.session.close()

        rv = self.client.get("/api/participant", content_type="application/json", headers=admin_headers)
        self.assert_success(rv)
        response = rv.json

        self.construct_identification_questionnaire(first_name="Felicity", nickname="City", participant_id=p_id)
        rv = self.client.get("/api/participant", content_type="application/json", headers=admin_headers)
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[0]["name"], "City")

    def test_user_meta(self):
        u = self.default_user
        usermeta = UserMeta(id=u.id, interested=True)
        self.session.add(usermeta)
        self.session.commit()
        rv = self.client.get(
            "/api/user/%i/usermeta" % u.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["interested"], True)

    def test_create_user_meta(self):
        u = self.default_user
        um = {"id": u.id, "professional": True}
        rv = self.client.post(
            "/api/user/%i/usermeta" % u.id,
            data=self.jsonify(um),
            content_type="application/json",
            follow_redirects=True,
        )
        self.assertEqual(401, rv.status_code, "you can't create a participant without an account.")
        rv = self.client.post(
            "/api/user/%i/usermeta" % u.id,
            data=self.jsonify(um),
            content_type="application/json",
            headers=self.logged_in_headers(u.id),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["professional"], True)
        self.assertIsNotNone(response["id"])

    def test_post_self_has_guardian(self):
        u = self.default_user
        usermeta = UserMeta(id=u.id, self_participant=True, self_has_guardian=True)
        self.session.add(usermeta)
        self.session.commit()
        rv = self.client.get(
            "/api/user/%i/usermeta" % u.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["self_has_guardian"], True)
        rel = usermeta.get_relationship()
        self.assertEqual(rel, None)

    def test_post_no_metadata(self):
        u = self.default_user
        usermeta = UserMeta(id=u.id)
        self.session.add(usermeta)
        self.session.commit()
        rv = self.client.get(
            "/api/user/%i/usermeta" % u.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        rel = usermeta.get_relationship()
        self.assertEqual(rel, "")

    def test_delete_user_meta(self):
        u = self.default_user
        u_id = u.id
        admin_headers = self.default_logged_in_headers
        usermeta = UserMeta(id=u_id, interested=True)
        self.session.add(usermeta)
        self.session.commit()
        rv = self.client.get("/api/user/%i/usermeta" % u_id, follow_redirects=True, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.get(
            "/api/user/%i/usermeta" % u_id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        rv = self.client.delete("/api/user/%i/usermeta" % u_id, content_type="application/json")
        self.assertEqual(401, rv.status_code, "Anonymous user can't delete user meta.")
        rv = self.client.delete("/api/user/%i/usermeta" % u_id, content_type="application/json", headers=admin_headers)
        self.assert_success(rv)
        rv = self.client.get("/api/user/%i/usermeta" % u_id, follow_redirects=True, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.get(
            "/api/user/%i/usermeta" % u_id,
            follow_redirects=True,
            content_type="application/json",
            headers=admin_headers,
        )
        self.assertEqual(404, rv.status_code)

    def test_user_meta_serialize(self):
        u = self.default_user
        usermeta = UserMeta(id=u.id, interested=True)
        result = usermeta.get_relationship()
        self.assertEqual(result, "self_interested")
        SchemaRegistry.UserMetaSchema().dump(usermeta)
