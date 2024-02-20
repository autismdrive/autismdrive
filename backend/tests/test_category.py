from sqlalchemy import cast, Integer, select

from app.models import Category
from tests.base_test import BaseTest


class TestCategory(BaseTest):
    def test_category_basics(self):
        parent_cat = self.construct_category(name="Mando")
        child_cat = self.construct_category(parent_id=parent_cat.id, name="Grogu")
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
        parent_cat_1_id = parent_cat_1.id
        parent_cat_2 = self.construct_category(name=parent_name_after)
        parent_cat_2_id = parent_cat_2.id

        child_name_before = "Aegon Targaryen"
        child_name_after = "Jon Snow"
        child_cat = self.construct_category(name=child_name_before, parent_id=parent_cat_1_id)
        child_cat_id = child_cat.id

        db_child = self.session.query(Category).filter_by(id=cast(child_cat_id, Integer)).first()
        self.assertIsNotNone(db_child)
        self.assertIsNotNone(db_child.name, child_name_before)
        self.assertEqual(db_child.parent.name, parent_name_before)

        rv1 = self.client.get("/api/category/%i" % child_cat_id, content_type="application/json")
        self.assert_success(rv1)
        child_dict = rv1.json.copy()
        child_dict["name"] = child_name_after
        child_dict["parent_id"] = parent_cat_2_id

        rv2 = self.client.put(
            "/api/category/%i" % child_cat_id,
            data=self.jsonify(child_dict),
            content_type="application/json",
            follow_redirects=True,
            headers=self.logged_in_headers(),
        )
        self.assert_success(rv2)

        rv3 = self.client.get("/api/category/%i" % child_cat_id, content_type="application/json")
        self.assert_success(rv3)
        rv3_dict = rv3.json
        self.assertEqual(rv3_dict["name"], child_name_after)
        self.assertEqual(rv3_dict["parent"]["name"], parent_name_after)

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
        wool_id = wool.id
        yarn = self.construct_category(name="yarn", parent_id=wool_id)
        yarn_id = yarn.id
        self.construct_category(name="roving", parent_id=wool_id)
        self.construct_category(name="worsted weight", parent_id=yarn_id)
        self.construct_category(name="sport weight", parent_id=yarn_id)

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
        c1_id = c1.id
        c2 = self.construct_category(name="I'm the kid", parent_id=c1_id)
        c2_id = c2.id
        rv = self.client.get("/api/category/" + str(c1_id), follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["children"][0]["id"], c2_id)
        self.assertEqual(response["children"][0]["name"], "I'm the kid")

    def test_category_has_parents_and_that_parent_has_no_children(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent_id=c1.id)
        c3 = self.construct_category(name="I'm the grand kid", parent_id=c2.id)
        rv = self.client.get("/api/category/" + str(c3.id), follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["parent"]["id"], c2.id)
        self.assertNotIn("children", response["parent"])

    def test_category_can_create_searchable_path(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent_id=c1.id)
        c3 = self.construct_category(name="I'm the grand kid", parent_id=c2.id)

        c1_path = str(c1.id)
        c2_path = str(c1.id) + "," + str(c2.id)
        c3_path = str(c1.id) + "," + str(c2.id) + "," + str(c3.id)

        db_c1 = self.session.execute(select(Category).where(Category.id == c1.id)).unique().scalar_one()
        db_c2 = self.session.execute(select(Category).where(Category.id == c2.id)).unique().scalar_one()
        db_c3 = self.session.execute(select(Category).where(Category.id == c3.id)).unique().scalar_one()

        self.assertEqual(1, len(db_c1.all_search_paths()))
        self.assertEqual(2, len(db_c2.all_search_paths()))
        self.assertEqual(3, len(db_c3.all_search_paths()))

        self.assertIn(c3_path, db_c3.all_search_paths())
        self.assertIn(c2_path, db_c3.all_search_paths())
        self.assertIn(c1_path, db_c3.all_search_paths())
        self.assertIn(c2_path, db_c2.all_search_paths())
        self.assertIn(c1_path, db_c2.all_search_paths())
        self.assertIn(c1_path, db_c1.all_search_paths())

    def test_parent_category_depth(self):
        c1 = self.construct_category()
        c2 = self.construct_category(name="I'm the kid", parent_id=c1.id)
        c3 = self.construct_category(name="I'm the grand kid", parent_id=c2.id)
        c4 = self.construct_category(name="I'm the great grand kid", parent_id=c3.id)

        rv = self.client.get("/api/category", follow_redirects=True, content_type="application/json")

        self.assert_success(rv)
        response = rv.json

        self.assertEqual(4, len(response))

        for cat in response:
            self.assertNotIn("children", cat)
