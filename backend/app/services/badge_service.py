from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User
from app.models.activity import UserBadge, ActivityLog
from app.models.letter import LetterProgress
from app.models.word import WordProgress
from app.schemas.badge import ALL_BADGES


async def check_and_award_badges(db: AsyncSession, user: User) -> list[str]:
    """Check all badge conditions and award any newly earned badges. Returns list of new badge types."""
    existing = await db.execute(
        select(UserBadge.badge_type).where(UserBadge.user_id == user.id)
    )
    existing_types = set(r[0] for r in existing.all())
    new_badges = []

    # Check each condition
    checks = {
        "first_letter": await _check_first_letter(db, user),
        "vowel_master": await _check_vowel_master(db, user),
        "consonant_master": await _check_consonant_master(db, user),
        "first_word": await _check_first_word(db, user),
        "word_50": await _check_word_count(db, user, 50),
        "word_100": await _check_word_count(db, user, 100),
        "word_300": await _check_word_count(db, user, 300),
        "streak_3": await _check_streak(db, user, 3),
        "streak_7": await _check_streak(db, user, 7),
        "streak_30": await _check_streak(db, user, 30),
    }

    for badge_type, earned in checks.items():
        if earned and badge_type not in existing_types:
            db.add(UserBadge(user_id=user.id, badge_type=badge_type))
            new_badges.append(badge_type)

    if new_badges:
        await db.commit()
    return new_badges


async def get_user_badges(db: AsyncSession, user: User) -> list[dict]:
    """Get all badges a user has earned"""
    result = await db.execute(
        select(UserBadge).where(UserBadge.user_id == user.id)
    )
    earned = {r.badge_type: r for r in result.scalars().all()}

    badge_list = []
    for bd in ALL_BADGES:
        badge_list.append({
            "badge_type": bd.badge_type,
            "name": bd.name,
            "description": bd.description,
            "icon": bd.icon,
            "condition": bd.condition,
            "earned": bd.badge_type in earned,
            "earned_at": earned[bd.badge_type].earned_at.isoformat() if bd.badge_type in earned else None,
        })
    return badge_list


async def _check_first_letter(db: AsyncSession, user: User) -> bool:
    result = await db.execute(
        select(func.count(LetterProgress.id)).where(
            LetterProgress.user_id == user.id,
            LetterProgress.mastered == True,
        )
    )
    return result.scalar() >= 1


async def _check_vowel_master(db: AsyncSession, user: User) -> bool:
    result = await db.execute(
        select(func.count(LetterProgress.id)).where(
            LetterProgress.user_id == user.id,
            LetterProgress.letter_type == "basic_vowel",
            LetterProgress.mastered == True,
        )
    )
    return result.scalar() >= 10


async def _check_consonant_master(db: AsyncSession, user: User) -> bool:
    result = await db.execute(
        select(func.count(LetterProgress.id)).where(
            LetterProgress.user_id == user.id,
            LetterProgress.letter_type == "consonant",
            LetterProgress.mastered == True,
        )
    )
    return result.scalar() >= 14


async def _check_first_word(db: AsyncSession, user: User) -> bool:
    result = await db.execute(
        select(func.count(WordProgress.id)).where(
            WordProgress.user_id == user.id,
            WordProgress.learned == True,
        )
    )
    return result.scalar() >= 1


async def _check_word_count(db: AsyncSession, user: User, count: int) -> bool:
    result = await db.execute(
        select(func.count(WordProgress.id)).where(
            WordProgress.user_id == user.id,
            WordProgress.learned == True,
        )
    )
    return result.scalar() >= count


async def _check_streak(db: AsyncSession, user: User, days: int) -> bool:
    from app.services.user_service import get_user_progress
    progress = await get_user_progress(db, user)
    return progress.streak_days >= days
