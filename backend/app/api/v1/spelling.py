from fastapi import APIRouter, Query
from app.services.spelling_game_service import (
    generate_spelling_question,
    generate_chain_question,
    check_spelling_answer,
)

router = APIRouter(prefix="/spelling", tags=["拼读游戏"])


@router.get("/question")
async def get_question(level: int = Query(1, ge=1, le=4)):
    """Get a spelling practice question"""
    return generate_spelling_question(level)


@router.get("/chain")
async def get_chain(count: int = Query(5, ge=3, le=10)):
    """Get a chain of syllable building questions"""
    return generate_chain_question(count)


@router.post("/check")
async def check_answer(user_input: str, correct_answer: str):
    """Check spelling answer. Query params: user_input, correct_answer"""
    return check_spelling_answer(user_input, correct_answer)
