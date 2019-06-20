from flask_marshmallow import Schema
from marshmallow import post_load


class ExportInfo:
    table_name = ""
    class_name = ""
    size = 0
    url = ""
    question_type = ""

    def __init__(self, table_name, class_name, size=0, url="", question_type=""):
        self.table_name = table_name
        self.class_name = class_name
        self.size = size
        self.url = url
        self.question_type = question_type


class ExportInfoSchema(Schema):
    class Meta:
        ordered = True
        fields = ["table_name", "class_name", "size", "url", "question_type"]

    @post_load
    def make_info(self, data, **kwargs):
        return ExportInfo(**data)