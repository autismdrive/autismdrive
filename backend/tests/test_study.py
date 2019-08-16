import unittest
from flask import json
from tests.base_test import BaseTest
from app import db, elastic_index
from app.model.investigator import Investigator
from app.model.study import Study, Status
from app.model.study_category import StudyCategory


class TestStudy(BaseTest, unittest.TestCase):



    def test_study_basics(self):
        self.construct_study()
        s = db.session.query(Study).first()
        self.assertIsNotNone(s)
        s_id = s.id
        rv = self.app.get('/api/study/%i' % s_id,
                          follow_redirects=True,
                          content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], s_id)
        self.assertEqual(response["title"], 'Fantastic Study')
        self.assertEqual(response["description"], 'A study that will go down in history')

    def test_modify_study_basics(self):
        self.construct_study()
        s = db.session.query(Study).first()
        self.assertIsNotNone(s)
        s_id = s.id
        rv = self.app.get('/api/study/%i' % s_id, content_type="application/json")
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'Edwarardos Lemonade and Oil Change'
        response['description'] = 'Better fluids for you and your car.'
        response['benefit_description'] = 'Better fluids for you and your car, Duh.'
        response["short_title"] = 'Edwardos'
        response["short_description"] = 'Better fluids yada yada.'
        response["image_url"] = '/some/url'
        orig_date = response['last_updated']
        rv = self.app.put('/api/study/%i' % s_id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True)
        self.assert_success(rv)
        rv = self.app.get('/api/study/%i' % s_id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Edwarardos Lemonade and Oil Change')
        self.assertEqual(response['description'], 'Better fluids for you and your car.')
        self.assertEqual(response['benefit_description'], 'Better fluids for you and your car, Duh.')
        self.assertEqual(response["short_title"], 'Edwardos')
        self.assertEqual(response["short_description"], 'Better fluids yada yada.')
        self.assertEqual(response["image_url"], '/some/url')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_study(self):
        s = self.construct_study()
        s_id = s.id
        rv = self.app.get('api/study/%i' % s_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.delete('api/study/%i' % s_id, content_type="application/json")
        self.assert_success(rv)

        rv = self.app.get('api/study/%i' % s_id, content_type="application/json")
        self.assertEqual(404, rv.status_code)

    def test_create_study(self):
        o_id = self.construct_organization().id
        study = {'title': "Study of Studies", 'benefit_description': "This study will change your life.", 'organization_id': o_id}
        rv = self.app.post('api/study', data=json.dumps(study), content_type="application/json",
                           follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'Study of Studies')
        self.assertEqual(response['benefit_description'], 'This study will change your life.')
        self.assertIsNotNone(response['id'])

    def test_get_study_by_category(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        db.session.add(cs)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/study' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(s.id, response[0]["study_id"])
        self.assertEqual(s.description, response[0]["study"]["description"])

    def test_get_study_by_category_includes_category_details(self):
        c = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        cs2 = StudyCategory(study=s, category=c2)
        db.session.add_all([cs, cs2])
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i/study' % c.id,
            content_type="application/json",
            headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(s.id, response[0]["study_id"])
        self.assertEqual(2,
                         len(response[0]["study"]["study_categories"]))
        self.assertEqual(
            "c1", response[0]["study"]["study_categories"][0]["category"]
            ["name"])

    def test_category_study_count(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        db.session.add(cs)
        db.session.commit()
        rv = self.app.get(
            '/api/category/%i' % c.id, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, response["study_count"])

    def test_get_category_by_study(self):
        c = self.construct_category()
        s = self.construct_study()
        cs = StudyCategory(study=s, category=c)
        db.session.add(cs)
        db.session.commit()
        rv = self.app.get(
            '/api/study/%i/category' % s.id,
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))
        self.assertEqual(c.id, response[0]["id"])
        self.assertEqual(c.name, response[0]["category"]["name"])

    def test_add_category_to_study(self):
        c = self.construct_category()
        s = self.construct_study()

        sc_data = {"study_id": s.id, "category_id": c.id}

        rv = self.app.post(
            '/api/study_category',
            data=json.dumps(sc_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(c.id, response["category_id"])
        self.assertEqual(s.id, response["study_id"])

    def test_set_all_categories_on_study(self):
        c1 = self.construct_category(name="c1")
        c2 = self.construct_category(name="c2")
        c3 = self.construct_category(name="c3")
        s = self.construct_study()

        sc_data = [
            {
                "category_id": c1.id
            },
            {
                "category_id": c2.id
            },
            {
                "category_id": c3.id
            },
        ]
        rv = self.app.post(
            '/api/study/%i/category' % s.id,
            data=json.dumps(sc_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        sc_data = [{"category_id": c1.id}]
        rv = self.app.post(
            '/api/study/%i/category' % s.id,
            data=json.dumps(sc_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_category_from_study(self):
        self.test_add_category_to_study()
        rv = self.app.delete('/api/study_category/%i' % 1)
        self.assert_success(rv)
        rv = self.app.get(
            '/api/study/%i/category' % 1, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_add_investigator_to_study(self):
        i = self.construct_investigator()
        s = self.construct_study()

        si_data = {"study_id": s.id, "investigator_id": i.id}

        rv = self.app.post(
            '/api/study_investigator',
            data=json.dumps(si_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(i.id, response["investigator_id"])
        self.assertEqual(s.id, response["study_id"])

    def test_set_all_investigators_on_study(self):
        i1 = self.construct_investigator(name="person1")
        i2 = self.construct_investigator(name="person2")
        i3 = self.construct_investigator(name="person3")
        s = self.construct_study()

        si_data = [
            {"investigator_id": i1.id},
            {"investigator_id": i2.id},
            {"investigator_id": i3.id},
        ]
        rv = self.app.post(
            '/api/study/%i/investigator' % s.id,
            data=json.dumps(si_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(3, len(response))

        si_data = [{"investigator_id": i1.id}]
        rv = self.app.post(
            '/api/study/%i/investigator' % s.id,
            data=json.dumps(si_data),
            content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(1, len(response))

    def test_remove_investigator_from_study(self):
        self.test_add_investigator_to_study()
        rv = self.app.delete('/api/study_investigator/%i' % 1)
        self.assert_success(rv)
        rv = self.app.get(
            '/api/study/%i/investigator' % 1, content_type="application/json")
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(0, len(response))

    def test_investigator_basics(self):
        self.construct_investigator()
        i = db.session.query(Investigator).first()
        self.assertIsNotNone(i)
        i_id = i.id
        rv = self.app.get('/api/investigator/%i' % i_id,
                          follow_redirects=True,
                          content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response["id"], i_id)
        self.assertEqual(response["name"], i.name)

    def test_modify_investigator_basics(self):
        self.construct_investigator()
        i = db.session.query(Investigator).first()
        self.assertIsNotNone(i)

        rv = self.app.get('/api/investigator/%i' % i.id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        response['title'] = 'dungeon master'
        orig_date = response['last_updated']
        rv = self.app.put('/api/investigator/%i' % i.id, data=json.dumps(response), content_type="application/json",
                          follow_redirects=True, headers=self.logged_in_headers())
        self.assert_success(rv)

        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['title'], 'dungeon master')
        self.assertNotEqual(orig_date, response['last_updated'])

    def test_delete_investigator(self):
        i = self.construct_investigator()
        i_id = i.id

        rv = self.app.get('api/investigator/%i' % i_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.delete('api/investigator/%i' % i_id, content_type="application/json", headers=self.logged_in_headers())
        self.assert_success(rv)

        rv = self.app.get('api/investigator/%i' % i_id, content_type="application/json", headers=self.logged_in_headers())
        self.assertEqual(404, rv.status_code)

    def test_create_investigator(self):
        o_id = self.construct_organization().id
        investigator = {'name': "Tara Tarantula", 'title': "Assistant Professor of Arachnology", 'organization_id': o_id}
        rv = self.app.post('api/investigator', data=json.dumps(investigator), content_type="application/json",
                           headers=self.logged_in_headers(), follow_redirects=True)
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(response['name'], 'Tara Tarantula')
        self.assertEqual(response['title'], 'Assistant Professor of Arachnology')
        self.assertIsNotNone(response['id'])
