import uuid
from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class BatchimRule(Base):
    __tablename__ = "batchim_rules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    rule_type: Mapped[str | None] = mapped_column(String(30))
    title: Mapped[str | None] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    animation_url: Mapped[str | None] = mapped_column(Text)
    order_index: Mapped[int | None] = mapped_column(Integer)

    examples: Mapped[list["BatchimExample"]] = relationship(back_populates="rule")


class BatchimExample(Base):
    __tablename__ = "batchim_examples"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("batchim_rules.id"), nullable=False
    )
    written_form: Mapped[str | None] = mapped_column(String(200))
    pronounced_form: Mapped[str | None] = mapped_column(String(200))
    process_description: Mapped[str | None] = mapped_column(Text)
    audio_url: Mapped[str | None] = mapped_column(Text)

    rule: Mapped["BatchimRule"] = relationship(back_populates="examples")
