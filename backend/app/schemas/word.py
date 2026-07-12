from datetime import datetime, date
from pydantic import BaseModel
import uuid


class WordExampleRead(BaseModel):
    id: uuid.UUID
    korean_sentence: str
    chinese_translation: str | None
    source_type: str | None
    source_name: str | None
    pronunciation_audio_url: str | None

    model_config = {"from_attributes": True}


class WordRead(BaseModel):
    id: uuid.UUID
    korean: str
    chinese: str | None
    romanization: str | None
    pronunciation_audio_url: str | None
    category: str | None
    sub_category: str | None
    difficulty_level: int

    model_config = {"from_attributes": True}


class WordDetailRead(WordRead):
    examples: list[WordExampleRead] = []


class WordReviewSubmit(BaseModel):
    is_correct: bool


class WordProgressRead(BaseModel):
    word_id: uuid.UUID
    review_count: int
    srs_interval_days: int
    next_review_at: date | None
    learning_stage: str

    model_config = {"from_attributes": True}
