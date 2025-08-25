from tests.base_test import BaseTest  # isort:skip
from sqlalchemy import Integer, cast, select

from app.models import Category
from tests.fixtures.fixture_utils import fake


class TestCategory(BaseTest):
    def test_category_basics(self):
        parent_cat = self.construct_category(name=fake.sentence())
        child_cat = self.construct_category(parent_id=parent_cat.id, name=fake.sentence())
        db_parent = self.session.query(Category).filter_by(id=parent_cat.id).first()
        db_child = self.session.query(Category).filter_by(id=child_cat.id).first()
        self.assertIsNotNone(db_parent)
        self.assertIsNotNone(db_child)
        self.assertEqual(db_parent.name, parent_cat.name)
        self.assertEqual(db_child.name, child_cat.name)
        self.assertEqual(db_child.parent.name, parent_cat.name)
        rv = self.client.get("/api/category/%i" % db_child.id, follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["id"], db_child.id)
        self.assertEqual(response["name"], child_cat.name)
        self.assertEqual(response["parent"]["name"], parent_cat.name)

    def test_modify_category_basics(self):
        parent_name_before = fake.sentence()
        parent_name_after = fake.sentence()
        parent_cat_1 = self.construct_category(name=parent_name_before)
        parent_cat_1_id = parent_cat_1.id
        parent_cat_2 = self.construct_category(name=parent_name_after)
        parent_cat_2_id = parent_cat_2.id

        child_name_before = fake.sentence()
        child_name_after = fake.sentence()
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
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv2)

        rv3 = self.client.get("/api/category/%i" % child_cat_id, content_type="application/json")
        self.assert_success(rv3)
        rv3_dict = rv3.json
        self.assertEqual(rv3_dict["name"], child_name_after)
        self.assertEqual(rv3_dict["parent"]["name"], parent_name_after)

    def test_delete_category(self):
        num_cats_before = self.session.query(Category).count()
        self.construct_category(fake.sentence())
        self.construct_category(fake.sentence())
        c = self.construct_category(fake.sentence())
        c_id = c.id
        rv = self.client.get("api/category/%i" % c_id, content_type="application/json")
        self.assert_success(rv)
        rv = self.client.get("api/category", content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(num_cats_before + 3, len(response))

        rv = self.client.delete(
            "api/category/%i" % c_id, content_type="application/json", headers=self.default_logged_in_headers
        )
        self.assert_success(rv)

        rv = self.client.get("api/category/%i" % c_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)
        rv = self.client.get("api/category", content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(num_cats_before + 2, len(response))

    def test_delete_category_will_not_delete_descendants(self):
        num_cats_before = self.session.query(Category).count()
        num_root_cats_before = self.session.query(Category).filter(Category.parent_id.is_(None)).count()
        cat1 = self.construct_category(name=fake.sentence())
        cat1_id = cat1.id
        cat2 = self.construct_category(name=fake.sentence(), parent_id=cat1_id)
        cat2_id = cat2.id
        self.construct_category(name=fake.sentence(), parent_id=cat1_id)
        self.construct_category(name=fake.sentence(), parent_id=cat2_id)
        self.construct_category(name=fake.sentence(), parent_id=cat2_id)

        rv = self.client.get("api/category/root", content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(num_root_cats_before + 1, len(response))

        # Get the root category matching cat1
        root_cat1 = next((cat for cat in response if cat["id"] == cat1_id), None)
        self.assertIsNotNone(root_cat1)
        self.assertEqual(2, len(root_cat1["children"]))

        rv = self.client.get("api/category", content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(num_cats_before + 5, len(response))

        rv = self.client.delete(
            "api/category/%i" % cat1.id, content_type="application/json", headers=self.default_logged_in_headers
        )
        self.assertEqual(400, rv.status_code)
        response = rv.json
        self.assertIsNotNone(response)
        self.assertEqual("can_not_delete", response["code"])
        self.assertEqual("You must delete all dependent records first.", response["message"])

    def test_create_category(self):
        category = {"name": fake.sentence()}
        rv = self.client.post(
            "api/category",
            data=self.jsonify(category),
            content_type="application/json",
            follow_redirects=True,
            headers=self.default_logged_in_headers,
        )
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["name"], category["name"])
        self.assertIsNotNone(response["id"])

    def test_category_has_links(self):
        c = self.construct_category(name=fake.sentence())
        rv = self.client.get("/api/category/" + str(c.id), follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["_links"]["self"], "/api/category/" + str(c.id))
        self.assertEqual(response["_links"]["collection"], "/api/category")

    def test_category_has_children(self):
        c1 = self.construct_category(name=fake.sentence())
        c1_id = c1.id
        c2 = self.construct_category(name=fake.sentence(), parent_id=c1_id)
        c2_id = c2.id
        rv = self.client.get("/api/category/" + str(c1_id), follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["children"][0]["id"], c2_id)
        self.assertEqual(response["children"][0]["name"], c2.name)

    def test_category_has_parents_and_that_parent_has_no_children(self):
        c1 = self.construct_category(name=fake.sentence())
        c2 = self.construct_category(name=fake.sentence(), parent_id=c1.id)
        c3 = self.construct_category(name=fake.sentence(), parent_id=c2.id)
        rv = self.client.get("/api/category/" + str(c3.id), follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["parent"]["id"], c2.id)
        self.assertNotIn("children", response["parent"])

    def test_category_can_create_searchable_path(self):
        c1 = self.construct_category(name=fake.sentence())
        c2 = self.construct_category(name=fake.sentence(), parent_id=c1.id)
        c3 = self.construct_category(name=fake.sentence(), parent_id=c2.id)

        from app.utils.category_utils import CategoryTreeMapperSingleton

        ctm = CategoryTreeMapperSingleton()

        c1_path = str(c1.id)
        c2_path = str(c1.id) + "," + str(c2.id)
        c3_path = str(c1.id) + "," + str(c2.id) + "," + str(c3.id)

        db_c1 = self.session.execute(select(Category).where(Category.id == c1.id)).unique().scalar_one()
        db_c2 = self.session.execute(select(Category).where(Category.id == c2.id)).unique().scalar_one()
        db_c3 = self.session.execute(select(Category).where(Category.id == c3.id)).unique().scalar_one()

        self.assertEqual(1, len(ctm.get_all_search_paths(db_c1.id)))
        self.assertEqual(2, len(ctm.get_all_search_paths(db_c2.id)))
        self.assertEqual(3, len(ctm.get_all_search_paths(db_c3.id)))

        self.assertIn(c3_path, ctm.get_all_search_paths(db_c3.id))
        self.assertIn(c2_path, ctm.get_all_search_paths(db_c3.id))
        self.assertIn(c1_path, ctm.get_all_search_paths(db_c3.id))
        self.assertIn(c2_path, ctm.get_all_search_paths(db_c2.id))
        self.assertIn(c1_path, ctm.get_all_search_paths(db_c2.id))
        self.assertIn(c1_path, ctm.get_all_search_paths(db_c1.id))

    def test_category_in_search_schema_has_no_child_joins(self):
        """
        The Category endpoint should return a flat list (i.e.,
        without the hierarchical "children" joins) of categories
        to optimize performance when populating dropdowns in the
        search UI.
        """
        num_cats_before = self.session.query(Category).count()

        # Construct 4 categories in the following hierarchy:
        # c1 (level 0)
        #  └─ c2 (level 1)
        #      └─ c3 (level 2)
        #          └─ c4 (level 3)
        c1 = self.construct_category(name=fake.sentence())
        c2 = self.construct_category(name=fake.sentence(), parent_id=c1.id)
        c3 = self.construct_category(name=fake.sentence(), parent_id=c2.id)
        self.construct_category(name=fake.sentence(), parent_id=c3.id)

        rv = self.client.get("/api/category", follow_redirects=True, content_type="application/json")

        self.assert_success(rv)
        response = rv.json

        # The Category endpoint should return a flat list of Categories,
        # without the hierarchical "children" joins, to optimize performance.
        self.assertEqual(num_cats_before + 4, len(response))

        for cat in response:
            self.assertNotIn("children", cat)
