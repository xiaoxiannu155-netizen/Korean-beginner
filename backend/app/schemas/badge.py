from pydantic import BaseModel
from datetime import datetime
import uuid


class BadgeRead(BaseModel):
    id: uuid.UUID
    badge_type: str
    earned_at: datetime

    model_config = {"from_attributes": True}


class BadgeDefinition:
    """Badge definitions - which badges exist and how to earn them"""
    def __init__(self, badge_type: str, name: str, description: str, icon: str, condition: str):
        self.badge_type = badge_type
        self.name = name
        self.description = description
        self.icon = icon
        self.condition = condition


ALL_BADGES = [
    BadgeDefinition("first_letter", "初识韩文", "学会第一个字母", "🔤", "完成任意1个字母学习"),
    BadgeDefinition("vowel_master", "元音大师", "掌握全部基础元音", "🅰️", "完成全部10个基础元音"),
    BadgeDefinition("consonant_master", "辅音达人", "掌握全部基础辅音", "🅱️", "完成全部14个基础辅音"),
    BadgeDefinition("first_word", "单词起步", "学会第一个单词", "📝", "学习任意1个单词"),
    BadgeDefinition("word_50", "词汇50", "掌握50个单词", "📚", "累计学习50个单词"),
    BadgeDefinition("word_100", "词汇100", "掌握100个单词", "📖", "累计学习100个单词"),
    BadgeDefinition("word_300", "词汇300", "掌握300个单词", "🏆", "累计学习300个单词"),
    BadgeDefinition("streak_3", "坚持3天", "连续学习3天", "🔥", "连续学习3天"),
    BadgeDefinition("streak_7", "一周之星", "连续学习7天", "⭐", "连续学习7天"),
    BadgeDefinition("streak_30", "月度冠军", "连续学习30天", "👑", "连续学习30天"),
    BadgeDefinition("first_grammar", "语法入门", "学会第一个语法点", "📐", "完成任意1个语法点"),
    BadgeDefinition("batchim_master", "收音专家", "学完所有收音规则", "🎯", "完成全部收音规则学习"),
    BadgeDefinition("speak_first", "开口说话", "第一次跟读练习", "🎤", "完成1次跟读评分"),
    BadgeDefinition("perfect_day", "完美一天", "一天内完成全部任务", "💯", "单日完成4项每日任务"),
    BadgeDefinition("joy_friend", "Joy之友", "自定义Joy设置", "🧚", "修改过Joy的名字或性格"),
]
