from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.activity import DailyTaskRead
from app.services.gamification_service import (
    get_or_create_daily_task, award_xp,
)

router = APIRouter(prefix="/daily-tasks", tags=["每日任务"])


@router.get("/today", response_model=DailyTaskRead)
async def get_today_tasks(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await get_or_create_daily_task(db, user)


@router.post("/complete", response_model=DailyTaskRead)
async def complete_task(
    task_type: str = Query(..., description="word | grammar | listening | speaking"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = await get_or_create_daily_task(db, user)

    xp_map = {
        "word": 6,
        "grammar": 20,
        "listening": 15,
        "speaking": 25,
    }
    xp = xp_map.get(task_type, 0)

    if task_type == "word":
        task.words_completed = min(task.words_completed + 1, 5)
    elif task_type == "grammar":
        task.grammar_completed = True
    elif task_type == "listening":
        task.listening_completed = True
    elif task_type == "speaking":
        task.speaking_completed = True

    await award_xp(db, user, xp, f"daily_{task_type}")
    await db.commit()
    return task
