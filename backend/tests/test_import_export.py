import unittest

from flask import json

from app import db
from app.export_service import ExportService
from app.model.participant import Relationship, Participant
from app.model.questionnaires.identification_questionnaire import IdentificationQuestionnaire
from app.model.user import Role, User
from app.resources.schema import UserSchema, ParticipantSchema
from tests.base_test import clean_db
from tests.base_test_questionnaire import BaseTestQuestionnaire


class TestImportExportCase(BaseTestQuestionnaire, unittest.TestCase):

    def test_get_list_of_exportables_requires_admin(self):
        rv = self.app.get('/api/export')
        self.assertEquals(401, rv.status_code)

        headers = self.logged_in_headers(self.construct_user(email="joe@smoe.com", role=Role.user))
        rv = self.app.get('/api/export', headers=headers)
        self.assertEquals(403, rv.status_code)

    def test_get_list_of_exportables_contains_common_tables(self):
        rv = self.app.get('/api/export',
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertTrue(len(response) > 1)
        self.assertEqual(1, len(list(filter(lambda field: field['class_name'] == 'Category', response))))
        self.assertEqual(1, len(list(filter(lambda field: field['class_name'] == 'Participant', response))))
        self.assertEqual(1, len(list(filter(lambda field: field['class_name'] == 'User', response))))
        self.assertEqual(1, len(list(filter(lambda field: field['class_name'] == 'AssistiveDevice', response))))

    def test_get_list_of_exportables_has_basic_attributes(self):
        rv = self.app.get('/api/export', headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        user_data = list(filter(lambda field: field['class_name'] == 'User', response))
        self.assertTrue(len(user_data) > 0)
        self.assertEquals("/api/export/user", user_data[0]['url'])
        self.assertEquals("User", user_data[0]['class_name'])
        self.assertEquals("stardrive_user", user_data[0]['table_name'])

    def test_get_list_of_exportables_has_url_for_all_endpoints(self):
        rv = self.app.get('/api/export', headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        for entry in response:
            self.assertTrue('url' in entry, msg="No url provided for " + entry["class_name"])
            self.assertNotEqual("", entry['url'], msg="No url provided for " + entry["class_name"])

    def test_al_urls_respond_with_success(self):
        rv = self.app.get('/api/export',
                          follow_redirects=True,
                          content_type="application/json",
                          headers=self.logged_in_headers())
        self.assert_success(rv)
        exports = json.loads(rv.get_data(as_text=True))
        for export in exports:
            rv = self.app.get(export['url'],
                              follow_redirects=True,
                              content_type="application/json",
                              headers=self.logged_in_headers())
            self.assert_success(rv, msg="Failed to retrieve a list for " + export['class_name'])
            print("Successful export of " + export['class_name'])

    def test_user_has_no_identifying_information(self):
        rv = self.app.get('/api/export/User', headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertFalse("email" in response)
        print(response)

    def test_user_with_participant_properly_exported(self):
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        db.session.commit()
        rv = self.app.get('/api/export/user', headers=self.logged_in_headers())
        self.assert_success(rv)
        rv = self.app.get('/api/export/participant', headers=self.logged_in_headers())
        self.assert_success(rv)
        response = json.loads(rv.get_data(as_text=True))
        self.assertEqual(u.id, response[0]["user_id"])

    def get_export(self):
        """Grabs everything form the export, clears everything from the database, and imports
        all the information again, running it all through the API endpoints so it is fully serilaized """
        all_data = {}
        exports = ExportService.get_export_info()
        for export in exports:
            rv = self.app.get(export.url, follow_redirects=True, content_type="application/json",
                              headers=self.logged_in_headers())
            all_data[export.class_name] = json.loads(rv.get_data(as_text=True))
        return all_data

    def load_database(self, all_data):
        exports = ExportService.get_export_info()
        for export in exports:
            ExportService.load_data(export, all_data[export.class_name])

    def test_insert_user_with_participant(self):
        u = self.construct_user()
        u._password = b"xxxxx"
        orig_u_date = u.last_updated
        orig_user_dict = UserSchema().dump(u).data  # Use standard schema
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        orig_p_dict = ParticipantSchema().dump(p).data  # Use standard schema
        orig_p_date = p.last_updated
        db.session.commit()

        data = self.get_export()
        clean_db(db)
        db.session.commit()
        self.load_database(data)

        db_user = db.session.query(User).filter_by(id=orig_user_dict["id"]).first()
        self.assertIsNotNone(db_user, msg="User is recreated.")
        self.assertNotEqual(orig_user_dict["email"], db_user.email, msg="Email should be obfuscated")
        self.assertEqual(db_user.last_updated, orig_u_date, msg="Dates are kept in tact")
        self.assertEqual(db_user.role, u.role)
        self.assertEqual(db_user.email_verified, u.email_verified)
        self.assertEqual(db_user._password, u._password)

        db_par = db.session.query(Participant).filter_by(id=orig_p_dict["id"]).first()
        self.assertIsNotNone(db_par, msg="Participant is recreated.")
        self.assertEqual(db_par.user, db_user, msg="Relationship in tact")
        self.assertEqual(db_par.last_updated, orig_p_date, msg="Dates are kept in tact")

    def test_re_insert_user_with_modifications(self):
        # Construct the base user.
        u = self.construct_user()
        id = u.id
        db.session.commit()

        data = self.get_export()
        clean_db(db)
        db.session.commit()
        self.load_database(data)

        db_user = db.session.query(User).filter_by(id=id).first()
        self.assertFalse(db_user.email_verified, msg="Email should start off unverified")

        # Modify the exported data slightly, and reload
        data['User'][0]['email_verified'] = True
        self.load_database(data)
        db_user = db.session.query(User).filter_by(id=id).first()
        self.assertTrue(db_user.email_verified, msg="Email should now be verified.")

    def test_identifying_questinnaire_does_not_export(self):

        # Construct the base user.
        u = self.construct_user()
        p = self.construct_participant(user=u, relationship=Relationship.self_participant)
        iq = self.construct_identification_questionnaire(user=u, participant=p)
        id = u.id
        db.session.commit()

        data = self.get_export()
        clean_db(db)
        db.session.commit()
        self.load_database(data)

        self.assertEqual(ExportService.TYPE_IDENTIFYING,
                         IdentificationQuestionnaire().__question_type__)
        self.assertEqual(0, len(db.session.query(IdentificationQuestionnaire).all()),
                         msg="Identifying Questionnaires should not import.")

    def test_all_exports_have_links_to_self(self):
        self.construct_all_questionnaires()
        exports = ExportService.get_export_info()
        for export in exports:
            rv = self.app.get(export.url, follow_redirects=True, content_type="application/json",
                              headers=self.logged_in_headers())
            data = json.loads(rv.get_data(as_text=True))
            for d in data:
                self.assertTrue('_links' in d, msg="%s should have links in json." % export.class_name)
                self.assertTrue('self' in d['_links'])
                self.assert_success(self.app.get(d['_links']['self'], headers=self.logged_in_headers()))

    def test_sensitive_records_returned_can_be_deleted(self):
        self.construct_all_questionnaires()
        exports = ExportService.get_export_info()
        exports.reverse()  # Reverse the records
        for export in exports:
            rv = self.app.get(export.url, follow_redirects=True, content_type="application/json",
                              headers=self.logged_in_headers())
            data = json.loads(rv.get_data(as_text=True))
            for d in data:
                if export.question_type == ExportService.TYPE_SENSITIVE:
                    del_rv = self.app.delete(d['_links']['self'], headers=self.logged_in_headers())
                    self.assert_success(del_rv)