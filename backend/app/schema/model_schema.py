from marshmallow import EXCLUDE
from app import ma


class ModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        include_fk = True
        ordered = True
