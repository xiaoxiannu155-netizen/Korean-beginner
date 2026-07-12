import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.word import Word, WordProgress, WordExample
from app.models.user import User
from app.services.srs_service import calculate_next_review


async def get_words(
    db: AsyncSession,
    category: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Word], int]:
    stmt = select(Word)
    count_stmt = select(func.count(Word.id))
    if category:
        stmt = stmt.where(Word.category == category)
        count_stmt = count_stmt.where(Word.category == category)

    count_result = await db.execute(count_stmt)
    total = count_result.scalar()

    stmt = stmt.order_by(Word.difficulty_level).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    return list(result.scalars().all()), total


async def get_word_with_examples(db: AsyncSession, word_id: uuid.UUID) -> Word | None:
    result = await db.execute(
        select(Word)
        .where(Word.id == word_id)
        .options(selectinload(Word.examples))
    )
    return result.scalar_one_or_none()


async def get_or_create_word_progress(
    db: AsyncSession, user: User, word_id: uuid.UUID
) -> WordProgress:
    result = await db.execute(
        select(WordProgress).where(
            WordProgress.user_id == user.id,
            WordProgress.word_id == word_id,
        )
    )
    progress = result.scalar_one_or_none()
    if not progress:
        progress = WordProgress(user_id=user.id, word_id=word_id)
        db.add(progress)
        await db.flush()
    return progress


async def record_word_review(
    db: AsyncSession,
    user: User,
    word_id: uuid.UUID,
    is_correct: bool,
) -> WordProgress:
    progress = await get_or_create_word_progress(db, user, word_id)

    result = calculate_next_review(
        review_count=progress.review_count,
        is_correct=is_correct,
        consecutive_correct=progress.consecutive_correct,
    )

    progress.learned = True
    progress.review_count = result["review_count"]
    progress.srs_interval_days = result["srs_interval_days"]
    progress.next_review_at = result["next_review_at"]
    progress.consecutive_correct = result["consecutive_correct"]
    progress.learning_stage = result["learning_stage"]

    await db.commit()
    return progress
