import datetime

import requests
from apscheduler.schedulers.background import BackgroundScheduler


# Fire of the scheduler
# The Data Importer should run on the SLAVE, and will make calls to the master to download
# data, store it locally, and remove it from the master when necessary.
from sqlalchemy import desc

from app.export_service import ExportService
from app.model.export_info import ExportInfoSchema
from app.model.import_log import ImportLog
from app.resources.ExportSchema import AdminExportSchema


class ImportService:

    LOGIN_ENDPOINT = "/api/login_password"
    EXPORT_ENDPOINT = "/api/export"
    EXPORT_ADMIN_ENDPOINT = "/api/export/admin"
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

    def request_data(self, export_list):
        for export in export_list:
            if export.size == 0:
                continue
            last_log = self.db.session.query(ImportLog).filter(ImportLog.class_name == export.class_name)\
                .order_by(desc(ImportLog.date_started)).limit(1).first()
            if last_log:
                date_string = last_log.date_started.strftime(ExportService.DATE_FORMAT)
                url = export.url + "?after=" + date_string
            else:
                url = export.url
            response = requests.get(url, headers=self.get_headers())
            export.json_data = response.json()
        return export_list

    def load_all_data(self, export_list):
        for export_info in export_list:
            self.load_data(export_info)

    def load_data(self, export_info):
        if len(export_info.json_data) < 1:
            return  # Nothing to do here.
        print("Loading " + str(len(export_info.json_data)) + " records into " + export_info.class_name + "")
        schema = ExportService.get_schema(export_info.class_name, many=False)
        model_class = ExportService.get_class(export_info.class_name)
        log = ImportLog(class_name=export_info.class_name, successful=True, success_count=0, failure_count=0)
        for item in export_info.json_data:
            item_copy = dict(item)
            if "_links" in item_copy:
                links = item_copy.pop("_links")
            existing_model = self.db.session.query(model_class).filter_by(id=item['id']).first()
            model, errors = schema.load(item_copy, session=self.db.session, instance=existing_model)
            if not errors:
                try:
                    self.db.session.add(model)
                    self.db.session.commit()
                    log.handle_success()
                    if hasattr(model, '__question_type__') and model.__question_type__ == ExportService.TYPE_SENSITIVE:
                        print("WE SHOULD CALL A DELETE ON THE MAIN SERVER HERE.")
                except Exception as e:
                    self.db.session.rollback()
                    log.handle_failure(e)
                    self.db.session.add(log)
                    raise e
            else:
                e = Exception(msg="Failed to parse model " + export_info.class_name)
                log.handle_failure(e)
                self.db.session.add(log)
                raise e
        self.db.session.add(log)
        self.db.session.commit()

    # Takes the partial path of an endpoint, and returns json.  Logging any errors.
    def __get_json(self, path):
        try:
            url = self.master_url + path;
            response = requests.get(url)
            return response.json()
        except requests.exceptions.ConnectionError as err:
            self.logger.error("Uable to contact the master instance at " + url)

    def load_admin(self):
        url = self.master_url + self.EXPORT_ADMIN_ENDPOINT
        response = requests.get(url).json()
        schema = AdminExportSchema(many=True)
        admin_users, errors = schema.load(response, session=self.db.session)
        for user in admin_users:
            user._password = str.encode(user._password)
            self.db.session.add(user)
        self.db.session.commit()
