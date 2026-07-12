import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.grammar import GrammarPoint
from app.schemas.grammar import GrammarRead, GrammarDetailRead

router = APIRouter(prefix="/grammar", tags=["语法"])


@router.get("", response_model=list[GrammarRead])
async def list_grammar(
    level: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(GrammarPoint).order_by(GrammarPoint.order_index)
    if level:
        stmt = stmt.where(GrammarPoint.level == level)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/{grammar_id}", response_model=GrammarDetailRead)
async def get_grammar(grammar_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GrammarPoint)
        .where(GrammarPoint.id == grammar_id)
        .options(selectinload(GrammarPoint.examples))
    )
    gp = result.scalar_one_or_none()
    if not gp:
        raise HTTPException(status_code=404, detail="语法点不存在")
    return gp
