"""Tests for grammar API filtering"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_filter_grammar_by_level(client, db_session: AsyncSession):
    """Filter grammar by level"""
    from app.models.grammar import GrammarPoint
    db_session.add(GrammarPoint(title="L1 Test", level=1, order_index=1))
    db_session.add(GrammarPoint(title="L2 Test", level=2, order_index=2))
    await db_session.commit()

    resp = await client.get("/api/v1/grammar?level=1")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["level"] == 1


@pytest.mark.asyncio
async def test_grammar_detail_with_examples(client, db_session: AsyncSession):
    """Grammar detail should include examples"""
    from app.models.grammar import GrammarPoint, GrammarExample
    gp = GrammarPoint(title="N + 은/는", level=1, order_index=1)
    db_session.add(gp)
    await db_session.flush()
    db_session.add(GrammarExample(grammar_id=gp.id, korean_sentence="저는 학생이에요.",
                                   chinese_translation="我是学生。", is_wrong_example=False))
    db_session.add(GrammarExample(grammar_id=gp.id, korean_sentence="저는 학생입니다.",
                                   chinese_translation="(错误示范-缺少이에요)", is_wrong_example=True))
    await db_session.commit()

    resp = await client.get(f"/api/v1/grammar/{gp.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["examples"]) == 2
    assert data["examples"][0]["is_wrong_example"] is False
    assert data["examples"][1]["is_wrong_example"] is True
