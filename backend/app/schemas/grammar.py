from pydantic import BaseModel
import uuid


class GrammarExampleRead(BaseModel):
    id: uuid.UUID
    korean_sentence: str | None
    chinese_translation: str | None
    is_wrong_example: bool

    model_config = {"from_attributes": True}


class GrammarRead(BaseModel):
    id: uuid.UUID
    title: str | None
    level: int | None
    structure_formula: str | None
    explanation: str | None
    usage_scenario: str | None
    order_index: int | None

    model_config = {"from_attributes": True}


class GrammarDetailRead(GrammarRead):
    examples: list[GrammarExampleRead] = []
