import uuid
import pytest


async def _register(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": f"badge{uuid.uuid4().hex[:8]}@example.com",
        "username": "badge_tester", "password": "testpass123",
    })
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_list_badges_new_user(client):
    """New user should see all badges but none earned"""
    token = await _register(client)
    resp = await client.get("/api/v1/badges", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 15  # 15 badge definitions
    assert all(b["earned"] is False for b in data)


@pytest.mark.asyncio
async def test_check_badges_no_new(client):
    """New user with no progress should earn no badges"""
    token = await _register(client)
    resp = await client.post("/api/v1/badges/check", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["new_badges"] == []


@pytest.mark.asyncio
async def test_badges_require_auth(client):
    resp = await client.get("/api/v1/badges")
    assert resp.status_code == 403
