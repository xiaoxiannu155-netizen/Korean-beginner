from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.services.badge_service import get_user_badges, check_and_award_badges

router = APIRouter(prefix="/badges", tags=["勋章"])


@router.get("")
async def list_badges(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get all badges with earned status"""
    return await get_user_badges(db, user)


@router.post("/check")
async def check_badges(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Check and award any newly earned badges"""
    new = await check_and_award_badges(db, user)
    return {"new_badges": new}
