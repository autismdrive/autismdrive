
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
    USER_ENDPOINT = "/api/session"
    token = "invalid"

    def __init__(self, app, db):
        self.master_url = app.config["MASTER_URL"]
        self.app = app
        self.db = db
        self.logger = app.logger
        self.email = app.config["MASTER_EMAIL"]
        self.password = app.config["MASTER_PASS"]

    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.start()
        job2 = scheduler.add_job(self.get_questionnaires, 'interval', seconds=5)

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

    def get_export_list(self):
        response = requests.get(self.master_url + self.EXPORT_ENDPOINT, headers=self.get_headers())
        exportables = ExportInfoSchema(many=True).load(response.json()).data
        return exportables

    def request_data(self):
        all_data = {}
        exports = self.get_export_list()
        for export in exports:
            if export.size == 0:
                continue
            response = requests.get(export.url, headers=self.get_headers())
            all_data[export.class_name] = response.json()
        return all_data

    # Takes the partial path of an endpoint, and returns json.  Logging any errors.
    def __get_json(self, path):
        try:
            url = self.master_url + path;
            response = requests.get(url)
            return response.json()
        except requests.exceptions.ConnectionError as err:
            self.logger.error("Uable to contact the master instance at " + url)
