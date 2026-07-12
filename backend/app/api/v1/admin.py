from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.seed import seed_all

router = APIRouter(prefix="/admin", tags=["管理"])


@router.post("/seed")
async def run_seed(
    scope: str = Query("all", description="all | letters | words | grammar | batchim | sentences"),
    db: AsyncSession = Depends(get_db),
):
    await seed_all(db, scope=scope)
    return {"message": f"Seed data loaded: scope={scope}"}
