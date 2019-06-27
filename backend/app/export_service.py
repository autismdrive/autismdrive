import datetime
import importlib
import re

from flask import url_for
from sqlalchemy import func

from app import db
from app.model.export_info import ExportInfo


class ExportService:

    QUESTION_PACKAGE = "app.model.questionnaires"
    SCHEMA_PACKAGE = "app.resources.schema"
    EXPORT_SCHEMA_PACKAGE = "app.resources.ExportSchema"

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
    def get_schema(name, many=False, session=None):
        model = ExportService.get_class(name)
        class_name = model.__name__

        # Check for an 'ExportSchema'
        schema_name = class_name + "ExportSchema"
        schema_class = ExportService.str_to_class(ExportService.EXPORT_SCHEMA_PACKAGE, schema_name)

        # If that doesn't work, then look in the resources schema file.
        if not schema_class:
            schema_name = class_name + "Schema"
            schema_class = ExportService.str_to_class(ExportService.SCHEMA_PACKAGE, schema_name)

        # If that doesn't work, check for a general schema in the class itself.
        if not schema_class:
            schema_name = class_name + "Schema"
            schema_class = ExportService.str_to_class(model.__module__, schema_name)

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
    def get_data(name, last_modifed_after = None):
        print("Exporting " + name)
        model = ExportService.get_class(name)
        query = db.session.query(model)
        if last_modifed_after:
            query = query.filter(model.last_updated > last_modifed_after)
        return query.all()

    @staticmethod
    def load_data(exportInfo, data):
        if len(data) < 1:
            return  # Nothing to do here.
        print("Loading " + exportInfo.class_name)
        schema = ExportService.get_schema(exportInfo.class_name, many=False)
        for item in data:
            item_copy = dict(item)
            links = item_copy.pop("_links")
            model, errors = schema.load(item_copy, session=db.session)
            if not errors:
                try:
                    db.session.add(model)
                    db.session.commit()
                    if hasattr(model, '__question_type__') and model.__question_type__ == ExportService.TYPE_SENSITIVE:
                        print("WE SHOULD CALL A DELETE ON THE MAIN SERVER HERE.")
                except Exception as e:
                    print("THERE WAS AN ERROR" + str(e))
            else:
                raise Exception("Failed!" + errors)
        models, errors = schema.load(data, session=db.session)
        db.session.add_all(models)

    # Returns a list of classes that can be exported from the system.
    @staticmethod
    def get_export_info():
        export_infos = []
        for table in db.metadata.sorted_tables:
            db_model = ExportService.get_class_for_table(table)

            # Never export Identifying information.
            if hasattr(db_model, '__question_type__') and db_model.__question_type__ == ExportService.TYPE_IDENTIFYING:
                continue
            # Do not include sub-tables that will fall through from quiestionnaire schemas
            if hasattr(db_model, '__question_type__') and db_model.__question_type__ == ExportService.TYPE_SUB_TABLE:
                continue

            export_info = ExportInfo(table_name=table.name, class_name= db_model.__name__)
            export_info.size=db.session.execute(db.select([func.count()]).select_from(table)).scalar(),
            export_info.url=url_for("api.exportendpoint", name=ExportService.snake_case_it(db_model.__name__))
            if hasattr(db_model, '__question_type__'):
                export_info.type = db_model.__question_type__
            export_infos.append(export_info)

        return export_infos

    @staticmethod
    def class_exists(module_name, class_name):
        try:
            module_ = importlib.import_module(module_name)
            try:
                return getattr(module_, class_name)
            except AttributeError:
                return False
        except ImportError:
            return False

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
                            if'fieldGroup' not in values: values['fieldGroup'] = []
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
    # this evil method recurses down through the metadata, removing items that have a
    # RELATIONSHIP_REQUIRED, if the relationship isn't there and selecting the right
    # content from a list, if RELATIONSHIP_SPECIFIC provides an array content for each
    # possible type of relationship.
    def _recursive_relationship_changes(meta, relationship):
        meta_copy = {}
        for k,v in meta.items():
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

