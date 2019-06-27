
import requests
from apscheduler.schedulers.background import BackgroundScheduler


# Fire of the scheduler
# The Data Importer should run on the SLAVE, and will make calls to the master to download
# data, store it locally, and remove it from the master when necessary.
from flask import json
from sqlalchemy import exc

from app.export_service import ExportService
from app.model.export_info import ExportInfoSchema
from app.resources.schema import UserSchema


class DataImporter:

    LOGIN_ENDPOINT = "/api/login_password"
    EXPORT_ENDPOINT = "/api/export"
    token = "invalid"

    def __init__(self, app, db):
        scheduler = BackgroundScheduler()
        scheduler.start()
        job2 = scheduler.add_job(self.get_questionnaires, 'interval', seconds=5)
        self.master_url = app.config["MASTER_URL"]
        self.db = db
        self.logger = app.logger
        self.email = app.config["MASTER_EMAIL"]
        self.password = app.config["MASTER_PASS"]

    def login(self):
        creds = {'email': self.email, 'password': self.password}
        response = requests.post(self.master_url + self.LOGIN_ENDPOINT, json=creds)
        if response.status_code != 200:
            self.logger.error("Authentication to Primary Server Failed." + str(response))
        else:
            data = response.json()
            self.token = data['token']

    def get_headers(self):
        # Verifies we still have a valid token, and returns the headers
        # or attempts to re-authenticate.
        headers = {'Authorization': 'Bearer {}'.format(self.token),
                   'Accept': "application/json"}
        response = requests.get(self.master_url + self.USER_ENDPOINT, headers=headers)
        if response.status_code != 200:
            self.login()
            headers = {'Authorization': 'Bearer {}'.format(self.token)}
        return headers

    def load_data(self):
        response = requests.get(self.master_url + self.EXPORT_ENDPOINT, headers=self.get_headers())
        exportables = ExportInfoSchema().load(response.json())
        return exportables

    def load_data(self):
        all_data = {}
        exports = ExportService.get_export_info()
        for export in exports:
            rv = self.app.get(export.url, follow_redirects=True, content_type="application/json",
                              headers=self.logged_in_headers())
            all_data[export.class_name] = json.loads(rv.get_data(as_text=True))
        return all_data

    # Takes the partial path of an endpoint, and returns json.  Logging any errors.
    def __get_json(self, path):
        try:
            url = self.master_url + path;
            response = requests.get(url)
            return response.json()
        except requests.exceptions.ConnectionError as err:
            self.logger.error("Uable to contact the master instance at " + url)

    def get_users(self):
        data = self.__get_json(self.USER_ENDPOINT)
        schema = UserSchema()
        for record in data:
            updated, errors = schema.load(data)
            self.db.session.merge(updated)
        self.db.session.commit

    # Now get a list of the questionnaires to pull back.
    def get_questionnaires(self):
        data = self.__get_json(self.QUESTION_ENDPOINT)
        for q in data:
            meta_data = self.get_metadata(question_name=q)
            self.pull_data_for_question(question_name=q, meta_data=meta_data)

    def get_metadata(self, question_name):
        return self.__get_json(self.QUESTION_ENDPOINT + "/" + question_name + "/meta")

    def pull_data_for_question(self, question_name, meta_data):
        data = self.__get_json(self.QUESTION_ENDPOINT + "/" + question_name + "/export")
        class_ref = ExportService.get_class(question_name)
        schema = ExportService.get_schema(question_name, session=self.db.session)
        for record in data:
            self.save_data(question_name, record)

    def save_data(self, name, data):
        try: # Attempt to update existing data record
            instance = self.db.session.query(class_ref).filter(class_ref.id == data['id']).first()
            updated, errors = schema.load(data, instance=instance)
        except exc.IntegrityError as ie: # If this fails, create a new record
            self.db.session.rollback()
            updated, errors = schema.load(data)
        if errors:
            raise Exception("Failed to save record.", details=errors)
        self.db.session.merge(updated)
        self.db.session.commit()

