"""Spelling game: generate syllable combination exercises"""
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.letter import Letter
from app.models.word import Word


# Common syllable combinations for practice
VOWELS = ["ㅏ", "ㅑ", "ㅓ", "ㅕ", "ㅗ", "ㅛ", "ㅜ", "ㅠ", "ㅡ", "ㅣ"]
CONSONANTS = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

# Real examples for each level
LEVEL_EXAMPLES = {
    1: ["가", "나", "다", "라", "마", "바", "사", "아", "자", "하"],
    2: ["각", "간", "감", "강", "국", "김", "논", "달", "밥", "산"],
    3: ["값", "넋", "앉", "읽", "젊", "싫", "많", "없", "있", "했"],
    4: ["한국", "학교", "감사", "사랑", "친구", "음악", "여행", "김치", "서울", "부산"],
}


def generate_spelling_question(level: int = 1) -> dict:
    """Generate a spelling practice question.
    Level 1: Basic CV syllables (가, 나, 다...)
    Level 2: CVC with batchim (각, 간, 감...)
    Level 3: Double batchim (값, 넋...)
    Level 4: Multi-syllable words (한국, 학교...)
    """
    examples = LEVEL_EXAMPLES.get(level, LEVEL_EXAMPLES[1])
    answer = random.choice(examples)

    # Decompose the syllable
    if level <= 3:
        decomposition = _decompose_syllable(answer)
    else:
        # Multi-syllable: decompose each syllable
        parts = []
        for ch in answer:
            parts.append(_decompose_syllable(ch))
        decomposition = " + ".join(parts)

    # Generate wrong options
    other_options = [w for w in examples if w != answer]
    random.shuffle(other_options)
    options = [answer] + other_options[:3]
    random.shuffle(options)

    return {
        "answer": answer,
        "decomposition": decomposition,
        "options": options,
        "level": level,
    }


def generate_chain_question(count: int = 5) -> list[dict]:
    """Generate a chain of syllable building questions (ga → na → da style)"""
    selected = random.sample(LEVEL_EXAMPLES[1], min(count, len(LEVEL_EXAMPLES[1])))
    questions = []
    for syllable in selected:
        decomp = _decompose_syllable(syllable)
        questions.append({
            "syllable": syllable,
            "decomposition": decomp,
        })
    return questions


def _decompose_syllable(syllable: str) -> str:
    """Decompose a Korean syllable into its parts.
    Examples: 가 → ㄱ+ㅏ, 각 → ㄱ+ㅏ+ㄱ, 값 → ㄱ+ㅏ+ㅂㅅ
    """
    if not syllable:
        return ""

    ch = syllable[0]
    code = ord(ch)
    if code < 0xAC00 or code > 0xD7A3:
        return ch

    base = code - 0xAC00
    cho = base // (21 * 28)
    jung = (base % (21 * 28)) // 28
    jong = base % 28

    CHOSUNG = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
    JUNGSUNG = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]
    JONGSUNG = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

    chosung = CHOSUNG[cho]
    jungsung = JUNGSUNG[jung]
    jongsung = JONGSUNG[jong] if jong > 0 else ""

    if jongsung:
        return f"{chosung}+{jungsung}+{jongsung}"
    return f"{chosung}+{jungsung}"


def check_spelling_answer(user_input: str, correct_answer: str) -> dict:
    """Check if user's spelling matches the correct answer"""
    is_correct = user_input.strip() == correct_answer.strip()
    return {
        "is_correct": is_correct,
        "user_input": user_input,
        "correct_answer": correct_answer,
        "xp_earned": 10 if is_correct else 0,
    }
