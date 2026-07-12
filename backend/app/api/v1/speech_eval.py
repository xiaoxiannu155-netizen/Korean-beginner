from fastapi import APIRouter, Query
from app.services.speech_evaluation_service import evaluate_pronunciation, get_pronunciation_tips

router = APIRouter(prefix="/speech", tags=["语音评估"])


@router.post("/evaluate")
async def evaluate(body: dict):
    """Evaluate pronunciation for given text.

    Body: {"text": "사랑해요", "difficulty_tolerance": 0.3}
    In production: also accepts audio file upload.
    """
    text = body.get("text", "")
    tolerance = body.get("difficulty_tolerance", 0.3)
    return evaluate_pronunciation(text, difficulty_tolerance=tolerance)


@router.get("/tips/{text:path}")
async def pronunciation_tips(text: str):
    """Get pronunciation tips for a Korean phrase"""
    return {
        "text": text,
        "tips": get_pronunciation_tips(text),
    }
