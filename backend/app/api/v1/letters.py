from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.letter import LetterRead, LetterProgressRead, LetterPracticeSubmit
from app.services.letter_service import (
    get_letters_by_type, get_letter,
    record_letter_practice,
)

router = APIRouter(prefix="/letters", tags=["字母"])


@router.get("", response_model=list[LetterRead])
async def list_letters(
    type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await get_letters_by_type(db, type)


@router.get("/{letter_id}", response_model=LetterRead)
async def get_letter_detail(letter_id: str, db: AsyncSession = Depends(get_db)):
    letter = await get_letter(db, letter_id)
    if not letter:
        raise HTTPException(status_code=404, detail="字母不存在")
    return letter


@router.post("/{letter_id}/practice", response_model=LetterProgressRead)
async def practice_letter(
    letter_id: str,
    body: LetterPracticeSubmit,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    letter = await get_letter(db, letter_id)
    if not letter:
        raise HTTPException(status_code=404, detail="字母不存在")
    progress = await record_letter_practice(db, user, letter_id, body.score, body.mastered)
    return progress
