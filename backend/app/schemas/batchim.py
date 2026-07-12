from pydantic import BaseModel
import uuid


class BatchimExampleRead(BaseModel):
    id: uuid.UUID
    written_form: str | None
    pronounced_form: str | None
    process_description: str | None
    audio_url: str | None

    model_config = {"from_attributes": True}


class BatchimRuleRead(BaseModel):
    id: uuid.UUID
    rule_type: str | None
    title: str | None
    description: str | None
    animation_url: str | None
    order_index: int | None

    model_config = {"from_attributes": True}


class BatchimRuleDetailRead(BatchimRuleRead):
    examples: list[BatchimExampleRead] = []
