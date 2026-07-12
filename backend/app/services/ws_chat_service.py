"""WebSocket chat service for AI conversation"""
import json
import random
from datetime import datetime, timezone

# Sample AI responses for free chat
CHAT_RESPONSES = {
    "greeting": [
        {"ko": "안녕하세요! 오늘 기분이 어때요?", "zh": "你好！今天心情怎么样？", "pron": "an-nyeong-ha-se-yo! o-neul gi-bun-i eo-ttae-yo?"},
        {"ko": "안녕! 한국어 공부 재미있어요?", "zh": "嗨！学韩语有趣吗？", "pron": "an-nyeong! han-guk-eo gong-bu jae-mi-it-seo-yo?"},
    ],
    "encouragement": [
        {"ko": "잘하고 있어요! 계속 연습하세요~", "zh": "做得很好！继续练习吧~", "pron": "jal-ha-go it-seo-yo! gye-sok yeon-seup-ha-se-yo~"},
        {"ko": "대단해요! 실력이 점점 늘고 있어요!", "zh": "太厉害了！实力在逐渐增长！", "pron": "dae-dan-hae-yo! sil-lyeok-i jeom-jeom neul-go it-seo-yo!"},
    ],
    "correction": [
        {"ko": "발음 조금만 더 연습하면 완벽할 거예요!", "zh": "发音再练习一下就会完美的！", "pron": "bal-eum jo-geum-man deo yeon-seup-ha-myeon wan-byeok-hal geo-ye-yo!"},
    ],
    "question_response": [
        {"ko": "아, 좋은 질문이에요! 한국어는 정말 재미있는 언어예요.", "zh": "啊，好问题！韩语真的是很有趣的语言。", "pron": None},
        {"ko": "네, 맞아요! 한국어 문법이 조금 어렵지만 천천히 배우면 돼요.", "zh": "是的，没错！韩语语法虽然有点难，但慢慢学就行了。", "pron": None},
    ],
    "farewell": [
        {"ko": "다음에 또 봐요! 열심히 공부하세요~", "zh": "下次再见！努力学习哦~", "pron": "da-eum-e tto bwa-yo! yeol-sim-hi gong-bu-ha-se-yo~"},
        {"ko": "수고했어요! 내일도 같이 공부해요~", "zh": "辛苦了！明天也一起学习吧~", "pron": "su-go-haet-seo-yo! nae-il-do gat-chi gong-bu-hae-yo~"},
    ],
}


def classify_message(message: str) -> str:
    """Classify user message intent for response selection"""
    msg = message.lower()
    if any(w in msg for w in ["안녕", "하세요", "hi", "hello", "你好"]):
        return "greeting"
    if any(w in msg for w in ["잘가", "bye", "다음", "再见", "내일"]):
        return "farewell"
    if any(w in msg for w in ["어때", "어떻게", "뭐", "왜", "언제", "어디", "吗", "什么", "怎么"]):
        return "question_response"
    return "encouragement"


def generate_chat_response(user_message: str) -> dict:
    """Generate an AI chat response based on user message"""
    category = classify_message(user_message)
    responses = CHAT_RESPONSES.get(category, CHAT_RESPONSES["encouragement"])
    response = random.choice(responses)

    return {
        "user_message": user_message,
        "reply": response["ko"],
        "reply_zh": response["zh"],
        "reply_pronunciation": response.get("pron"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def get_chat_starter() -> dict:
    """Get a random chat starter message"""
    return random.choice(CHAT_RESPONSES["greeting"])
