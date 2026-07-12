import uuid
import pytest


async def _register(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": f"ai{uuid.uuid4().hex[:8]}@example.com", "username": "ai_tester", "password": "testpass123",
    })
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_translate_zh_to_ko_cached(client):
    resp = await client.post("/api/v1/ai/translate", json={"text": "你好", "direction": "zh-ko"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] == "안녕하세요"
    assert data["pronunciation"] == "an-nyeong-ha-se-yo"
    assert "audio_url" in data


@pytest.mark.asyncio
async def test_translate_uncached(client):
    resp = await client.post("/api/v1/ai/translate", json={"text": "完全陌生的短语", "direction": "zh-ko"})
    assert resp.status_code == 200
    assert resp.json()["source"] == "fallback"


@pytest.mark.asyncio
async def test_search_korean(client):
    resp = await client.get("/api/v1/ai/search?q=你好")
    assert resp.status_code == 200
    data = resp.json()
    assert data["korean"] == "안녕하세요"


@pytest.mark.asyncio
async def test_pronounce_breakdown(client):
    resp = await client.get("/api/v1/ai/pronounce/사랑해요")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["breakdown"]) == 4
    assert data["breakdown"][0]["syllable"] == "사"


@pytest.mark.asyncio
async def test_pronounce_with_speed(client):
    resp = await client.get("/api/v1/ai/pronounce/감사합니다?speed=0.5&gender=female")
    assert resp.status_code == 200
    data = resp.json()
    assert data["speed"] == 0.5
    assert data["slow_audio_url"] is None  # already slow, so no slow version
