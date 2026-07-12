from fastapi import APIRouter, Query, HTTPException
from app.services.translation_service import translation_service
from app.services.tts_service import tts_service

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/translate")
async def translate(body: dict):
    """Translate between Chinese and Korean"""
    text = body.get("text", "")
    direction = body.get("direction", "zh-ko")
    if not text:
        raise HTTPException(status_code=400, detail="text is required")
    return await translation_service.translate(text, direction)


@router.get("/search")
async def search(q: str = Query(..., description="搜索关键词")):
    """Search Korean pronunciation by query"""
    return await translation_service.search_pronunciation(q)


@router.get("/pronounce/{text:path}")
async def get_pronunciation(text: str, speed: float = Query(1.0, ge=0.25, le=2.0), gender: str = Query("female", pattern="^(female|male)$")):
    """Get pronunciation breakdown for Korean text"""
    return {
        "text": text,
        "speed": speed,
        "gender": gender,
        "breakdown": tts_service.get_pronunciation_breakdown(text),
        "audio_url": tts_service.get_audio_url(text, speed, gender),
        "slow_audio_url": tts_service.get_audio_url(text, min(speed * 0.5, 0.25), gender) if speed > 0.5 else None,
    }
