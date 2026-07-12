import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.word import (
    WordRead, WordDetailRead, WordReviewSubmit, WordProgressRead,
)
from app.services.word_service import (
    get_words, get_word_with_examples, record_word_review,
)

router = APIRouter(prefix="/words", tags=["单词"])


@router.get("", response_model=dict)
async def list_words(
    category: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
):
    words, total = await get_words(db, category, page, page_size)
    return {
        "items": [WordRead.model_validate(w) for w in words],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{word_id}", response_model=WordDetailRead)
async def get_word(word_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    word = await get_word_with_examples(db, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="单词不存在")
    return word


@router.post("/{word_id}/review", response_model=WordProgressRead)
async def review_word(
    word_id: uuid.UUID,
    body: WordReviewSubmit,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    word = await get_word_with_examples(db, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="单词不存在")
    progress = await record_word_review(db, user, word_id, body.is_correct)
    return progress
