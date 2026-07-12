"""Track daily study time"""
from datetime import date, datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User
from app.models.activity import ActivityLog


async def get_today_study_minutes(db: AsyncSession, user: User) -> int:
    """Get today's total study time in minutes (estimated from activity count)"""
    today = date.today()
    result = await db.execute(
        select(func.count(ActivityLog.id)).where(
            ActivityLog.user_id == user.id,
            func.date(ActivityLog.created_at) == today,
        )
    )
    count = result.scalar() or 0
    # Estimate ~2 minutes per activity
    return count * 2


async def get_weekly_study_data(db: AsyncSession, user: User) -> list[dict]:
    """Get study activity counts for the last 7 days"""
    today = date.today()
    data = []
    for i in range(6, -1, -1):
        d = today.replace(day=today.day - i) if today.day > i else today
        # Simplified - just count activities per day
        result = await db.execute(
            select(func.count(ActivityLog.id)).where(
                ActivityLog.user_id == user.id,
                func.date(ActivityLog.created_at) == d,
            )
        )
        count = result.scalar() or 0
        data.append({
            "date": d.isoformat(),
            "activity_count": count,
            "studied": count > 0,
        })
    return data
