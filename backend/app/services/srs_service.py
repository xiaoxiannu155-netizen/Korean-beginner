from datetime import date, timedelta

# SRS 间隔映射: review_count → 间隔天数
SRS_INTERVALS = [0, 1, 3, 7, 14, 30]  # index = review_count


def calculate_next_review(
    review_count: int,
    is_correct: bool,
    consecutive_correct: int,
) -> dict:
    """计算 SRS 下次复习时间。

    复习流程:
      review_count=0 (新词) → 当天复习 → rc=1
      rc=1 → 1天后 → rc=2
      rc=2 → 3天后 → rc=3
      rc=3 → 7天后 → rc=4
      rc=4 → 14天后 → rc=5
      rc=5 → 30天后 → mastered
    """
    today = date.today()

    if not is_correct:
        # 遗忘 → 重置间隔为1天，review_count 不变
        return {
            "review_count": review_count,
            "srs_interval_days": 1,
            "next_review_at": today + timedelta(days=1),
            "consecutive_correct": 0,
            "learning_stage": "learning",
        }

    new_consecutive = consecutive_correct + 1

    # 连续3次正确 → 提前晋级
    if new_consecutive >= 3 and review_count < 6:
        new_review_count = min(review_count + 1, 6)
        new_consecutive = 0
    else:
        new_review_count = min(review_count + 1, 6)

    # 达到 mastered
    if new_review_count >= 6:
        return {
            "review_count": 6,
            "srs_interval_days": 0,
            "next_review_at": None,
            "consecutive_correct": new_consecutive,
            "learning_stage": "mastered",
        }

    interval = SRS_INTERVALS[new_review_count]

    return {
        "review_count": new_review_count,
        "srs_interval_days": interval,
        "next_review_at": today + timedelta(days=interval),
        "consecutive_correct": new_consecutive,
        "learning_stage": "familiar" if new_review_count >= 4 else "learning",
    }
