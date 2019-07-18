import requests
from apscheduler.schedulers.background import BackgroundScheduler


# Fire of the scheduler
# The Data Importer should run on the MIRROR, and will make calls to the primary server to download
# data, store it locally, and remove it from the master when necessary.
from flask import logging
from sqlalchemy import desc

from app.export_service import ExportService
from app.model.export_info import ExportInfoSchema
from app.model.import_log import ImportLog
from app.schema.export_schema import AdminExportSchema


class ImportService:

    logger = logging.getLogger("ImportService")

    LOGIN_ENDPOINT = "/api/login_password"
    EXPORT_ENDPOINT = "/api/export"
    EXPORT_ADMIN_ENDPOINT = "/api/export/admin"
    USER_ENDPOINT = "/api/session"
    token = "invalid"

    def __init__(self, app, db):
        self.master_url = app.config["MASTER_URL"]
        self.app = app
        self.db = db
        self.email = app.config["MASTER_EMAIL"]
        self.password = app.config["MASTER_PASS"]

    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(self.run_backup, 'interval', seconds=5)

    def run_backup(self):
        exportables = self.get_export_list()
        data = self.request_data(exportables)
        self.load_all_data(data)
        self.load_admin()

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
            url = self.master_url + url
            print("Calling: " + url)
            response = requests.get(url, headers=self.get_headers())
            export.json_data = response.json()
        return export_list

    def load_all_data(self, export_list):
        for export_info in export_list:
            self.load_data(export_info)

    def load_data(self, export_info):
        if len(export_info.json_data) < 1:
            return  # Nothing to do here.
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
                        self.delete_record(item)
                except Exception as e:
                    self.db.session.rollback()
                    self.logger.error("Error processing " + export_info.class_name + " with id of " + str(item["id"]) + ".  Error: " + str(e))
                    log.handle_failure(e)
                    self.db.session.add(log)
                    raise e
            else:
                e = Exception("Failed to parse model " + export_info.class_name + ". " + str(errors))
                log.handle_failure(e)
                self.db.session.add(log)
                raise e
        self.db.session.add(log)
        self.db.session.commit()

    def delete_record(self, item):
        if not '_links' in item or not 'self' in item['_links']:
            raise Exception('No link available to delete ' + item.__class__.__name__)
        if not self.app.config['DELETE_RECORDS']:
            self.logger.info("DELETE is off in the configuration.  So not deleting.")
            return
        url = self.master_url + item['_links']['self']
        response = requests.delete(url, headers=self.get_headers())
        assert(response.status_code == 200)

    # Takes the partial path of an endpoint, and returns json.  Logging any errors.
    def __get_json(self, path):
        try:
            url = self.master_url + path
            response = requests.get(url)
            return response.json()
        except requests.exceptions.ConnectionError as err:
            self.logger.error("Uable to contact the master instance at " + url)

    def load_admin(self):
        url = self.master_url + self.EXPORT_ADMIN_ENDPOINT
        response = requests.get(url, headers=self.get_headers())
        schema = AdminExportSchema()
        json_response = response.json()
        for json_admin in json_response:
            password = str.encode(json_admin.pop('_password'))
            admin, errors = schema.load(json_admin, session=self.db.session)
            admin._password = password
            self.db.session.add(admin)
        self.db.session.commit()
