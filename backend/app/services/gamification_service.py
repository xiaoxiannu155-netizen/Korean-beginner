from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User, UserProgress
from app.models.activity import DailyTask, ActivityLog

# XP constants
XP_WORD = 6
XP_GRAMMAR = 20
XP_LISTENING = 15
XP_SPEAKING = 25

LEVEL_THRESHOLDS = [
    (0, "🥉 铜"),
    (100, "🥉 铜 II"),
    (300, "🥈 银"),
    (600, "🥈 银 II"),
    (1000, "🥇 金"),
    (1500, "🥇 金 II"),
    (2500, "💎 钻石"),
]


def get_level_name(xp: int) -> tuple[int, str]:
    level = 1
    name = "🥉 铜"
    for i, (threshold, label) in enumerate(LEVEL_THRESHOLDS):
        if xp >= threshold:
            level = i + 1
            name = label
    return level, name


async def get_or_create_daily_task(db: AsyncSession, user: User) -> DailyTask:
    today = date.today()
    result = await db.execute(
        select(DailyTask).where(
            DailyTask.user_id == user.id,
            DailyTask.task_date == today,
        )
    )
    task = result.scalar_one_or_none()
    if not task:
        task = DailyTask(user_id=user.id, task_date=today)
        db.add(task)
        await db.flush()
    return task


async def award_xp(db: AsyncSession, user: User, xp: int, activity_type: str,
                   target_id=None, score=None):
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == user.id)
    )
    progress = result.scalar_one()
    progress.total_xp += xp
    new_level, _ = get_level_name(progress.total_xp)
    progress.level = new_level

    log = ActivityLog(
        user_id=user.id,
        activity_type=activity_type,
        target_id=target_id,
        score=score,
        xp_earned=xp,
    )
    db.add(log)
    await db.commit()
