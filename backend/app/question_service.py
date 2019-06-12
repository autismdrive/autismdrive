import copy
import importlib
import re


class QuestionService:

    QUESTION_PACKAGE = "app.model.questionnaires"

    TYPE_SENSITIVE = 'sensitive'
    TYPE_IDENTIFYING = 'identifying'
    TYPE_UNRESTRICTED = 'unrestricted'

    @staticmethod
    def get_class(name):
        module_name = QuestionService.QUESTION_PACKAGE + "." + name
        class_name = QuestionService.camel_case_it(name)
        return QuestionService.str_to_class(module_name, class_name)

    @staticmethod
    def get_schema(name, many=False, session=None):
        module_name = QuestionService.QUESTION_PACKAGE + "." + name
        schema_name = QuestionService.camel_case_it(name) + "Schema"
        return QuestionService.str_to_class(module_name, schema_name)(many=many, session=session)

    @staticmethod
    def camel_case_it(name):
        first, *rest = name.split('_')
        return first.capitalize() + ''.join(word.capitalize() for word in rest)

    @staticmethod
    def snake_case_it(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    # Given a string, creates an instance of that class
    @staticmethod
    def str_to_class(module_name, class_name):
        try:
            module_ = importlib.import_module(module_name)
            try:
                return getattr(module_, class_name)
            except AttributeError:
                # FIXME: Get some damn logging.
                print("Error class does not exist:" + class_name)
                # logging.ERROR('Class does not exist')
        except ImportError:
            # FIXME: Get some damn logging.
            print("Module does not exist:" + module_name)
            #   logging.('Module does not exist')
        return None

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
                values['fields'] = QuestionService.get_meta(values["repeat_class"](), relationship)['fields']
                values.pop('repeat_class')

            if 'type' in values and values['type'] == 'repeat':
                values['fieldArray'] = {'fieldGroup': values.pop('fields')}
            meta['fields'].append(values)

        # Sort the fields
        meta['fields'] = sorted(meta['fields'], key=lambda field: field['display_order'])

        # loops through the depths, checks, and replaces ....
        meta_relationed = QuestionService._recursive_relationship_changes(meta, relationship)
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
                        meta_copy[k] = QuestionService._recursive_relationship_changes(v, relationship)
                        # Otherwise, it should not be included in the copy.
                else:
                    meta_copy[k] = QuestionService._recursive_relationship_changes(v, relationship)
            elif type(v) is list:
                meta_copy[k] = []
                for sv in v:
                    if type(sv) is dict:
                        if "RELATIONSHIP_REQUIRED" in sv and not relationship.name in sv['RELATIONSHIP_REQUIRED']:
                            # skip it.
                            pass
                        else:
                            meta_copy[k].append(QuestionService._recursive_relationship_changes(sv, relationship))
                    else:
                        meta_copy[k].append(sv)
            else:
                meta_copy[k] = v
        return meta_copy

