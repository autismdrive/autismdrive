import copy
import importlib


class QuestionService:

    QUESTION_PACKAGE = "app.model.questionnaires"

    TYPE_SENSITIVE = 'sensitive'
    TYPE_IDENTIFYING = 'identifying'
    TYPE_UNRESTRICTED = 'unrestricted'

    @staticmethod
    def get_class(name):
        module_name = QuestionService.QUESTION_PACKAGE + "." + name;
        class_name = QuestionService.camel_case_it(name)
        return QuestionService.str_to_class(module_name, class_name)

    @staticmethod
    def get_schema(name, many=False):
        module_name = QuestionService.QUESTION_PACKAGE + "." + name
        schema_name = QuestionService.camel_case_it(name) + "Schema"
        return QuestionService.str_to_class(module_name, schema_name)(many=many)

    @staticmethod
    def camel_case_it(name):
        first, *rest = name.split('_')
        return first.capitalize() + ''.join(word.capitalize() for word in rest)

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
        meta = questionnaire.get_meta()
        if not "table" in meta:
            meta["table"] = ""
        meta["table"]["type"] = questionnaire.__question_type__
        meta["table"]["label"] = questionnaire.__label__

        # loops through the depths, checks, and replaces ....
        meta_processed = QuestionService._recursive_relationship_changes(meta, relationship)
        return {"get_meta": meta_processed}

    @staticmethod
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
            else:
                meta_copy[k] = v
        return meta_copy

