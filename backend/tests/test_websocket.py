"""WebSocket tests - unit tests for chat service"""
from app.services.ws_chat_service import classify_message, generate_chat_response, get_chat_starter


class TestChatClassification:
    def test_greeting(self):
        assert classify_message("안녕하세요") == "greeting"
        assert classify_message("你好") == "greeting"
        assert classify_message("hello") == "greeting"

    def test_farewell(self):
        assert classify_message("잘가요") == "farewell"
        assert classify_message("再见") == "farewell"
        assert classify_message("bye") == "farewell"

    def test_question(self):
        assert classify_message("이게 뭐예요?") == "question_response"
        assert classify_message("怎么学") == "question_response"

    def test_default_fallback(self):
        assert classify_message("그냥 말하는 거예요") == "encouragement"


class TestChatResponse:
    def test_generate_response_has_required_fields(self):
        resp = generate_chat_response("안녕하세요")
        assert "reply" in resp
        assert "reply_zh" in resp
        assert "user_message" in resp
        assert "timestamp" in resp

    def test_starter_is_valid(self):
        starter = get_chat_starter()
        assert "ko" in starter
        assert "zh" in starter
