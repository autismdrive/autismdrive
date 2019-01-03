import datetime

from app import db


class StarQuestionnaire():
    title: str
    description: str
    steps: List[StarStep]

class StarStep():
    title: str
    description: str
    fields: List[StarFieldAbstract]

    def update(self):
        for field in self.fields:
            # Store new value in database

class StarFieldAbstract():
    whatever: str

@StarFieldAbstract
class StarFieldGroup():
    title: str
    description: str
    fields: List[StarFieldAbstract]

@StarFieldAbstract
class StarField():
    prompt_text: str
    help_text: str
    placeholder_text: str
    field_type: str
    regex_pattern: str
    max_value: any
    min_value: any

@StarField
class StarFieldText():
    field_type: str

    def __init__(
        self,
        prompt_text=None,
        help_text=None,
        placeholder_text=None,
        regex_pattern=None,
        max_value=None,
        min_value=None
    ):
        self.prompt_text = prompt_text
        self.help_text = help_text
        self.placeholder_text = placeholder_text
        self.field_type = 'text'
        self.regex_pattern = regex_pattern
        self.max_value = max_value
        self.min_value = min_value

@StarField
class StarFieldSelect():
    options: List[str]

    def __init__(
        self,
        prompt_text=None,
        help_text=None,
        placeholder_text=None,
        regex_pattern=None,
        max_value=None,
        min_value=None,
        options=None
    ):
        self.field_type = 'select'
        self.prompt_text = prompt_text
        self.help_text = help_text
        self.placeholder_text = placeholder_text
        self.regex_pattern = regex_pattern
        self.max_value = max_value
        self.min_value = min_value
        self.options = options




