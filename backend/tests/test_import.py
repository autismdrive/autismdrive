import unittest

from app import app, db
from app.data_importer import DataImporter
from tests.base_test_questionnaire import BaseTestQuestionnaire


class TestImportCase(BaseTestQuestionnaire, unittest.TestCase):

    def test_login(self):
        importer = DataImporter(app, db)
        data = importer.login()
        self.assertIsNotNone(data["token"])
