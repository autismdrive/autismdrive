from app.model.admin_note import AdminNote
from tests.base_test import BaseTest


class TestAdminNote(BaseTest):
    def test_admin_note_basics(self):
        u = self.construct_user()
        l = self.construct_location()
        self.construct_admin_note(id=377, user=u, resource=l, note="This resource is related to an event record")
        an = self.session.query(AdminNote).first()
        self.assertIsNotNone(an)
        headers = self.logged_in_headers()
        rv = self.client.get(
            f"/api/admin_note/{an.id}",
            follow_redirects=True,
            content_type="application/json",
            headers=headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], an.id)
        self.assertEqual(response["note"], "This resource is related to an event record")

    def test_modify_admin_note_basics(self):
        u = self.construct_user()
        e = self.construct_event()
        self.construct_admin_note(id=342, user=u, resource=e, note="This event is related to a location record")
        an = self.session.query(AdminNote).first()
        self.assertIsNotNone(an)
        rv = self.client.get(
            "/api/admin_note/%i" % an.id, content_type="application/json", headers=self.logged_in_headers()
        )
        response = rv.json
        response["note"] = "Related to Location #42"
        rv = self.client.put(
            "/api/admin_note/%i" % an.id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        self.session.commit()
        rv = self.client.get(
            "/api/admin_note/%i" % an.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["note"], "Related to Location #42")

    def test_delete_admin_note(self):
        an = self.construct_admin_note(user=self.construct_user(), resource=self.construct_resource())
        an_id = an.id
        rv = self.client.get(
            "api/admin_note/%i" % an_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.delete(
            "api/admin_note/%i" % an_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.get(
            "api/admin_note/%i" % an_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assertEqual(404, rv.status_code)

    def test_create_admin_note(self):
        admin_note = {
            "note": "My Favorite Things",
            "user_id": self.construct_user().id,
            "resource_id": self.construct_resource().id,
        }
        rv = self.client.post(
            "api/admin_note",
            data=self.jsonify(admin_note),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["note"], "My Favorite Things")
        self.assertIsNotNone(response["id"])

    def test_admin_note_by_user_basics(self):
        u = self.construct_user()
        r = self.construct_resource()
        self.construct_admin_note(id=467, user=u, resource=r, note="Lotsa stuff to say about this resource")
        an = self.session.query(AdminNote).first()
        self.assertIsNotNone(an)
        rv = self.client.get(
            "/api/user/%i/admin_note" % u.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[0]["id"], an.id)
        self.assertEqual(response[0]["id"], 467)
        self.assertEqual(response[0]["note"], "Lotsa stuff to say about this resource")

    def test_admin_note_by_resource_basics(self):
        u = self.construct_user()
        r = self.construct_resource()
        self.construct_admin_note(user=u, resource=r, note="This resource is a duplicate")
        an = self.session.query(AdminNote).first()
        self.assertIsNotNone(an)
        rv = self.client.get(
            "/api/resource/%i/admin_note" % r.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[0]["id"], an.id)
        self.assertEqual(response[0]["note"], "This resource is a duplicate")

    def test_many_notes(self):
        u1 = self.construct_user(email="u1@sartography.com")
        u2 = self.construct_user(email="u2@sartography.com")
        r1 = self.construct_resource(title="R1")
        r2 = self.construct_resource(title="R2")
        r3 = self.construct_resource(title="R3")
        r4 = self.construct_resource(title="R4")
        self.construct_admin_note(id=324, user=u1, resource=r1, note="This resource is a duplicate")
        self.construct_admin_note(id=249, user=u1, resource=r3, note="This is my favorite resource")
        self.construct_admin_note(
            id=569, user=u2, resource=r1, note="I don't agree - I think this is a separate resource"
        )
        self.construct_admin_note(id=208, user=u2, resource=r2, note="Their hours have changed to 3-4PM Sundays")
        self.construct_admin_note(id=796, user=u2, resource=r4, note="They have a waiting list of 20 as of today.")
        rv = self.client.get(
            "/api/admin_note", follow_redirects=True, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(5, len(response))
        rv = self.client.get(
            "/api/resource/%i/admin_note" % r1.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(2, len(response))
        rv = self.client.get(
            "/api/user/%i/admin_note" % u2.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(3, len(response))
