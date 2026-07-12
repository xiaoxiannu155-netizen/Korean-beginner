"""AI Translation service - integrates with LLM for Korean↔Chinese translation"""
import hashlib
import json
from app.services.tts_service import tts_service

# Cached common translations for MVP (no API call needed for frequent phrases)
COMMON_TRANSLATIONS = {
    "你好": {"result": "안녕하세요", "pronunciation": "an-nyeong-ha-se-yo", "breakdown": [
        {"syllable": "안", "components": "ㅇ+ㅏ+ㄴ", "pronunciation_hint": "an"},
        {"syllable": "녕", "components": "ㄴ+ㅕ+ㅇ", "pronunciation_hint": "nyeong"},
        {"syllable": "하", "components": "ㅎ+ㅏ", "pronunciation_hint": "ha"},
        {"syllable": "세", "components": "ㅅ+ㅔ", "pronunciation_hint": "se"},
        {"syllable": "요", "components": "ㅇ+ㅛ", "pronunciation_hint": "yo"},
    ]},
    "谢谢": {"result": "감사합니다", "pronunciation": "gam-sa-ham-ni-da"},
    "对不起": {"result": "죄송합니다", "pronunciation": "joe-song-ham-ni-da"},
    "我爱你": {"result": "사랑해요", "pronunciation": "sa-rang-hae-yo"},
    "再见": {"result": "안녕히 가세요", "pronunciation": "an-nyeong-hi ga-se-yo"},
    "你好吗": {"result": "잘 지내세요?", "pronunciation": "jal ji-nae-se-yo?"},
    "我很好": {"result": "잘 지내요", "pronunciation": "jal ji-nae-yo"},
    "早安": {"result": "좋은 아침입니다", "pronunciation": "jo-eun a-chim-im-ni-da"},
    "晚安": {"result": "잘 자요", "pronunciation": "jal ja-yo"},
    "好吃": {"result": "맛있어요", "pronunciation": "ma-sit-seo-yo"},
    "我想吃饭": {"result": "밥 먹고 싶어요", "pronunciation": "bap meok-go sip-eo-yo"},
    "多少钱": {"result": "얼마예요?", "pronunciation": "eol-ma-ye-yo?"},
    "太贵了": {"result": "너무 비싸요", "pronunciation": "neo-mu bi-ssa-yo"},
    "便宜点": {"result": "좀 깎아 주세요", "pronunciation": "jom kkak-a ju-se-yo"},
    "请帮我": {"result": "도와주세요", "pronunciation": "do-wa-ju-se-yo"},
    "不知道": {"result": "몰라요", "pronunciation": "mol-la-yo"},
    "等一下": {"result": "잠시만요", "pronunciation": "jam-si-man-yo"},
    "加油": {"result": "파이팅", "pronunciation": "pa-i-ting"},
    "生日快乐": {"result": "생일 축하합니다", "pronunciation": "saeng-il chuk-ha-ham-ni-da"},
    "我想你": {"result": "보고 싶어요", "pronunciation": "bo-go sip-eo-yo"},
}


class TranslationService:
    @staticmethod
    async def translate(text: str, direction: str = "zh-ko") -> dict:
        """Translate between Chinese and Korean.

        For MVP, uses cached common translations. In production, calls LLM API
        (Claude/GPT) for dynamic translations.
        """
        if direction == "zh-ko":
            result = COMMON_TRANSLATIONS.get(text)
            if result:
                breakdown = result.get("breakdown") or tts_service.get_pronunciation_breakdown(result["result"])
                return {
                    "input": text,
                    "result": result["result"],
                    "pronunciation": result["pronunciation"],
                    "breakdown": breakdown,
                    "audio_url": tts_service.get_audio_url(result["result"]),
                    "slow_audio_url": tts_service.get_audio_url(result["result"], speed=0.5),
                    "source": "cache",
                }
        elif direction == "ko-zh":
            # Reverse lookup
            for zh, ko_data in COMMON_TRANSLATIONS.items():
                ko = ko_data["result"] if isinstance(ko_data, dict) else ""
                if ko == text:
                    return {
                        "input": text,
                        "result": zh,
                        "pronunciation": None,
                        "breakdown": tts_service.get_pronunciation_breakdown(text),
                        "audio_url": tts_service.get_audio_url(text),
                        "slow_audio_url": tts_service.get_audio_url(text, speed=0.5),
                        "source": "cache",
                    }

        # Fallback for uncached translations
        return {
            "input": text,
            "result": text,  # Would call LLM in production
            "pronunciation": None,
            "breakdown": tts_service.get_pronunciation_breakdown(text),
            "audio_url": tts_service.get_audio_url(text),
            "slow_audio_url": tts_service.get_audio_url(text, speed=0.5),
            "source": "fallback",
        }

    @staticmethod
    async def search_pronunciation(query: str) -> dict:
        """Search Korean pronunciation by Chinese or Korean query"""
        # Check if query is in common translations
        result = COMMON_TRANSLATIONS.get(query)
        if result:
            return {
                "query": query,
                "korean": result["result"],
                "pronunciation": result["pronunciation"],
                "breakdown": tts_service.get_pronunciation_breakdown(result["result"]),
                "audio_url": tts_service.get_audio_url(result["result"]),
            }

        # If query looks like Korean, just return pronunciation
        if any('가' <= c <= '힣' for c in query):
            return {
                "query": query,
                "korean": query,
                "pronunciation": None,
                "breakdown": tts_service.get_pronunciation_breakdown(query),
                "audio_url": tts_service.get_audio_url(query),
            }

        return {"query": query, "korean": None, "message": "未找到匹配结果"}


translation_service = TranslationService()
