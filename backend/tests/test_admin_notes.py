from copy import deepcopy

from sqlalchemy import desc

from tests.base_test import BaseTest  # isort:skip
from app.models import AdminNote
from tests.fixtures.fixture_utils import fake


class TestAdminNote(BaseTest):
    def test_admin_note_basics(self):
        u = self.default_user
        loc = self.construct_location()
        an = self.construct_admin_note(user=u, resource=loc, note="This resource is related to an event record")
        self.assertIsNotNone(an)

        db_an = self.session.query(AdminNote).first()
        self.assertIsNotNone(db_an)

        headers = self.default_logged_in_headers
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
        note1 = fake.paragraph()
        note2 = fake.paragraph()
        assert note1 != note2

        u = self.default_user
        e = self.construct_event()
        self.construct_admin_note(user=u, resource=e, note=note1)
        an = self.session.query(AdminNote).filter_by(user_id=u.id, resource_id=e.id).order_by(desc(AdminNote.last_updated)).first()
        self.assertIsNotNone(an)
        rv = self.client.get(
            "/api/admin_note/%i" % an.id, content_type="application/json", headers=self.default_logged_in_headers
        )
        rv1_dict = rv.json
        self.assertEqual(rv1_dict["note"], note1)

        modified_dict = deepcopy(rv1_dict)
        modified_dict["note"] = note2
        rv2 = self.client.put(
            "/api/admin_note/%i" % an.id,
            data=self.jsonify(modified_dict),
            content_type="application/json",
            follow_redirects=True,
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv2)
        rv2_dict = rv2.json
        self.assertEqual(rv2_dict["note"], note2)

        rv3 = self.client.get(
            "/api/admin_note/%i" % an.id, content_type="application/json", headers=self.default_logged_in_headers
        )
        self.assert_success(rv3)
        rv3_dict = rv3.json
        self.assertEqual(rv3_dict["note"], note2)

    def test_delete_admin_note(self):
        an = self.construct_admin_note(user=self.default_user, resource=self.construct_resource())
        an_id = an.id
        self.session.close()

        rv = self.client.get(
            "api/admin_note/%i" % an_id, content_type="application/json", headers=self.default_logged_in_headers
        )
        self.assert_success(rv)

        rv = self.client.delete(
            "api/admin_note/%i" % an_id, content_type="application/json", headers=self.default_logged_in_headers
        )
        self.assert_success(rv)

        rv = self.client.get(
            "api/admin_note/%i" % an_id, content_type="application/json", headers=self.default_logged_in_headers
        )
        self.assertEqual(404, rv.status_code)

    def test_create_admin_note(self):
        admin_note = {
            "note": "My Favorite Things",
            "user_id": self.default_user.id,
            "resource_id": self.construct_resource().id,
        }
        rv = self.client.post(
            "api/admin_note",
            data=self.jsonify(admin_note),
            content_type="application/json",
            follow_redirects=True,
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["note"], "My Favorite Things")
        self.assertIsNotNone(response["id"])

    def test_admin_note_by_user_basics(self):
        u = self.default_user
        r = self.construct_resource()
        self.construct_admin_note(user=u, resource=r, note="Lotsa stuff to say about this resource")
        an = self.session.query(AdminNote).first()
        self.assertIsNotNone(an)
        rv = self.client.get(
            "/api/user/%i/admin_note" % u.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[0]["id"], an.id)
        self.assertEqual(response[0]["note"], "Lotsa stuff to say about this resource")

    def test_admin_note_by_resource_basics(self):
        u = self.default_user
        r = self.construct_resource()
        self.construct_admin_note(user=u, resource=r, note="This resource is a duplicate")
        an = self.session.query(AdminNote).first()
        self.assertIsNotNone(an)
        rv = self.client.get(
            "/api/resource/%i/admin_note" % r.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
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
        self.construct_admin_note(user=u1, resource=r1, note="This resource is a duplicate")
        self.construct_admin_note(user=u1, resource=r3, note="This is my favorite resource")
        self.construct_admin_note(user=u2, resource=r1, note="I don't agree - I think this is a separate resource")
        self.construct_admin_note(user=u2, resource=r2, note="Their hours have changed to 3-4PM Sundays")
        self.construct_admin_note(user=u2, resource=r4, note="They have a waiting list of 20 as of today.")
        rv = self.client.get(
            "/api/admin_note",
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(5, len(response))
        rv = self.client.get(
            "/api/resource/%i/admin_note" % r1.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(2, len(response))
        rv = self.client.get(
            "/api/user/%i/admin_note" % u2.id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(3, len(response))
