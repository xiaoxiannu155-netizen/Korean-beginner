"""TTS voice synthesis service - supports multiple providers"""
import hashlib
import json
from app.config import settings


class TTSService:
    """Text-to-Speech service abstraction.

    In production, integrate with Azure Neural TTS (ko-KR-SunHiNeural for female,
    ko-KR-InJoonNeural for male). For MVP, returns placeholder URLs.
    """

    # Azure TTS voices
    VOICES = {
        "female": "ko-KR-SunHiNeural",
        "male": "ko-KR-InJoonNeural",
    }

    @staticmethod
    def get_audio_url(text: str, speed: float = 1.0, gender: str = "female") -> str:
        """Generate TTS audio URL for Korean text.

        In production, this calls Azure Cognitive Services TTS API.
        For MVP, generates a cacheable URL pattern that the frontend
        can use to request audio from the /audio/tts endpoint.
        """
        cache_key = hashlib.md5(
            f"{text}:{speed}:{gender}".encode()
        ).hexdigest()
        voice = TTSService.VOICES.get(gender, TTSService.VOICES["female"])
        return f"/api/v1/audio/tts?text={text}&speed={speed}&gender={gender}&voice={voice}&cache_key={cache_key}"

    @staticmethod
    def get_pronunciation_breakdown(text: str) -> list[dict]:
        """Break down Korean text into syllables with pronunciation.

        Example:
            "사랑해요" → [
                {"syllable": "사", "pronunciation": "sa"},
                {"syllable": "랑", "pronunciation": "rang"},
                {"syllable": "해", "pronunciation": "hae"},
                {"syllable": "요", "pronunciation": "yo"},
            ]
        """
        # Simple romanization mapping for common syllables
        roman_map = {
            'ㄱ': 'g', 'ㄴ': 'n', 'ㄷ': 'd', 'ㄹ': 'r/l', 'ㅁ': 'm',
            'ㅂ': 'b', 'ㅅ': 's', 'ㅇ': '', 'ㅈ': 'j', 'ㅊ': 'ch',
            'ㅋ': 'k', 'ㅌ': 't', 'ㅍ': 'p', 'ㅎ': 'h',
            'ㅏ': 'a', 'ㅑ': 'ya', 'ㅓ': 'eo', 'ㅕ': 'yeo',
            'ㅗ': 'o', 'ㅛ': 'yo', 'ㅜ': 'u', 'ㅠ': 'yu', 'ㅡ': 'eu', 'ㅣ': 'i',
            'ㅐ': 'ae', 'ㅔ': 'e',
        }

        # For MVP, return simple syllable-by-syllable breakdown without full romanization
        result = []
        for ch in text:
            if '가' <= ch <= '힣':
                code = ord(ch) - 0xAC00
                cho = code // (21 * 28)
                jung = (code % (21 * 28)) // 28
                jong = code % 28

                CHOSUNG = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
                JUNGSUNG = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]
                JONGSUNG = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

                c = CHOSUNG[cho]
                v = JUNGSUNG[jung]
                f = JONGSUNG[jong] if jong > 0 else ""
                pron = (roman_map.get(c, c) + roman_map.get(v, v) + (roman_map.get(f, f) if f else ""))

                result.append({"syllable": ch, "components": f"{c}+{v}" + (f"+{f}" if f else ""), "pronunciation_hint": pron})
            else:
                result.append({"syllable": ch, "components": ch, "pronunciation_hint": ch})
        return result


tts_service = TTSService()
