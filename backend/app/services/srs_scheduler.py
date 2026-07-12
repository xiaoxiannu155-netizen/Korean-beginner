"""SRS review scheduler - finds words due for review"""
from datetime import date, datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, Integer

from app.models.user import User
from app.models.word import WordProgress, Word


async def get_due_reviews(db: AsyncSession, user: User, limit: int = 20) -> list[dict]:
    """Get words due for SRS review today"""
    today = date.today()
    result = await db.execute(
        select(WordProgress, Word)
        .join(Word, WordProgress.word_id == Word.id)
        .where(
            WordProgress.user_id == user.id,
            WordProgress.learned == True,
            WordProgress.next_review_at <= today,
            WordProgress.learning_stage != "mastered",
        )
        .order_by(WordProgress.next_review_at.asc())
        .limit(limit)
    )
    rows = result.all()
    return [
        {
            "word_id": str(row.WordProgress.word_id),
            "korean": row.Word.korean,
            "chinese": row.Word.chinese,
            "romanization": row.Word.romanization,
            "review_count": row.WordProgress.review_count,
            "srs_interval_days": row.WordProgress.srs_interval_days,
            "next_review_at": row.WordProgress.next_review_at.isoformat() if row.WordProgress.next_review_at else None,
            "learning_stage": row.WordProgress.learning_stage,
        }
        for row in rows
    ]


async def get_review_stats(db: AsyncSession, user: User) -> dict:
    """Get SRS review statistics"""
    result = await db.execute(
        select(
            func.count(WordProgress.id).label("total"),
            func.sum(case((WordProgress.learning_stage == "mastered", 1), else_=0)).label("mastered"),
        ).where(
            WordProgress.user_id == user.id,
            WordProgress.learned == True,
        )
    )
    row = result.one()
    total = row.total or 0
    mastered = row.mastered or 0

    # Due today
    today = date.today()
    due_result = await db.execute(
        select(func.count(WordProgress.id)).where(
            WordProgress.user_id == user.id,
            WordProgress.learned == True,
            WordProgress.next_review_at <= today,
            WordProgress.learning_stage != "mastered",
        )
    )
    due_today = due_result.scalar() or 0

    return {
        "total_learned": total,
        "mastered": mastered,
        "due_today": due_today,
        "learning": total - mastered - due_today,
    }
