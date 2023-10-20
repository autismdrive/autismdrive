from app.models import ResourceCategory, Location, ResourceChangeLog
from app.enums import Role
from tests.base_test import BaseTest


class TestLocations(BaseTest):
    def test_location_basics(self):
        self.construct_location()
        r = self.session.query(Location).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.client.get("/api/location/%i" % r_id, follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], r_id)
        self.assertEqual(response["title"], "A+ location")
        self.assertEqual(response["description"], "A delightful location destined to create rejoicing")
        self.assertEqual(response["latitude"], 38.98765)
        self.assertEqual(response["longitude"], -93.12345)

    def test_modify_location_basics(self):
        self.construct_location()
        r = self.session.query(Location).first()
        self.assertIsNotNone(r)
        r_id = r.id
        rv = self.client.get("/api/location/%i" % r_id, content_type="application/json")
        response = rv.json
        response["title"] = "Edwarardos Lemonade and Oil Change"
        response["description"] = "Better fluids for you and your car."
        response["website"] = "http://sartography.com"
        response["latitude"] = 34.5678
        response["longitude"] = -98.7654
        orig_date = response["last_updated"]
        rv = self.client.put(
            "/api/location/%i" % r_id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        rv = self.client.get("/api/location/%i" % r_id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["title"], "Edwarardos Lemonade and Oil Change")
        self.assertEqual(response["description"], "Better fluids for you and your car.")
        self.assertEqual(response["website"], "http://sartography.com")
        self.assertEqual(response["latitude"], 34.5678)
        self.assertEqual(response["longitude"], -98.7654)
        self.assertNotEqual(orig_date, response["last_updated"])

    def test_delete_location(self):
        r = self.construct_location()
        r_id = r.id
        rv = self.client.get("api/location/%i" % r_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.client.delete(
            "api/location/%i" % r_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.get("api/location/%i" % r_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_location(self):
        self.loader.load_partial_zip_codes()
        location = {
            "title": "location of locations",
            "description": "You need this location in your life.",
            "organization_name": "Location Org",
        }
        rv = self.client.post(
            "api/location",
            data=self.jsonify(location),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["title"], "location of locations")
        self.assertEqual(response["description"], "You need this location in your life.")
        self.assertIsNotNone(response["id"])

    def test_get_location_by_category(self):
        loc = self.construct_location()
        c = self.construct_location_category(loc.id, "c1")

        rv = self.client.get(
            "/api/category/%i/location" % c.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(loc.id, response[0]["resource_id"])
        self.assertEqual(loc.description, response[0]["resource"]["description"])

    def test_get_location_by_category_includes_category_details(self):
        loc = self.construct_location()
        c1 = self.construct_location_category(loc.id, "c1")
        c2 = self.construct_location_category(loc.id, "c2")

        rv = self.client.get(
            "/api/category/%i/location" % c1.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(loc.id, response[0]["resource_id"])
        self.assertEqual(2, len(response[0]["resource"]["resource_categories"]))
        self.assertEqual("c1", response[0]["resource"]["resource_categories"][0]["category"]["name"])

    def test_category_location_count(self):
        loc = self.construct_location()
        c = self.construct_location_category(loc.id, "c1")
        rv = self.client.get("/api/category/%i" % c.id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, response["location_count"])

    def test_get_category_by_location(self):
        c = self.construct_category()
        loc = self.construct_location()
        rc = ResourceCategory(resource_id=loc.id, category=c, type="location")
        self.session.add(rc)
        self.session.commit()
        rv = self.client.get("/api/location/%i/category" % loc.id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_location(self):
        c = self.construct_category()
        loc = self.construct_location()

        rc_data = {"resource_id": loc.id, "category_id": c.id}

        rv = self.client.post("/api/resource_category", data=self.jsonify(rc_data), content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(loc.id, response["resource_id"])

    def test_set_all_categories_on_location(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        loc = self.construct_location()

        lc_data = [
            {"category_id": c1.id},
            {"category_id": c2.id},
            {"category_id": c3.id},
        ]
        rv = self.client.post(
            "/api/location/%i/category" % loc.id, data=self.jsonify(lc_data), content_type="application/json"
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(3, len(response))

        lc_data = [{"category_id": c1.id}]
        rv = self.client.post(
            "/api/location/%i/category" % loc.id, data=self.jsonify(lc_data), content_type="application/json"
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))

    def test_remove_category_from_location(self):
        self.test_add_category_to_location()
        rv = self.client.delete("/api/resource_category/%i" % 1)
        self.assert_success(rv)
        rv = self.client.get("/api/location/%i/category" % 1, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(0, len(response))

    def test_zip_code_coordinates(self):
        z = self.construct_zip_code()
        rv = self.client.get("/api/zip_code_coords/%i" % z.id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(z.id, response["id"])
        self.assertEqual(z.latitude, response["latitude"])
        self.assertEqual(z.longitude, response["longitude"])

    def test_resource_change_log(self):
        l = self.construct_location(title="A Location that is Super and Great")
        u = self.construct_user(email="editor@sartorgraphy.com", role=Role.admin)

        rv = self.client.get("api/location/%i" % l.id, content_type="application/json")
        self.assert_success(rv)

        response = rv.json
        response["title"] = "Super Great Location"
        rv = self.client.put(
            "/api/location/%i" % l.id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(user=u),
        )
        self.assert_success(rv)
        rv = self.client.get("/api/location/%i" % l.id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["title"], "Super Great Location")

        logs = self.session.query(ResourceChangeLog).all()
        self.assertIsNotNone(logs[-1].resource_id)
        self.assertIsNotNone(logs[-1].user_id)

        rv = self.client.get(
            "/api/resource/%i/change_log" % l.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[-1]["user_id"], u.id)

        rv = self.client.get(
            "/api/user/%i/resource_change_log" % u.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response[-1]["resource_id"], l.id)

    def test_geocode_setting(self):
        self.loader.load_partial_zip_codes()
        location = {"title": "Some super place", "description": "You should go here every day."}
        rv = self.client.post(
            "api/location",
            data=self.jsonify(location),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertIsNotNone(response["latitude"])
        self.assertIsNotNone(response["longitude"])
        location_id = response["id"]
        initial_lat_lng = str(response["latitude"]) + str(response["longitude"])

        # lat and lng shouldn't change on edit unless the street_address1 or zip fields are edited.
        response["description"] = "Something different"
        rv = self.client.put(
            "/api/location/%i" % location_id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        rv = self.client.get("/api/location/%i" % location_id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(initial_lat_lng, str(response["latitude"]) + str(response["longitude"]))

        response["zip"] = "24401"
        rv = self.client.put(
            "/api/location/%i" % location_id,
            data=self.jsonify(response),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        rv = self.client.get("/api/location/%i" % location_id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertNotEqual(initial_lat_lng, str(response["latitude"]) + str(response["longitude"]))
