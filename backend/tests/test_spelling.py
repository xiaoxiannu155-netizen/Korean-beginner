from app.services.spelling_game_service import (
    generate_spelling_question,
    _decompose_syllable,
    check_spelling_answer,
)


class TestSyllableDecomposition:
    def test_ga(self):
        assert _decompose_syllable("가") == "ㄱ+ㅏ"

    def test_gak(self):
        assert _decompose_syllable("각") == "ㄱ+ㅏ+ㄱ"

    def test_ggak(self):
        assert _decompose_syllable("깍") == "ㄲ+ㅏ+ㄱ"

    def test_sa(self):
        assert _decompose_syllable("사") == "ㅅ+ㅏ"

    def test_han(self):
        assert _decompose_syllable("한") == "ㅎ+ㅏ+ㄴ"

    def test_guk(self):
        assert _decompose_syllable("국") == "ㄱ+ㅜ+ㄱ"

    def test_neok(self):
        assert _decompose_syllable("넋") == "ㄴ+ㅓ+ㄳ"

    def test_eop(self):
        assert _decompose_syllable("없") == "ㅇ+ㅓ+ㅄ"


class TestSpellingGame:
    def test_generate_question_level1(self):
        q = generate_spelling_question(1)
        assert "answer" in q
        assert "decomposition" in q
        assert len(q["options"]) == 4
        assert q["answer"] in q["options"]
        assert q["level"] == 1

    def test_generate_question_level2(self):
        q = generate_spelling_question(2)
        assert "answer" in q
        # Level 2 words have batchim (받침)
        assert q["answer"] in ["각", "간", "감", "강", "국", "김", "논", "달", "밥", "산"]

    def test_check_correct(self):
        result = check_spelling_answer("가", "가")
        assert result["is_correct"] is True
        assert result["xp_earned"] == 10

    def test_check_wrong(self):
        result = check_spelling_answer("나", "가")
        assert result["is_correct"] is False
        assert result["xp_earned"] == 0

    def test_check_with_whitespace(self):
        result = check_spelling_answer(" 가 ", "가")
        assert result["is_correct"] is True
