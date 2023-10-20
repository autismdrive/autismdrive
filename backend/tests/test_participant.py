from flask import json

from app.models import Participant, UserMeta
from app.enums import Relationship
from app.schemas import UserMetaSchema
from tests.base_test_questionnaire import BaseTestQuestionnaire


class TestParticipant(BaseTestQuestionnaire):
    def test_participant_relationships(self):
        u = self.construct_user()
        participant = self.construct_participant(user=u, relationship=Relationship.self_participant)
        guardian = self.construct_participant(user=u, relationship=Relationship.self_guardian)
        dependent = self.construct_participant(user=u, relationship=Relationship.dependent)
        professional = self.construct_participant(user=u, relationship=Relationship.self_professional)
        interested = self.construct_participant(user=u, relationship=Relationship.self_interested)
        rv = self.client.get(
            "/api/user/%i" % u.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], u.id)
        self.assertEqual(len(response["participants"]), 5)
        self.assertEqual(response["participants"][0]["id"], participant.id)
        self.assertEqual(response["participants"][0]["relationship"], "self_participant")
        self.assertEqual(response["participants"][1]["id"], guardian.id)
        self.assertEqual(response["participants"][1]["relationship"], "self_guardian")
        self.assertEqual(response["participants"][2]["id"], dependent.id)
        self.assertEqual(response["participants"][2]["relationship"], "dependent")
        self.assertEqual(response["participants"][3]["id"], professional.id)
        self.assertEqual(response["participants"][3]["relationship"], "self_professional")
        self.assertEqual(response["participants"][4]["id"], interested.id)
        self.assertEqual(response["participants"][4]["relationship"], "self_interested")

    def test_participant_basics(self):
        self.construct_participant(user=self.construct_user(), relationship=Relationship.dependent)
        p = self.session.query(Participant).first()
        self.assertIsNotNone(p)
        p_id = p.id
        rv = self.client.get(
            "/api/participant/%i" % p_id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], p_id)
        self.assertEqual(response["relationship"], p.relationship.name)

    def test_modify_participant_you_do_not_own(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        good_headers = self.logged_in_headers(u)

        p = self.session.query(Participant).first()
        odd_user = self.construct_user(email="frankie@badfella.rf")
        participant = {"first_name": "Lil' Johnny", "last_name": "Tables"}
        rv = self.client.put(
            "/api/participant/%i" % p.id,
            data=self.jsonify(participant),
            content_type="application/json",
            follow_redirects=True,
        )
        self.assertEqual(401, rv.status_code, "you have to be logged in to edit participant.")
        rv = self.client.put(
            "/api/participant/%i" % p.id,
            data=self.jsonify(participant),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(odd_user),
        )
        self.assertEqual(400, rv.status_code, "you have to have a relationship with the user to do stuff.")
        response = rv.json
        self.assertEqual("unrelated_participant", response["code"])
        rv = self.client.put(
            "/api/participant/%i" % p.id,
            data=self.jsonify(participant),
            content_type="application/json",
            follow_redirects=True,
            headers=good_headers,
        )
        self.assertEqual(200, rv.status_code, "The owner can edit the user.")

    def test_modify_participant_you_do_own(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_guardian)
        headers = self.logged_in_headers(u)
        participant = {"id": 567}
        rv = self.client.put(
            "/api/participant/%i" % p.id,
            data=self.jsonify(participant),
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)
        p = self.session.query(Participant).filter_by(id=p.id).first()
        self.assertEqual(567, p.id)

    def test_modify_participant_basics_admin(self):
        self.construct_participant(user=self.construct_user(), relationship=Relationship.dependent)
        user2 = self.construct_user(email="theotherguy@stuff.com")
        logged_in_headers = self.logged_in_headers()
        p = self.session.query(Participant).first()
        self.assertIsNotNone(p)
        p_id = p.id
        rv = self.client.get("/api/participant/%i" % p_id, content_type="application/json", headers=logged_in_headers)
        self.assert_success(rv)
        response = rv.json
        response["user_id"] = user2.id
        orig_date = response["last_updated"]
        rv = self.client.put(
            "/api/participant/%i" % p_id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=logged_in_headers,
        )
        self.assert_success(rv)
        rv = self.client.get("/api/participant/%i" % p_id, content_type="application/json", headers=logged_in_headers)
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["user_id"], user2.id)
        self.assertNotEqual(orig_date, response["last_updated"])

    def test_delete_participant(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.dependent)
        p_id = p.id
        rv = self.client.get("api/participant/%i" % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.get(
            "api/participant/%i" % p_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.delete("api/participant/%i" % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.delete(
            "api/participant/%i" % p_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.get("api/participant/%i" % p_id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.get(
            "api/participant/%i" % p_id, content_type="application/json", headers=self.logged_in_headers()
        )
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
            headers=self.logged_in_headers(),
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
            headers=self.logged_in_headers(),
        )
        self.assertEqual(400, rv.status_code, "you can't create a participant using an invalid relationship")
        response = rv.json
        self.assertEqual(response["code"], "unknown_relationship")

    def test_create_participant_to_have_invalid_relationship(self):
        u = self.construct_user()
        p = {"id": 10, "relationship": "self_guardian", "user_id": u.id}
        rv = self.client.post(
            "/api/session/participant",
            data=self.jsonify(p),
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)

        p_bad = {"id": 10, "relationship": "self_guardian", "user_id": u.id}
        rv_bad = self.client.post(
            "/api/session/participant",
            data=self.jsonify(p_bad),
            content_type="application/json",
            headers=self.logged_in_headers(),
        )

        self.assertEqual(400, rv_bad.status_code, "You may not edit another users account.")
        response = json.loads(rv_bad.get_data(as_text=True))
        self.assertEqual(response["code"], "permission_denied")

    def test_get_participant_by_user(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        self.session.commit()
        rv = self.client.get("/api/user/%i" % u.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(u.id, response["id"])
        self.assertEqual(1, len(response["participants"]))
        self.assertEqual(p.relationship.name, response["participants"][0]["relationship"])

    def test_participant_ids_are_not_sequential(self):
        u = self.construct_user()
        p1 = self.construct_participant(user=u, relationship=Relationship.self_participant)
        p2 = self.construct_participant(user=u, relationship=Relationship.dependent)
        p3 = self.construct_participant(user=u, relationship=Relationship.dependent)

        self.assertNotEqual(p1.id + 1, p2.id)
        self.assertNotEqual(p2.id + 1, p3.id)

    def test_participant_admin_list(self):
        u1 = self.construct_user(email="test1@sartography.com")
        u2 = self.construct_user(email="test2@sartography.com")
        self.construct_participant(user=u1, relationship=Relationship.self_participant)
        self.construct_participant(user=u2, relationship=Relationship.self_participant)
        self.construct_participant(user=u1, relationship=Relationship.self_guardian)
        self.construct_participant(user=u1, relationship=Relationship.dependent)
        self.construct_participant(user=u2, relationship=Relationship.self_professional)
        rv = self.client.get(
            "/api/participant_admin_list", content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(2, response["num_self_participants"])
        self.assertEqual(1, response["num_self_guardians"])
        self.assertIsNotNone(response["num_dependents"])
        self.assertIsNotNone(response["num_self_professionals"])
        self.assertIsNotNone(response["all_participants"])

    def test_participant_percent_complete(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)

        rv = self.client.get("/api/participant", content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(0, response[0]["percent_complete"])

        iq = self.get_identification_questionnaire(p.id)
        self.client.post(
            "api/flow/self_intake/identification_questionnaire",
            data=self.jsonify(iq),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(u),
        )

        rv = self.client.get("/api/participant", content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertGreater(response[0]["percent_complete"], 0)

    def test_participant_name(self):
        p = self.construct_participant(user=self.construct_user(), relationship=Relationship.self_participant)
        rv = self.client.get("/api/participant", content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[0]["name"], "")

        self.construct_identification_questionnaire(first_name="Felicity", nickname="City", participant=p)
        rv = self.client.get("/api/participant", content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[0]["name"], "City")

    def test_user_meta(self):
        u = self.construct_user()
        usermeta = UserMeta(id=u.id, interested=True)
        self.session.add(usermeta)
        self.session.commit()
        rv = self.client.get(
            "/api/user/%i/usermeta" % u.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["interested"], True)

    def test_create_user_meta(self):
        u = self.construct_user()
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
            headers=self.logged_in_headers(u),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["professional"], True)
        self.assertIsNotNone(response["id"])

    def test_post_self_has_guardian(self):
        u = self.construct_user()
        usermeta = UserMeta(id=u.id, self_participant=True, self_has_guardian=True)
        self.session.add(usermeta)
        self.session.commit()
        rv = self.client.get(
            "/api/user/%i/usermeta" % u.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["self_has_guardian"], True)
        rel = usermeta.get_relationship()
        self.assertEqual(rel, None)

    def test_post_no_metadata(self):
        u = self.construct_user()
        usermeta = UserMeta(id=u.id)
        self.session.add(usermeta)
        self.session.commit()
        rv = self.client.get(
            "/api/user/%i/usermeta" % u.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        rel = usermeta.get_relationship()
        self.assertEqual(rel, "")

    def test_delete_user_meta(self):
        u = self.construct_user()
        usermeta = UserMeta(id=u.id, interested=True)
        self.session.add(usermeta)
        self.session.commit()
        rv = self.client.get("/api/user/%i/usermeta" % u.id, follow_redirects=True, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.get(
            "/api/user/%i/usermeta" % u.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        rv = self.client.delete("/api/user/%i/usermeta" % u.id, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.delete(
            "/api/user/%i/usermeta" % u.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        rv = self.client.get("/api/user/%i/usermeta" % u.id, follow_redirects=True, content_type="application/json")
        self.assertEqual(401, rv.status_code)
        rv = self.client.get(
            "/api/user/%i/usermeta" % u.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assertEqual(404, rv.status_code)

    def test_user_meta_serialize(self):
        u = self.construct_user()
        usermeta = UserMeta(id=u.id, interested=True)
        result = usermeta.get_relationship()
        self.assertEqual(result, "self_interested")
        UserMetaSchema().dump(usermeta)
