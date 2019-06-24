from app.export_service import ExportService


class Step:
    STATUS_COMPLETE = "COMPLETE"
    STATUS_INCOMPLETE = "INCOMPLETE"

    def __init__(self, name, question_type, label):
        self.name = name
        self.type = question_type
        self.label = label
        self.status = self.STATUS_INCOMPLETE
        self.date_completed = None
        self.questionnaire_id = None


class Flow:


    def __init__(self, name):
        self.name = name
        self.steps = []
        self.relationship = ""

    def has_step(self, questionnaire_name):
        for q in self.steps:
            if q.name == questionnaire_name:
                return True
        return False

    def update_step_progress(self, step_log):
        for step in self.steps:
            if step.name == step_log.questionnaire_name:
                step.status = step.STATUS_COMPLETE
                step.date_completed = step_log.date_completed
                step.questionnaire_id = step_log.questionnaire_id

    def add_step(self, questionnaireName):
        if not self.has_step(questionnaireName):
            q = ExportService.get_class(ExportService.camel_case_it(questionnaireName))()
            step = Step(questionnaireName, q.__question_type__, q.__label__)
            self.steps.append(step)
