# Fire off the scheduler
# The Data Importer should run on the MIRROR, and will make calls to the primary server to download
# data, store it locally, and remove it from the master when necessary.
import datetime
import logging

import requests
from marshmallow import ValidationError
from sqlalchemy import desc, select
from sqlalchemy.orm import joinedload

from app.database import session, get_class
from app.export_service import ExportService
from app.log_service import LogService
from app.models import DataTransferLog, DataTransferLogDetail, ExportInfo
from app.rest_exception import RestException
from app.schemas import SchemaRegistry
from config.load import settings


class ImportService:
    logger = logging.getLogger("ImportService")

    LOGIN_ENDPOINT = "/api/login_password"
    EXPORT_ENDPOINT = "/api/export"
    EXPORT_ADMIN_ENDPOINT = "/api/export/admin"
    USER_ENDPOINT = "/api/session"
    token = "invalid"
    master_url = settings.MASTER_URL
    email = settings.MASTER_EMAIL
    password = settings.MASTER_PASS
    import_interval_minutes = settings.IMPORT_INTERVAL_MINUTES

    def run_backup(self, load_admin=True, full_backup=False):
        date_started = datetime.datetime.utcnow()
        exportables = self.get_export_list(full_backup)
        # Note:  We request data THEN create the next log.  We depend on this order to get data since
        # the last log was recorded, but be sure and set the start date from the moment this was called.
        data = self.request_data(exportables, full_backup=full_backup)
        log = self.log_for_export(exportables, date_started)
        session.add(log)
        self.load_all_data(data, log)
        if load_admin:
            self.load_admin()
        session.commit()

    def run_full_backup(self, load_admin=True):
        self.run_backup(load_admin=load_admin, full_backup=True)

    def log_for_export(self, exportables, date_started):
        total = 0
        for e in exportables:
            total += e.size
        if total > 0:
            log = DataTransferLog(type="importing", total_records=total)
        else:
            log = (
                session.execute(
                    select(DataTransferLog)
                    .options(joinedload(DataTransferLog.details))
                    .filter_by(type="importing")
                    .order_by(desc(DataTransferLog.last_updated))
                )
                .unique()
                .scalar_one()
            )
            log.last_updated = date_started
            session.close()
        return log

    def login(self):
        creds = {"email": self.email, "password": self.password}
        response = requests.post(self.master_url + self.LOGIN_ENDPOINT, json=creds)
        if response.status_code != 200:
            self.logger.error("Authentication to Primary Server Failed." + str(response))
        else:
            data = response.json()
            self.token = data["token"]

    def get_headers(self):
        # Verifies we still have a valid token, and returns the headers
        # or attempts to re-authenticate.
        headers = {"Authorization": "Bearer {}".format(self.token), "Accept": "application/json"}
        response = requests.get(self.master_url + self.USER_ENDPOINT, headers=headers)
        if response.status_code != 200:
            self.login()
            headers = {"Authorization": "Bearer {}".format(self.token)}
        return headers

    def get_export_list(self, full_backup=False) -> list[ExportInfo]:
        url = self.master_url + self.EXPORT_ENDPOINT
        last_log = (
            session.execute(
                select(DataTransferLog)
                .options(joinedload(DataTransferLog.details))
                .filter_by(type="importing")
                .order_by(desc(DataTransferLog.last_updated))
            )
            .unique()
            .scalar_one_or_none()
        )
        if last_log and last_log.successful() and not full_backup:
            date_string = last_log.date_started.strftime(ExportService.DATE_FORMAT)
            url += "?after=" + date_string

        session.close()
        response = requests.get(url, headers=self.get_headers())
        return SchemaRegistry.ExportInfoSchema().load(response.json(), many=True)

    def request_data(self, export_list, full_backup=False):
        for export in export_list:
            if export.size == 0:
                continue
            last_detail_log = (
                session.execute(
                    select(DataTransferLogDetail)
                    .filter(DataTransferLogDetail.class_name == export.class_name)
                    .order_by(desc(DataTransferLogDetail.date_started))
                )
                .unique()
                .scalar_one_or_none()
            )
            if last_detail_log and not full_backup:
                date_string = last_detail_log.date_started.strftime(ExportService.DATE_FORMAT)
                url = export.url + "?after=" + date_string
            else:
                url = export.url

            session.close()
            url = self.master_url + url
            print("Calling: " + url)
            response = requests.get(url, headers=self.get_headers())
            export.json_data = response.json()
        return export_list

    def load_all_data(self, export_list: list[ExportInfo], log):
        for export_info in export_list:
            self.load_data(export_info, log)

    def load_data(self, export_info: ExportInfo, log) -> int:
        num_items = 0

        if not (
            export_info
            and hasattr(export_info, "json_data")
            and export_info.json_data
            and len(export_info.json_data) > 0
        ):
            return num_items  # Nothing to do here.

        schema = ExportService.get_schema(export_info.class_name, many=False, is_import=True)
        model_class = get_class(export_info.class_name)
        log_detail = DataTransferLogDetail(
            class_name=export_info.class_name,
            date_started=log.date_started,
            successful=True,
            success_count=0,
            failure_count=0,
        )
        log.details.append(log_detail)

        for item in export_info.json_data:
            item_copy = dict(item)
            if "_links" in item_copy:
                links = item_copy.pop("_links")

            existing_model = session.query(model_class).filter_by(id=item["id"]).first()
            try:
                if existing_model:
                    model = schema.load(data=item_copy, session=session, instance=existing_model)
                else:
                    model = schema.load(data=item_copy, session=session)
            except Exception as e:
                e = Exception("Failed to parse model " + export_info.class_name + ". " + str(e))
                log_detail.handle_failure(e)
                session.add(log)
                session.add(log_detail)
                session.commit()
                session.close()
                raise e

            try:
                session.add(model)
                session.commit()
                log_detail.handle_success()
                num_items += 1
                session.add(log_detail)
                session.commit()

                if hasattr(model, "__question_type__") and model.__question_type__ == ExportService.TYPE_SENSITIVE:
                    print("Sensitive Data.  Calling Delete.")
                    self.delete_record(item)
            except Exception as e:
                session.rollback()
                self.logger.error(
                    "Error processing "
                    + export_info.class_name
                    + " with id of "
                    + str(item["id"])
                    + ".  Error: "
                    + str(e)
                )
                log_detail.handle_failure(e)
                session.add(log)
                session.add(log_detail)
                session.commit()
                session.close()
                raise e

        session.commit()
        session.close()
        return num_items

    def delete_record(self, item):
        if not "_links" in item or not "self" in item["_links"]:
            raise Exception("No link available to delete " + item.__class__.__name__)
        if not settings.DELETE_RECORDS:
            self.logger.info("DELETE is off in the configuration.  So not deleting.")
            return
        url = self.master_url + item["_links"]["self"]
        response = requests.delete(url, headers=self.get_headers())
        assert response.status_code == 200

    # Takes the partial path of an endpoint, and returns json.  Logging any errors.
    def __get_json(self, path):
        url = self.master_url + path
        try:
            response = requests.get(url)
            return response.json()
        except requests.exceptions.ConnectionError as err:
            self.logger.error("Unable to contact the master instance at " + url)

    def load_admin(self):
        url = self.master_url + self.EXPORT_ADMIN_ENDPOINT
        response = requests.get(url, headers=self.get_headers())
        schema = SchemaRegistry.AdminExportSchema()
        json_response = response.json()
        for json_admin in json_response:
            try:
                password = str.encode(json_admin.pop("_password"))
                admin = schema.load(json_admin, session=session)
                admin._password = password
                session.add(admin)
            except (ValidationError, RestException) as e:
                LogService.print(f"Failed to import admin user: {json_admin['id']}", e)
        session.commit()
