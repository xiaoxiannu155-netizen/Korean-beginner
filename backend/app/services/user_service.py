from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User, UserProgress


async def get_user_progress(db: AsyncSession, user: User) -> UserProgress:
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == user.id)
    )
    return result.scalar_one()


async def update_streak(db: AsyncSession, user: User) -> int:
    today = date.today()
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == user.id)
    )
    progress = result.scalar_one()

    if progress.last_active_date == today:
        return progress.streak_days

    if progress.last_active_date and (today - progress.last_active_date).days == 1:
        progress.streak_days += 1
    elif not progress.last_active_date or (today - progress.last_active_date).days > 1:
        progress.streak_days = 1

    progress.last_active_date = today
    await db.commit()
    return progress.streak_days
