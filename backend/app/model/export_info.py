import re

from flask_marshmallow import Schema
from marshmallow import post_load, fields, EXCLUDE

from app import ma


class ExportInfo:
    table_name = ""
    class_name = ""
    size = 0
    url = ""
    question_type = ""
    exportable = True
    json_data = {}
    display_name = ""
    sub_tables = []

    def __init__(self, table_name, class_name, size=0, url="", question_type="", export=True):
        self.table_name = table_name
        self.class_name = class_name
        self.size = size
        self.url = url
        self.question_type = question_type
        self.export = export
        self.display_name = self.pretty_title_from_snakecase(class_name)
        self.sub_tables = []

    def pretty_title_from_snakecase(self, title):
        # Capitalizes, removes '_', drops 'Questionnaire' and limits to 30 chars.
        title = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', title)
        title = re.sub('([a-z0-9])([A-Z])', r'\1 \2', title)
        return title.replace("Questionnaire", "").strip()[:30]


class ExportInfoSchema(Schema):
    class Meta:
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        include_fk = True
        ordered = True
        fields = ["table_name", "class_name", "display_name", "size", "url", "question_type", "sub_tables"]

    sub_tables = ma.Nested(lambda: ExportInfoSchema(), default=None, many=True, dump_only=True)
    display_name = fields.String(dump_only=True)

    @post_load
    def make_info(self, data, **kwargs):
        return ExportInfo(**data)
