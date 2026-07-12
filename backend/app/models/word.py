import uuid
from datetime import datetime, date

from sqlalchemy import String, Integer, Boolean, DateTime, Date, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Word(Base):
    __tablename__ = "words"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    korean: Mapped[str] = mapped_column(String(100), nullable=False)
    chinese: Mapped[str | None] = mapped_column(String(200))
    romanization: Mapped[str | None] = mapped_column(String(200))
    pronunciation_audio_url: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(50))
    sub_category: Mapped[str | None] = mapped_column(String(50))
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1)

    examples: Mapped[list["WordExample"]] = relationship(back_populates="word")


class WordExample(Base):
    __tablename__ = "word_examples"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    word_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("words.id"), nullable=True
    )
    korean_sentence: Mapped[str] = mapped_column(Text, nullable=False)
    chinese_translation: Mapped[str | None] = mapped_column(Text)
    source_type: Mapped[str | None] = mapped_column(String(30))
    source_name: Mapped[str | None] = mapped_column(String(200))
    source_date: Mapped[date | None] = mapped_column(Date)
    pronunciation_audio_url: Mapped[str | None] = mapped_column(Text)

    word: Mapped["Word | None"] = relationship(back_populates="examples")


class WordProgress(Base):
    __tablename__ = "word_progress"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    word_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("words.id"), nullable=False
    )
    learned: Mapped[bool] = mapped_column(Boolean, default=False)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    last_review_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    next_review_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    srs_interval_days: Mapped[int] = mapped_column(Integer, default=0)
    consecutive_correct: Mapped[int] = mapped_column(Integer, default=0)
    learning_stage: Mapped[str] = mapped_column(String(10), default="new")
