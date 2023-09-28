from marshmallow.utils import EXCLUDE

from app.schema.ma import ma


class ModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        include_fk = True
        ordered = True
