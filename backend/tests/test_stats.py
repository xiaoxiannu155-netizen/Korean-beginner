"""Tests for personal stats API"""
import uuid
import pytest


async def _register(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": f"stat{uuid.uuid4().hex[:8]}@example.com",
        "username": "stat_tester", "password": "testpass123",
    })
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_personal_stats_authenticated(client):
    """Authenticated user should get personal stats"""
    token = await _register(client)
    resp = await client.get("/api/v1/stats/personal",
                             headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert "total_xp" in data
    assert "level" in data
    assert "streak_days" in data
    assert "stage" in data
    assert "completion_percentage" in data


@pytest.mark.asyncio
async def test_stats_require_auth(client):
    """Stats should require authentication"""
    resp = await client.get("/api/v1/stats/personal")
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_initial_stats_defaults(client):
    """New user stats should have correct defaults"""
    token = await _register(client)
    resp = await client.get("/api/v1/stats/personal",
                             headers={"Authorization": f"Bearer {token}"})
    data = resp.json()
    assert data["total_xp"] == 0
    assert data["level"] == 1
    assert data["streak_days"] == 0
    assert data["stage"] == 1
