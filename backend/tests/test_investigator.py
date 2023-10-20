from app.models import Investigator, StudyInvestigator
from tests.base_test import BaseTest


class TestStudy(BaseTest):
    def test_investigator_basics(self):
        self.construct_investigator()
        i = self.session.query(Investigator).first()
        self.assertIsNotNone(i)
        i_id = i.id
        rv = self.client.get(
            "/api/investigator/%i" % i_id,
            follow_redirects=True,
            content_type="application/json",
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], i_id)
        self.assertEqual(response["name"], i.name)

    def test_modify_investigator_basics(self):
        self.construct_investigator()
        i = self.session.query(Investigator).first()
        self.assertIsNotNone(i)

        rv = self.client.get(
            "/api/investigator/%i" % i.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        response["title"] = "dungeon master"
        orig_date = response["last_updated"]
        rv = self.client.put(
            "/api/investigator/%i" % i.id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)

        response = rv.json
        self.assertEqual(response["title"], "dungeon master")
        self.assertNotEqual(orig_date, response["last_updated"])

    def test_delete_investigator(self):
        i = self.construct_investigator()
        i_id = i.id

        rv = self.client.get(
            "api/investigator/%i" % i_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.delete(
            "api/investigator/%i" % i_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.get(
            "api/investigator/%i" % i_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assertEqual(404, rv.status_code)

    def test_create_investigator(self):
        investigator = {
            "name": "Tara Tarantula",
            "title": "Assistant Professor of Arachnology",
            "organization_name": "Spider University",
        }
        rv = self.client.post(
            "api/investigator",
            data=self.jsonify(investigator),
            content_type="application/json",
            headers=self.logged_in_headers(),
            follow_redirects=True,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["name"], "Tara Tarantula")
        self.assertEqual(response["title"], "Assistant Professor of Arachnology")
        self.assertIsNotNone(response["id"])

    def test_investigator_list_alphabetical_by_name(self):
        self.construct_investigator(name="Adelaide Smith")
        self.construct_investigator(name="Sarah Blakemore")
        self.construct_investigator(name="Zelda Cat")
        self.construct_investigator(name="Benjamin Jensen")

        rv = self.client.get("api/investigator", content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[0]["name"], "Adelaide Smith")
        self.assertEqual(response[1]["name"], "Benjamin Jensen")
        self.assertEqual(response[2]["name"], "Sarah Blakemore")
        self.assertEqual(response[3]["name"], "Zelda Cat")

    def test_create_investigator_checks_for_name(self):
        self.test_create_investigator()
        rv = self.client.get("api/investigator", content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[0]["name"], "Tara Tarantula")
        self.assertEqual(response[0]["title"], "Assistant Professor of Arachnology")

        investigator = {"name": "Tara Tarantula", "title": "Spider"}
        rv = self.client.post(
            "api/investigator",
            data=self.jsonify(investigator),
            content_type="application/json",
            headers=self.logged_in_headers(),
            follow_redirects=True,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["name"], "Tara Tarantula")
        self.assertEqual(response["title"], "Assistant Professor of Arachnology")

    def test_delete_investigator_deletes_relationship(self):
        i = self.construct_investigator()
        s = self.construct_study()
        si = StudyInvestigator(investigator_id=i.id, study_id=s.id)
        self.session.add(si)
        self.session.commit()
        si_id = si.id

        rv = self.client.get(
            "api/study_investigator/%i" % si_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.delete(
            "api/investigator/%i" % i.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.get(
            "api/study_investigator/%i" % si_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assertEqual(404, rv.status_code)
