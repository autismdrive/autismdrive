from app.model.category import Category
from tests.base_test import BaseTest


class TestCategory(BaseTest):
    def test_category_basics(self):
        parent_cat = self.construct_category(name="Mando")
        child_cat = self.construct_category(parent=parent_cat, name="Grogu")
        db_parent = self.session.query(Category).filter_by(id=parent_cat.id).first()
        db_child = self.session.query(Category).filter_by(id=child_cat.id).first()
        self.assertIsNotNone(db_parent)
        self.assertIsNotNone(db_child)
        self.assertEqual(db_parent.name, "Mando")
        self.assertEqual(db_child.name, "Grogu")
        self.assertEqual(db_child.parent.name, "Mando")
        rv = self.client.get("/api/category/%i" % db_child.id, follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], db_child.id)
        self.assertEqual(response["name"], "Grogu")
        self.assertEqual(response["parent"]["name"], "Mando")

    def test_modify_category_basics(self):
        parent_name_before = "Rhaegar Targaryen"
        parent_name_after = "Ned Stark"
        parent_cat_1 = self.construct_category(name=parent_name_before)
        parent_cat_2 = self.construct_category(name=parent_name_after)

        child_name_before = "Aegon Targaryen"
        child_name_after = "Jon Snow"
        child_cat = self.construct_category(name=child_name_before, parent=parent_cat_1)

        db_child = self.session.query(Category).filter_by(id=child_cat.id).first()
        self.assertIsNotNone(db_child)
        self.assertIsNotNone(db_child.name, child_name_before)
        self.assertEqual(db_child.parent.name, parent_name_before)

        rv = self.client.get("/api/category/%i" % child_cat.id, content_type="application/json")
        self.assert_success(rv)
        child_dict = rv.json
        child_dict["name"] = child_name_after
        child_dict["parent_id"] = parent_cat_2.id

        rv = self.client.put(
            "/api/category/%i" % child_cat.id,
            data=self.jsonify(child_dict),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)

        rv = self.client.get("/api/category/%i" % child_cat.id, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["name"], child_name_after)
        self.assertEqual(response["parent"]["name"], parent_name_after)

    def test_delete_category(self):
        self.construct_category(name="Unicorns")
        self.construct_category(name="Typewriters")
        c = self.construct_category(name="Pianos")
        c_id = c.id
        rv = self.client.get("api/category/%i" % c_id, content_type="application/json")
        self.assert_success(rv)
        rv = self.client.get("api/category", content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(3, len(response))

        rv = self.client.delete(
            "api/category/%i" % c_id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assert_success(rv)

        rv = self.client.get("api/category/%i" % c_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)
        rv = self.client.get("api/category", content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(2, len(response))

    def test_delete_category_will_not_delete_descendants(self):
        wool = self.construct_category(name="wool")
        yarn = self.construct_category(name="yarn", parent=wool)
        self.construct_category(name="roving", parent=wool)
        self.construct_category(name="worsted weight", parent=yarn)
        self.construct_category(name="sport weight", parent=yarn)

        rv = self.client.get("api/category/root", content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(1, len(response))
        self.assertEqual(2, len(response[0]["children"]))

        rv = self.client.get("api/category", content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(5, len(response))

        rv = self.client.delete(
            "api/category/%i" % wool.id, content_type="application/json", headers=self.logged_in_headers()
        )
        self.assertEqual(400, rv.status_code)
        response = rv.json
        self.assertIsNotNone(response)
        self.assertEqual("can_not_delete", response["code"])
        self.assertEqual("You must delete all dependent records first.", response["message"])

    def test_create_category(self):
        category = {"name": "My Favorite Things"}
        rv = self.client.post(
            "api/category",
            data=self.jsonify(category),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["name"], "My Favorite Things")
        self.assertIsNotNone(response["id"])

    def test_category_has_links(self):
        c = self.construct_category()
        rv = self.client.get("/api/category/" + str(c.id), follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["_links"]["self"], "/api/category/" + str(c.id))
        self.assertEqual(response["_links"]["collection"], "/api/category")

    def test_category_has_children(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent=c1)
        rv = self.client.get("/api/category/" + str(c1.id), follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["children"][0]["id"], c2.id)
        self.assertEqual(response["children"][0]["name"], "I'm the kid")

    def test_category_has_parents_and_that_parent_has_no_children(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent=c1)
        c3 = self.construct_category(name="I'm the grand kid", parent=c2)
        rv = self.client.get("/api/category/" + str(c3.id), follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["parent"]["id"], c2.id)
        self.assertNotIn("children", response["parent"])

    def test_category_can_create_searchable_path(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent=c1)
        c3 = self.construct_category(name="I'm the grand kid", parent=c2)

        c1_path = str(c1.id)
        c2_path = str(c1.id) + "," + str(c2.id)
        c3_path = str(c1.id) + "," + str(c2.id) + "," + str(c3.id)

        self.assertEqual(1, len(c1.all_search_paths()))
        self.assertEqual(2, len(c2.all_search_paths()))
        self.assertEqual(3, len(c3.all_search_paths()))

        self.assertIn(c3_path, c3.all_search_paths())
        self.assertIn(c2_path, c3.all_search_paths())
        self.assertIn(c1_path, c3.all_search_paths())
        self.assertIn(c2_path, c2.all_search_paths())
        self.assertIn(c1_path, c2.all_search_paths())
        self.assertIn(c1_path, c1.all_search_paths())

    # def test_category_depth_is_limited(self):
    #     c1 = self.construct_category()
    #     c2 = self.construct_category(
    #         name="I'm the kid", parent=c1)
    #     c3 = self.construct_category(
    #         name="I'm the grand kid",
    #         parent=c2)
    #     c4 = self.construct_category(
    #         name="I'm the great grand kid",
    #         parent=c3)
    #
    #     rv = self.app.get(
    #         '/api/category',
    #         follow_redirects=True,
    #         content_type="application/json")
    #
    #     self.assert_success(rv)
    #     response = rv.json
    #
    #     self.assertEqual(1, len(response))
    #     self.assertEqual(1, len(response[0]["children"]))
