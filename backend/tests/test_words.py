import uuid
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


async def _register(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": f"word{uuid.uuid4().hex[:8]}@example.com",
        "username": "word_tester",
        "password": "testpass123",
    })
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_get_word_with_examples(client, db_session: AsyncSession):
    from app.models.word import Word, WordExample
    w = Word(
        korean="사랑", chinese="爱情",
        romanization="sarang", category="life", sub_category="emotion",
    )
    db_session.add(w)
    await db_session.flush()
    ex = WordExample(
        word_id=w.id,
        korean_sentence="사랑해요.", chinese_translation="我爱你。",
        source_type="drama", source_name="泪之女王",
    )
    db_session.add(ex)
    await db_session.commit()

    resp = await client.get(f"/api/v1/words/{w.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["korean"] == "사랑"
    assert data["chinese"] == "爱情"
    assert len(data["examples"]) == 1
    assert data["examples"][0]["source_name"] == "泪之女王"


@pytest.mark.asyncio
async def test_review_word_srs_progression(client, db_session: AsyncSession):
    from app.models.word import Word
    w = Word(
        korean="감사합니다", chinese="谢谢",
        romanization="gamsahamnida", category="travel",
    )
    db_session.add(w)
    await db_session.commit()

    token = await _register(client)

    # 第1次正确 → review_count=1, interval=1d
    resp = await client.post(
        f"/api/v1/words/{w.id}/review",
        json={"is_correct": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["review_count"] == 1
    assert data["srs_interval_days"] == 1
    assert data["learning_stage"] == "learning"


@pytest.mark.asyncio
async def test_get_words_pagination(client, db_session: AsyncSession):
    from app.models.word import Word
    for i in range(5):
        db_session.add(Word(korean=f"테스트{i}", chinese=f"测试{i}", category="test"))
    await db_session.commit()

    resp = await client.get("/api/v1/words?page=1&page_size=3")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 3
