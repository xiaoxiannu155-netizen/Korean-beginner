"""Speech evaluation service - pronunciation scoring using DTW + phonetic comparison"""
import math

# Korean phoneme similarity matrix (simplified)
# Higher score = more similar pronunciation
PHONEME_SIMILARITY = {
    # Vowel pairs that sound similar
    ("ㅏ", "ㅓ"): 0.7, ("ㅓ", "ㅗ"): 0.7, ("ㅗ", "ㅜ"): 0.7,
    ("ㅐ", "ㅔ"): 0.95,  # Nearly identical in Seoul dialect
    ("ㅡ", "ㅣ"): 0.5,
    # Consonant pairs
    ("ㄱ", "ㄲ"): 0.9, ("ㄷ", "ㄸ"): 0.9, ("ㅂ", "ㅃ"): 0.9, ("ㅅ", "ㅆ"): 0.9, ("ㅈ", "ㅉ"): 0.9,
    ("ㄱ", "ㅋ"): 0.8, ("ㄷ", "ㅌ"): 0.8, ("ㅂ", "ㅍ"): 0.8, ("ㅈ", "ㅊ"): 0.8,
    ("ㄴ", "ㄷ"): 0.6, ("ㄹ", "ㄴ"): 0.7, ("ㅁ", "ㅂ"): 0.7,
    # Batchim confusion pairs
    ("ㄱ", "ㅇ"): 0.6,  # Both back-of-mouth sounds
    ("ㄷ", "ㅅ"): 0.7,  # Similar tongue position
    ("ㄷ", "ㅈ"): 0.6,
}


def evaluate_pronunciation(
    target_text: str,
    user_audio_features: dict | None = None,
    difficulty_tolerance: float = 0.3,
) -> dict:
    """Evaluate pronunciation quality.

    For MVP: uses simulated scoring based on phonetic analysis.
    In production: uses Azure Speech Assessment API or custom DTW + Wav2Vec2 model.

    Args:
        target_text: The Korean text to pronounce
        user_audio_features: Optional extracted audio features (pitch, duration, etc.)
        difficulty_tolerance: How lenient the scoring is (0=strict, 1=lenient)

    Returns:
        dict with overall_score, syllable_scores, and feedback
    """
    # For MVP: Generate simulated but realistic scores
    # Based on text length and complexity
    import random
    random.seed(sum(ord(c) for c in target_text))

    syllables = []
    for ch in target_text:
        if '가' <= ch <= '힣':
            code = ord(ch) - 0xAC00
            cho = code // (21 * 28)
            jung = (code % (21 * 28)) // 28
            jong = code % 28
            has_batchim = jong > 0
            complexity = 1 + (0.5 if has_batchim else 0)
        else:
            complexity = 0.5

        base_score = random.uniform(0.6, 1.0)
        adjusted_score = min(1.0, base_score + difficulty_tolerance * 0.2)

        syllables.append({
            "syllable": ch,
            "score": round(adjusted_score, 2),
            "status": "good" if adjusted_score >= 0.8 else ("ok" if adjusted_score >= 0.6 else "needs_work"),
        })

    if not syllables:
        return {"overall_score": 0, "syllable_scores": [], "feedback": "无法评估：文本中没有韩文音节"}

    overall = round(sum(s["score"] for s in syllables) / len(syllables), 2)

    # Generate feedback
    low_syllables = [s for s in syllables if s["status"] == "needs_work"]
    feedback_items = []

    if overall >= 0.9:
        feedback_items.append("🏆 发音非常标准！跟韩国人一样自然。")
    elif overall >= 0.8:
        feedback_items.append("👍 发音很好！继续练习可以更流利。")
    elif overall >= 0.6:
        feedback_items.append("📖 发音基本正确，多注意收音部分。")
    else:
        feedback_items.append("💪 还需要多练习，Joy会帮你的！")

    if low_syllables:
        feedback_items.append(f"注意这些音节：{' '.join(s['syllable'] for s in low_syllables)}")

    # Batchim tips
    batchim_syllables = []
    for ch in target_text:
        if '가' <= ch <= '힣':
            code = ord(ch) - 0xAC00
            jong = code % 28
            if jong > 0:
                JONGSUNG = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
                batchim_syllables.append(f"{ch}({JONGSUNG[jong]}收音)")

    if batchim_syllables:
        feedback_items.append(f"💡 收音音节: {', '.join(batchim_syllables)}")

    return {
        "target_text": target_text,
        "overall_score": overall,
        "syllable_scores": syllables,
        "feedback": feedback_items,
        "xp_earned": max(0, int(overall * 20)),
    }


def compare_phonemes(target: str, spoken: str) -> float:
    """Compare two Korean phoneme strings and return similarity score 0-1"""
    if not target or not spoken:
        return 0.0

    if target == spoken:
        return 1.0

    pair = tuple(sorted([target, spoken]))
    return PHONEME_SIMILARITY.get(pair, 0.3)


def get_pronunciation_tips(text: str) -> list[str]:
    """Get pronunciation tips for a Korean text"""
    tips = []

    for ch in text:
        if '가' <= ch <= '힣':
            code = ord(ch) - 0xAC00
            cho = code // (21 * 28)
            jong = code % 28

            # Batchim tips
            if jong > 0:
                JONGSUNG = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
                b = JONGSUNG[jong]
                if b in ["ㄱ", "ㄷ", "ㅂ"]:
                    tips.append(f"{ch}: {b}收音不爆发，只做口型")
                elif b in ["ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ"]:
                    tips.append(f"{ch}: {b}是紧音收音，喉部要用力")
                elif b in ["ㄳ", "ㄵ", "ㄶ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㅀ", "ㅄ"]:
                    tips.append(f"{ch}: 双收音{b}，只发第一个音")

    return list(set(tips))
