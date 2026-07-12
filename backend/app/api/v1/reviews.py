from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.services.srs_scheduler import get_due_reviews, get_review_stats

router = APIRouter(prefix="/reviews", tags=["SRS复习"])


@router.get("/due")
async def due_reviews(
    limit: int = Query(20, le=50),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get words due for review today"""
    return await get_due_reviews(db, user, limit)


@router.get("/stats")
async def review_stats(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get SRS review statistics"""
    return await get_review_stats(db, user)
