import uuid
import pytest


async def _register(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": f"review{uuid.uuid4().hex[:8]}@example.com",
        "username": "review_tester", "password": "testpass123",
    })
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_due_reviews_empty_for_new_user(client):
    token = await _register(client)
    resp = await client.get("/api/v1/reviews/due", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_review_stats_new_user(client):
    token = await _register(client)
    resp = await client.get("/api/v1/reviews/stats", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_learned"] == 0
    assert data["mastered"] == 0
    assert data["due_today"] == 0


@pytest.mark.asyncio
async def test_reviews_require_auth(client):
    resp = await client.get("/api/v1/reviews/due")
    assert resp.status_code == 403
