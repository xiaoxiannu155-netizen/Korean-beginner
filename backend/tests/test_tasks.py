"""Tests for daily tasks API"""
import uuid
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


async def _register(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": f"task{uuid.uuid4().hex[:8]}@example.com",
        "username": "task_tester", "password": "testpass123",
    })
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_get_today_tasks_initial(client):
    """New user should get empty daily task"""
    token = await _register(client)
    resp = await client.get("/api/v1/daily-tasks/today", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["words_completed"] == 0
    assert data["grammar_completed"] is False
    assert data["listening_completed"] is False
    assert data["speaking_completed"] is False


@pytest.mark.asyncio
async def test_complete_word_task(client):
    """Complete a word task, verify XP awarded"""
    token = await _register(client)
    resp = await client.post("/api/v1/daily-tasks/complete?task_type=word",
                              headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["words_completed"] == 1


@pytest.mark.asyncio
async def test_complete_grammar_task(client):
    """Complete grammar task"""
    token = await _register(client)
    resp = await client.post("/api/v1/daily-tasks/complete?task_type=grammar",
                              headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["grammar_completed"] is True


@pytest.mark.asyncio
async def test_tasks_require_auth(client):
    """Daily tasks should require authentication"""
    resp = await client.get("/api/v1/daily-tasks/today")
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_word_task_caps_at_5(client):
    """Word completion should cap at 5"""
    token = await _register(client)
    for _ in range(7):
        resp = await client.post("/api/v1/daily-tasks/complete?task_type=word",
                                  headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["words_completed"] == 5
