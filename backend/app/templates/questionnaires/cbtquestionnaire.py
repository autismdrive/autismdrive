from app.model.questionnaire import StarQuestionnaire
from app.templates.steps.color_affect import ColorAffectCorrelation

@StarQuestionnaire
class CBTQuestionnaire():
    title = "Welcome to the CBT study"
    description = "This is a questionnaire for cognitive behavioral therapy (CBT)"
    steps = [
        ColorAffectCorrelation
    ]
