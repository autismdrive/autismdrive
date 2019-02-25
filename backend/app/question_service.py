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
    def get_meta_schema(name):
        module_name = QuestionService.QUESTION_PACKAGE + "." + name
        schema_name = QuestionService.camel_case_it(name) + "MetaSchema"
        return QuestionService.str_to_class(module_name, schema_name)()

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
    def get_meta(questionnaire, participant):
        meta = questionnaire.get_meta(participant);
        # loops through the depths, checks, and replaces ....
        return {"get_meta": meta};
