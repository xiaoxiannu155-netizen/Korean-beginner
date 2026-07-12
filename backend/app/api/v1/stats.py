from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import date

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User, UserProgress
from app.models.activity import DailyTask, ActivityLog

router = APIRouter(tags=["统计"])


@router.get("/stats/personal")
async def personal_stats(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """个人学习统计 (非竞争型)"""
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == user.id)
    )
    progress = result.scalar_one()

    today = date.today()
    task_result = await db.execute(
        select(DailyTask).where(
            DailyTask.user_id == user.id,
            DailyTask.task_date == today,
        )
    )
    today_task = task_result.scalar_one_or_none()

    # Today's word count
    today_words_result = await db.execute(
        select(func.count(ActivityLog.id)).where(
            ActivityLog.user_id == user.id,
            ActivityLog.activity_type == "daily_word",
            func.date(ActivityLog.created_at) == today,
        )
    )
    today_words = today_words_result.scalar() or 0

    # Simple completion % based on stage
    stage_percentages = {1: 0.25, 2: 0.50, 3: 0.75, 4: 1.0}
    completion = stage_percentages.get(progress.stage, 0.0) * 100

    return {
        "total_xp": progress.total_xp,
        "level": progress.level,
        "streak_days": progress.streak_days,
        "today_words_learned": today_words,
        "stage": progress.stage,
        "completion_percentage": completion,
    }
