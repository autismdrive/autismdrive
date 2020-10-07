import datetime
import importlib
import re
import logging

from dateutil.tz import UTC
from flask import url_for
from sqlalchemy import func, desc

from app import db, EmailService, app
from app.model.data_transfer_log import DataTransferLog
from app.model.export_info import ExportInfo


class ExportService:

    logger = logging.getLogger("ExportService")

    QUESTION_PACKAGE = "app.model.questionnaires"
    SCHEMA_PACKAGE = "app.schema.schema"
    EXPORT_SCHEMA_PACKAGE = "app.schema.export_schema"

    TYPE_SENSITIVE = 'sensitive'
    TYPE_IDENTIFYING = 'identifying'
    TYPE_UNRESTRICTED = 'unrestricted'
    TYPE_SUB_TABLE = 'sub-table'

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    @staticmethod
    def get_class_for_table(table):
        for c in db.Model._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == table.name:
                return c

    @staticmethod
    def get_class(class_name):
        # class_name = ExportService.camel_case_it(name)
        for c in db.Model._decl_class_registry.values():
            if hasattr(c, '__name__') and c.__name__ == class_name:
                return c

    @staticmethod
    def get_schema(name, many=False, session=None, is_import=False):
        model = ExportService.get_class(name)
        class_name = model.__name__
        schema_name = ''
        schema_class = None

        if not is_import:
            # Check for an 'ExportSchema'
            schema_name = class_name + "ExportSchema"
            schema_class = ExportService.str_to_class(ExportService.EXPORT_SCHEMA_PACKAGE, schema_name)

        # If that doesn't work, then look in the resources schema file.
        if schema_class is None:
            schema_name = class_name + "Schema"
            schema_class = ExportService.str_to_class(ExportService.SCHEMA_PACKAGE, schema_name)

        # If that doesn't work, check for a general schema in the class itself.
        if schema_class is None:
            schema_name = class_name + "Schema"
            schema_class = ExportService.str_to_class(model.__module__, schema_name)

        if schema_class is None:
            raise Exception("Unable to locate schema for class " + class_name)

        return schema_class(many=many, session=session)

    @staticmethod
    def camel_case_it(name):
        first, *rest = name.split('_')
        return first.capitalize() + ''.join(word.capitalize() for word in rest)

    @staticmethod
    def snake_case_it(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def get_data(name, user_id=None, last_updated=None):
        model = ExportService.get_class(name)
        query = db.session.query(model)
        if last_updated:
            query = query.filter(model.last_updated > last_updated)
        if hasattr(model, '__mapper_args__') \
                and 'polymorphic_identity' in model.__mapper_args__:
            query = query.filter(model.type == model.__mapper_args__['polymorphic_identity'])
        query = query.order_by(model.id)
        if user_id:
            if hasattr(model, 'user_id'):
                return query.filter(model.user_id == user_id)
            else:
                return []
        else:
            return query.all()

    # Returns a list of classes/tables with information about how they should be exported.
    @staticmethod
    def get_table_info(last_updated=None):
        export_infos = []
        sorted_tables = db.metadata.sorted_tables  # Tables in an order that should correctly manage dependencies

        # This moves the resource_categories table to the end of the list.
        rc = next((t for t in sorted_tables if t.fullname == "resource_category"), None)
        sorted_tables.append(sorted_tables.pop(sorted_tables.index(rc)))

        for table in sorted_tables:
            db_model = ExportService.get_class_for_table(table)
            export_infos.append(ExportService.get_single_table_info(db_model, last_updated))
        return export_infos

    @staticmethod
    def get_single_table_info(db_model, last_updated):
        export_info = ExportInfo(table_name=db_model.__tablename__, class_name=db_model.__name__)
        query = (db.session.query(func.count(db_model.id)))
        if last_updated:
            query = query.filter(db_model.last_updated > last_updated)
        if hasattr(db_model, '__mapper_args__') \
                and 'polymorphic_identity' in db_model.__mapper_args__:
            query = query.filter(db_model.type == db_model.__mapper_args__['polymorphic_identity'])

        export_info.size = query.all()[0][0]
        export_info.url = url_for("api.exportendpoint", name=ExportService.snake_case_it(db_model.__name__))
        if hasattr(db_model, '__question_type__'):
            export_info.question_type = db_model.__question_type__
        # Do not include sub-tables that will fall through from quiestionnaire schemas,
        # or logs that don't make sense to export.
        if hasattr(db_model, '__no_export__') and db_model.__no_export__:
            export_info.exportable = False

        if hasattr(db_model, "get_field_groups"):
            groups = db_model().get_field_groups()
            for name, settings in groups.items():
                if "repeat_class" in settings:
                    # RECURSE!
                    c = settings["repeat_class"]
                    export_info.sub_tables.append(ExportService.get_single_table_info(c, last_updated))

        return export_info

    @staticmethod
    def class_exists(module_name, class_name):
        try:
            module_ = importlib.import_module(module_name)
            try:
                return getattr(module_, class_name)
            except AttributeError:
                return None
        except ImportError:
            return None

    # Given a string, creates an instance of that class
    @staticmethod
    def str_to_class(module_name, class_name):
        return ExportService.class_exists(module_name, class_name)

    @staticmethod
    def get_meta(questionnaire, relationship):
        meta = {"table": {}}
        try:
            meta["table"]['question_type'] = questionnaire.__question_type__
            meta["table"]["label"] = questionnaire.__label__
        except:
            pass  # If these fields don't exist, just keep going.
        meta["fields"] = []

        groups = questionnaire.get_field_groups()
        if groups is None: groups = {}

        # This will move fields referenced by the field groups into the group, but will otherwise add them
        # the base meta object if they are not contained within a group.
        for c in questionnaire.__table__.columns:
            if c.info:
                c.info['name'] = c.name
                c.info['key'] = c.name
                added = False
                for group, values in groups.items():
                    if "fields" in values:
                        if c.name in values['fields']:
                            values['fields'].remove(c.name)
                            if 'fieldGroup' not in values: values['fieldGroup'] = []
                            values['fieldGroup'].append(c.info)
                            values['fieldGroup'] = sorted(values['fieldGroup'],
                                                          key=lambda field: field['display_order'])
                            added = True
                    # Sort the fields

                if not added:
                    meta['fields'].append(c.info)

        for group, values in groups.items():
            values['name'] = group
            #            if value['type'] == 'repeat':
            #                value['fieldArray'] = value.pop('fields')
            if "repeat_class" in values:
                values['key'] = group  # Only include the key on the group if an actual sub-class exists.
                values['fields'] = ExportService.get_meta(values["repeat_class"](), relationship)['fields']
                values.pop('repeat_class')

            if 'type' in values and values['type'] == 'repeat':
                values['fieldArray'] = {'fieldGroup': values.pop('fields')}
            meta['fields'].append(values)

        # Sort the fields
        meta['fields'] = sorted(meta['fields'], key=lambda field: field['display_order'])

        # loops through the depths, checks, and replaces ....
        meta_relationed = ExportService._recursive_relationship_changes(meta, relationship)
        return meta_relationed

    @staticmethod
    def _recursive_relationship_changes(meta, relationship):
        """
        This evil method recurses down through the metadata, removing items that have a
        RELATIONSHIP_REQUIRED, if the relationship isn't there and selecting the right
        content from a list, if RELATIONSHIP_SPECIFIC provides an array content for each
        possible type of relationship.
        """
        meta_copy = {}
        for k, v in meta.items():
            if type(v) is dict:
                if "RELATIONSHIP_SPECIFIC" in v:
                    if relationship.name in meta[k]['RELATIONSHIP_SPECIFIC']:
                        meta_copy[k] = meta[k]['RELATIONSHIP_SPECIFIC'][relationship.name]
                elif "RELATIONSHIP_REQUIRED" in v:
                    if relationship.name in meta[k]['RELATIONSHIP_REQUIRED']:
                        meta_copy[k] = ExportService._recursive_relationship_changes(v, relationship)
                        # Otherwise, it should not be included in the copy.
                else:
                    meta_copy[k] = ExportService._recursive_relationship_changes(v, relationship)
            elif type(v) is list:
                meta_copy[k] = []
                for sv in v:
                    if type(sv) is dict:
                        if "RELATIONSHIP_REQUIRED" in sv and not relationship.name in sv['RELATIONSHIP_REQUIRED']:
                            # skip it.
                            pass
                        else:
                            meta_copy[k].append(ExportService._recursive_relationship_changes(sv, relationship))
                    else:
                        meta_copy[k].append(sv)
            else:
                meta_copy[k] = v
        return meta_copy

    @staticmethod
    def send_alert_if_exports_not_running():
        """
        If more than 30 minutes pass without an export from the Public Mirror to the Private Mirror, an email will be
        sent to an administrative email address. Emails to this address will occur every two (2) hours for the first
        24 hours and every four hours after that until the fault is corrected or the system taken down. After 24
        hours, the PI will also be emailed notifications every 8 hours until the fault is corrected or the system
        taken down.
        """
        alert_principal_investigator = False
        last_log = db.session.query(DataTransferLog).filter(DataTransferLog.type == 'export')\
            .order_by(desc(DataTransferLog.last_updated)).limit(1).first()
        if not last_log:
            # If the export logs are empty, create one with the current date.
            seed_log = DataTransferLog(total_records=0)
            db.session.add(seed_log)
            db.session.commit()
        else:
            msg = None
            subject = "Autism DRIVE: Error - "
            now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)  # Make date timezone aware
            time_difference = now - last_log.last_updated
            hours = int(time_difference.total_seconds()/3600)
            minutes = int(time_difference.total_seconds()/60)
            if hours >= 24 and hours% 4 == 0 and last_log.alerts_sent < (hours / 4 + 12):
                alert_principal_investigator = hours % 8 == 0
                subject = subject + str(hours) + " hours since last successful export"
                msg = "Exports should occur every 5 minutes.  It has been " + str(hours) + \
                    " hours since the last export was requested. This is the " + str(last_log.alerts_sent) + \
                    " email about this issue.  You will receive an email every 2 hours for the first " + \
                    "24 hours, and every 4 hours there-after."

            elif hours >= 2 and hours % 2 == 0 and hours / 2 >= last_log.alerts_sent:
                subject = subject + str(hours) + " hours since last successful export"
                msg = "Exports should occur every 5 minutes.  It has been " + str(hours) + \
                    " hours since the last export was requested. This is the " + str(last_log.alerts_sent) + \
                    " email about this issue.  You will receive an email every 2 hours for the first " \
                    "24 hours, and every 4 hours there-after."

            elif minutes >= 30 and last_log.alerts_sent == 0:
                subject = subject + str(minutes) + " minutes since last successful export"
                msg = "Exports should occur every 5 minutes.  It has been " + str(minutes) + \
                    " minutes since the last export was requested."
            if msg:
                email_server = EmailService(app)
                email_server.admin_alert_email(subject, msg,
                                               alert_principal_investigator=alert_principal_investigator)
                last_log.alerts_sent = last_log.alerts_sent + 1
                db.session.add(last_log)
                db.session.commit()


