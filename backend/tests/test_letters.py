import uuid
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


async def _register_and_get_token(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": f"letter{uuid.uuid4().hex[:8]}@example.com",
        "username": "letter_tester",
        "password": "testpass123",
    })
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_list_letters_empty(client):
    resp = await client.get("/api/v1/letters")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_submit_practice(client, db_session: AsyncSession):
    from app.models.letter import Letter
    letter = Letter(
        char="ㅏ", type="basic_vowel",
        romanization="a", chinese_hint="类似中文'啊'", order_index=1,
    )
    db_session.add(letter)
    await db_session.commit()

    token = await _register_and_get_token(client)

    resp = await client.post(
        f"/api/v1/letters/{letter.id}/practice",
        json={"score": 85.0, "mastered": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["mastered"] is True
    assert data["best_score"] == 85.0


@pytest.mark.asyncio
async def test_get_letter_404(client):
    resp = await client.get(f"/api/v1/letters/{uuid.uuid4()}")
    assert resp.status_code == 404
