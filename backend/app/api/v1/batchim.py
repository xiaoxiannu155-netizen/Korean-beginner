import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.batchim import BatchimRule
from app.schemas.batchim import BatchimRuleRead, BatchimRuleDetailRead

router = APIRouter(prefix="/batchim", tags=["收音规则"])


@router.get("", response_model=list[BatchimRuleRead])
async def list_batchim(
    rule_type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(BatchimRule).order_by(BatchimRule.order_index)
    if rule_type:
        stmt = stmt.where(BatchimRule.rule_type == rule_type)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/{rule_id}", response_model=BatchimRuleDetailRead)
async def get_batchim(rule_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BatchimRule)
        .where(BatchimRule.id == rule_id)
        .options(selectinload(BatchimRule.examples))
    )
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="收音规则不存在")
    return rule
