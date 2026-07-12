import uuid
from datetime import datetime

from sqlalchemy import String, Integer, Boolean, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Letter(Base):
    __tablename__ = "letters"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    char: Mapped[str] = mapped_column(String(10), nullable=False)
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    romanization: Mapped[str | None] = mapped_column(String(20))
    chinese_hint: Mapped[str | None] = mapped_column(Text)
    pronunciation_audio_url: Mapped[str | None] = mapped_column(Text)
    stroke_animation_url: Mapped[str | None] = mapped_column(Text)
    mouth_shape_url: Mapped[str | None] = mapped_column(Text)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    pronunciation_tip: Mapped[str | None] = mapped_column(Text, nullable=True)


class LetterProgress(Base):
    __tablename__ = "letter_progress"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    letter_id: Mapped[str] = mapped_column(String(10), nullable=False)
    letter_type: Mapped[str | None] = mapped_column(String(20))
    mastered: Mapped[bool] = mapped_column(Boolean, default=False)
    practice_count: Mapped[int] = mapped_column(Integer, default=0)
    best_score: Mapped[float | None] = mapped_column(Float)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
