import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.letter import Letter, LetterProgress
from app.models.user import User


async def get_letters_by_type(db: AsyncSession, letter_type: str | None = None) -> list[Letter]:
    stmt = select(Letter).order_by(Letter.order_index)
    if letter_type:
        stmt = stmt.where(Letter.type == letter_type)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_letter(db: AsyncSession, letter_id: str) -> Letter | None:
    result = await db.execute(select(Letter).where(Letter.id == uuid.UUID(letter_id)))
    return result.scalar_one_or_none()


async def get_or_create_letter_progress(
    db: AsyncSession, user: User, letter_id: str
) -> LetterProgress:
    result = await db.execute(
        select(LetterProgress).where(
            LetterProgress.user_id == user.id,
            LetterProgress.letter_id == letter_id,
        )
    )
    progress = result.scalar_one_or_none()
    if not progress:
        progress = LetterProgress(user_id=user.id, letter_id=letter_id)
        db.add(progress)
        await db.flush()
    return progress


async def record_letter_practice(
    db: AsyncSession,
    user: User,
    letter_id: str,
    score: float,
    mastered: bool,
) -> LetterProgress:
    progress = await get_or_create_letter_progress(db, user, letter_id)
    progress.practice_count += 1
    if progress.best_score is None or score > progress.best_score:
        progress.best_score = score
    if mastered:
        progress.mastered = True
        progress.completed_at = datetime.now(timezone.utc)
    await db.commit()
    return progress
