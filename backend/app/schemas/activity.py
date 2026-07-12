from pydantic import BaseModel


class DailyTaskRead(BaseModel):
    words_completed: int
    grammar_completed: bool
    listening_completed: bool
    speaking_completed: bool

    model_config = {"from_attributes": True}


class PersonalStatsRead(BaseModel):
    total_xp: int
    level: int
    streak_days: int
    today_words_learned: int
    stage: int
    completion_percentage: float  # 0.0 - 100.0
