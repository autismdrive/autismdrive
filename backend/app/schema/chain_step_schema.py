from app.model.chain_step import ChainStep
from app.schema.model_schema import ModelSchema


class ChainStepSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ChainStep
        fields = ["id", "name", "instruction", "last_updated"]
