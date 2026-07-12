from app.services.gamification_service import get_level_name


class TestGetLevelName:
    def test_copper(self):
        level, name = get_level_name(0)
        assert "铜" in name
        assert level == 1

    def test_silver(self):
        level, name = get_level_name(600)
        assert "银" in name

    def test_gold(self):
        level, name = get_level_name(1500)
        assert "金" in name

    def test_diamond(self):
        level, name = get_level_name(2500)
        assert "钻石" in name
