from marshmallow_sqlalchemy import ModelSchema


class ExportInfo:
    name = ""
    size = 0
    url = ""
    question_type = ""


class ExportInfoSchema(ModelSchema):
    class Meta:
        ordered = True
        fields = ["name", "size", "url", "question_type"]
