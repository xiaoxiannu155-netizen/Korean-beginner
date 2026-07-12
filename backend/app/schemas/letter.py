from pydantic import BaseModel


class LetterRead(BaseModel):
    id: str
    char: str
    type: str
    romanization: str | None
    chinese_hint: str | None
    pronunciation_audio_url: str | None
    stroke_animation_url: str | None
    mouth_shape_url: str | None
    order_index: int
    pronunciation_tip: str | None

    model_config = {"from_attributes": True}


class LetterPracticeSubmit(BaseModel):
    score: float  # 0-100
    mastered: bool = False


class LetterProgressRead(BaseModel):
    letter_id: str
    mastered: bool
    practice_count: int
    best_score: float | None

    model_config = {"from_attributes": True}
