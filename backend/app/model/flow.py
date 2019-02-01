from marshmallow import Schema, fields

#         "name": "contact",
#         "type": "identifying",
#         "status": "complete"
#         "date_completed": 2009-12-11h11:12:15
from app.question_service import QuestionService


class Step:

    def __init__(self, name, question_type, status, date_completed):
        self.name = name
        self.type = question_type
        self.status = status
        self.date_completed = date_completed


class Flow:

    steps = []

    def __init__(self, name):
        self.name = name

    def has_step(self, questionnaire_name):
        for q in self.steps:
            if q.name == questionnaire_name:
                return True
        return False

    def add_step(self, questionnaireName):
        q = QuestionService.get_class(questionnaireName)()
        step = Step(questionnaireName, q.__question_type__, "unknown", '')
        self.steps.append(step)


class StepSchema(Schema):
    name = fields.Str()
    type = fields.Str()
    status = fields.Str()
    date_completed = fields.Date()


class FlowSchema(Schema):
    name = fields.Str()
    steps = fields.Nested(StepSchema(), many=True)
