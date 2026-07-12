from datetime import date, timedelta

from app.services.srs_service import calculate_next_review


class TestSRSCalculateNextReview:
    def test_new_word_first_correct(self):
        """新词首次正确 → review_count=1, 间隔=1天"""
        result = calculate_next_review(
            review_count=0, is_correct=True, consecutive_correct=0
        )
        assert result["review_count"] == 1
        assert result["srs_interval_days"] == 1
        assert result["next_review_at"] == date.today() + timedelta(days=1)
        assert result["learning_stage"] == "learning"

    def test_progression_through_stages(self):
        """测试完整 SRS 进程"""
        today = date.today()
        expected = [
            (1, today + timedelta(days=1)),   # 新词 → 1天
            (3, today + timedelta(days=3)),   # → 3天
            (7, today + timedelta(days=7)),   # → 7天
            (14, today + timedelta(days=14)), # → 14天
            (30, today + timedelta(days=30)), # → 30天
        ]

        rc = 0
        cc = 0
        for exp_interval, exp_next in expected:
            result = calculate_next_review(
                review_count=rc, is_correct=True, consecutive_correct=cc
            )
            assert result["srs_interval_days"] == exp_interval
            assert result["next_review_at"] == exp_next
            rc = result["review_count"]
            cc = 0

    def test_mastered_after_6(self):
        """第6次正确 → mastered"""
        result = calculate_next_review(
            review_count=5, is_correct=True, consecutive_correct=0
        )
        assert result["review_count"] == 6
        assert result["learning_stage"] == "mastered"
        assert result["next_review_at"] is None

    def test_wrong_answer_resets_interval(self):
        """错误 → 间隔重置为1天，review_count 不变"""
        result = calculate_next_review(
            review_count=3, is_correct=False, consecutive_correct=2
        )
        assert result["review_count"] == 3  # 不变
        assert result["srs_interval_days"] == 1  # 重置
        assert result["consecutive_correct"] == 0  # 清零

    def test_three_consecutive_correct_skip(self):
        """连续3次正确 → 提前晋级"""
        result = calculate_next_review(
            review_count=2, is_correct=True, consecutive_correct=2
        )
        assert result["review_count"] == 3
        assert result["srs_interval_days"] == 7  # 跳过了3天，直接到7天
        assert result["consecutive_correct"] == 0
