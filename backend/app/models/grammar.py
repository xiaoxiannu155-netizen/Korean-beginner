import uuid
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class GrammarPoint(Base):
    __tablename__ = "grammar_points"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str | None] = mapped_column(String(200))
    level: Mapped[int | None] = mapped_column(Integer)
    structure_formula: Mapped[str | None] = mapped_column(Text)
    explanation: Mapped[str | None] = mapped_column(Text)
    usage_scenario: Mapped[str | None] = mapped_column(Text)
    order_index: Mapped[int | None] = mapped_column(Integer)

    examples: Mapped[list["GrammarExample"]] = relationship(back_populates="grammar")


class GrammarExample(Base):
    __tablename__ = "grammar_examples"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    grammar_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("grammar_points.id"), nullable=False
    )
    korean_sentence: Mapped[str | None] = mapped_column(Text)
    chinese_translation: Mapped[str | None] = mapped_column(Text)
    is_wrong_example: Mapped[bool] = mapped_column(Boolean, default=False)

    grammar: Mapped["GrammarPoint"] = relationship(back_populates="examples")
