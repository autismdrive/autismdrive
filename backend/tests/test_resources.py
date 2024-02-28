from collections import Counter

from sqlalchemy import select

from app.elastic_index import elastic_index
from app.enums import Role
from app.models import Resource, ResourceCategory, ResourceChangeLog
from fixtures.fixure_utils import fake
from fixtures.resource import MockResource
from tests.base_test import BaseTest


class TestResources(BaseTest):
    def test_resource_basics(self):
        r = self.construct_resource()
        r_id = r.id
        rv = self.client.get("/api/resource/%i" % r_id, follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], r_id)
        self.assertEqual(response["title"], r.title)
        self.assertEqual(response["description"], r.description)

    def test_modify_resource_basics(self):
        self.construct_resource()
        r = self.session.query(Resource).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.client.get("/api/resource/%i" % r_id, content_type="application/json")
        response = rv.json
        response["title"] = "Edwarardos Lemonade and Oil Change"
        response["description"] = "Better fluids for you and your car."
        response["website"] = "http://sartography.com"
        orig_date = response["last_updated"]
        rv = self.client.put(
            "/api/resource/%i" % r_id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        rv = self.client.get("/api/resource/%i" % r_id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["title"], "Edwarardos Lemonade and Oil Change")
        self.assertEqual(response["description"], "Better fluids for you and your car.")
        self.assertEqual(response["website"], "http://sartography.com")
        self.assertNotEqual(orig_date, response["last_updated"])

    def test_delete_resource(self):
        r = self.construct_resource()
        r_id = r.id
        rv = self.client.get("api/resource/%i" % r_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.client.delete(
            "api/resource/%i" % r_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.get("api/resource/%i" % r_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_delete_resource_with_admin_note_and_no_elastic_record(self):
        from app.schemas import SchemaRegistry
        from app.utils.resource_utils import to_database_object_dict

        r = self.construct_resource()
        r_id = r.id
        rv = self.client.get("api/resource/%i" % r_id, content_type="application/json")
        self.assert_success(rv)

        self.construct_admin_note(user=self.construct_user(), resource=r)
        resource_dict = to_database_object_dict(SchemaRegistry.ResourceSchema(), r)
        elastic_index.remove_document(resource_dict)
        rv = self.client.delete(
            "api/resource/%i" % r_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.get("api/resource/%i" % r_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_resource(self):
        resource = MockResource()
        rv = self.client.post(
            "api/resource",
            data=self.jsonify(resource),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["title"], resource.title)
        self.assertEqual(response["description"], resource.description)
        self.assertIsNotNone(response["id"])

    def test_get_resource_by_category(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c, type="resource")
        self.session.add(cr)
        self.session.commit()
        rv = self.client.get(
            "/api/category/%i/resource" % c.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(r.id, response[0]["resource_id"])
        self.assertEqual(r.description, response[0]["resource"]["description"])

    def test_get_resource_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c, type="resource")
        cr2 = ResourceCategory(resource=r, category=c2, type="resource")
        self.session.add_all([cr, cr2])
        self.session.commit()
        rv = self.client.get(
            "/api/category/%i/resource" % c.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(r.id, response[0]["resource_id"])
        self.assertEqual(2, len(response[0]["resource"]["resource_categories"]))
        self.assertEqual("c1", response[0]["resource"]["resource_categories"][0]["category"]["name"])

    def test_category_resource_count(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c, type="resource")
        self.session.add(cr)
        self.session.commit()
        rv = self.client.get("/api/category/%i" % c.id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, response["resource_count"])

    def test_get_category_by_resource(self):
        c = self.construct_category()
        r = self.construct_resource()
        cr = ResourceCategory(resource=r, category=c, type="resource")
        self.session.add(cr)
        self.session.commit()
        rv = self.client.get("/api/resource/%i/category" % r.id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_resource(self):
        c = self.construct_category()
        r = self.construct_resource()

        rc_data = {"resource_id": r.id, "category_id": c.id}

        rv = self.client.post("/api/resource_category", data=self.jsonify(rc_data), content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(r.id, response["resource_id"])

    def test_set_all_categories_on_resource(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        r = self.construct_resource()

        rc_data = [
            {"category_id": c1.id},
            {"category_id": c2.id},
            {"category_id": c3.id},
        ]
        rv = self.client.post(
            "/api/resource/%i/category" % r.id, data=self.jsonify(rc_data), content_type="application/json"
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(3, len(response))

        rc_data = [{"category_id": c1.id}]
        rv = self.client.post(
            "/api/resource/%i/category" % r.id, data=self.jsonify(rc_data), content_type="application/json"
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))

    def test_remove_category_from_resource(self):
        self.test_add_category_to_resource()
        rv = self.client.delete("/api/resource_category/%i" % 1)
        self.assert_success(rv)
        rv = self.client.get("/api/resource/%i/category" % 1, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(0, len(response))

    def test_resource_change_log_types(self):
        u_email = fake.email()
        u = self.construct_user(email=u_email, role=Role.admin)
        user_id = u.id
        headers = self.logged_in_headers(user=u)
        mock_resource = MockResource()
        rv_1 = self.client.post(
            "api/resource",
            json=mock_resource.__dict__,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv_1)
        r_1 = rv_1.json
        resource_id = r_1["id"]

        logs = self.session.query(ResourceChangeLog).all()
        self.assertEqual(logs[-1].resource_id, resource_id)
        self.assertEqual(logs[-1].user_id, user_id)
        self.assertEqual(logs[-1].type, "create")

        url = f"api/resource/{resource_id}"
        rv = self.client.get(url, content_type="application/json")
        self.assert_success(rv)

        response = rv.json
        new_title = fake.catch_phrase()
        response["title"] = new_title
        rv = self.client.put(
            url,
            json=response,
            content_type="application/json",
            follow_redirects=True,
            headers=headers,
        )
        self.assert_success(rv)
        rv = self.client.get(url, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["title"], new_title)

        logs = self.session.query(ResourceChangeLog).all()
        self.assertEqual(logs[-1].resource_id, resource_id)
        self.assertEqual(logs[-1].user_id, user_id)
        self.assertEqual(logs[-1].type, "edit")

        rv = self.client.delete(url, content_type="application/json", headers=headers)
        self.assert_success(rv)

        logs = self.session.query(ResourceChangeLog).all()
        self.assertEqual(logs[-1].resource_id, resource_id)
        self.assertEqual(logs[-1].user_id, user_id)
        self.assertEqual(logs[-1].type, "delete")

    def test_get_resource_change_log_by_resource(self):
        r = self.construct_resource()
        u = self.construct_user(email="editor@sartorgraphy.com", role=Role.admin)
        rv = self.client.get("api/resource/%i" % r.id, content_type="application/json")
        self.assert_success(rv)

        response = rv.json
        response["title"] = "Super Great Resource"
        rv = self.client.put(
            "/api/resource/%i" % r.id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(user=u),
        )
        self.assert_success(rv)

        rv = self.client.get(
            "/api/resource/%i/change_log" % r.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[-1]["user_id"], u.id)

    def test_get_resource_change_log_by_user(self):
        r = self.construct_resource()
        u = self.construct_user(email="editor@sartorgraphy.com", role=Role.admin)
        rv = self.client.get("api/resource/%i" % r.id, content_type="application/json")
        self.assert_success(rv)

        response = rv.json
        response["title"] = "Super Great Resource"
        rv = self.client.put(
            "/api/resource/%i" % r.id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(user=u),
        )
        self.assert_success(rv)

        rv = self.client.get(
            "/api/user/%i/resource_change_log" % u.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[-1]["resource_id"], r.id)

    def test_covid19_resource_lists(self):
        covid_cats = [
            "covid_19_for_autism",
            "edu_tainment",
            "free_educational_resources",
            "supports_with_living",
            "visual_aids",
            "health_and_telehealth",
        ]

        resource_cats = [
            [0, 2],
            [0, 1, 2],
            [0, 1, 3],
            [0, 1, 4],
            [0, 1, 5],
        ]

        for cat in resource_cats:
            resource_covid_cats = [covid_cats[i] for i in cat]
            new_r = self.construct_resource(covid19_categories=resource_covid_cats, is_draft=False)
            db_r = self.session.execute(select(Resource).filter(Resource.id == new_r.id)).unique().scalar_one()
            self.assertEqual(db_r.covid19_categories, resource_covid_cats)
            self.session.close()

        # Make a dict of the expected counts for each category, based on the resource_cats list
        expected_counts = dict(sum((Counter(sublist) for sublist in resource_cats), Counter()))

        for i, cat in enumerate(covid_cats):
            rv = self.client.get(f"api/resource/covid19/{cat}", content_type="application/json")
            self.assert_success(rv)
            response = rv.json
            self.assertEqual(len(response), expected_counts[i])

    def test_is_uva_education_content(self):
        self.construct_resource(is_draft=True, title="Autism at UVA", is_uva_education_content=True)
        self.construct_resource(is_draft=False, title="Healthy Eating", is_uva_education_content=True)
        self.construct_resource(is_draft=True, title="Autism and the Arts", is_uva_education_content=False)
        self.construct_resource(is_draft=False, title="Autism One", is_uva_education_content=True)
        self.construct_resource(is_draft=False, title="Two", is_uva_education_content=False)

        rv = self.client.get("api/resource/education", content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(len(response), 2)

        rv = self.client.get("api/resource", content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(len(response), 5)
