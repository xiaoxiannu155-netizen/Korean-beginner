import pytest


@pytest.mark.asyncio
async def test_evaluate_simple_text(client):
    resp = await client.post("/api/v1/speech/evaluate", json={"text": "사랑해요"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["target_text"] == "사랑해요"
    assert 0 <= data["overall_score"] <= 1
    assert len(data["syllable_scores"]) == 4
    assert len(data["feedback"]) >= 1
    assert "xp_earned" in data


@pytest.mark.asyncio
async def test_evaluate_with_tolerance(client):
    resp = await client.post("/api/v1/speech/evaluate", json={"text": "안녕하세요", "difficulty_tolerance": 0.8})
    assert resp.status_code == 200
    assert len(resp.json()["feedback"]) >= 1


@pytest.mark.asyncio
async def test_evaluate_empty_text(client):
    resp = await client.post("/api/v1/speech/evaluate", json={"text": ""})
    data = resp.json()
    assert data["overall_score"] == 0


@pytest.mark.asyncio
async def test_tips_endpoint(client):
    resp = await client.get("/api/v1/speech/tips/한국어")
    assert resp.status_code == 200
    data = resp.json()
    assert data["text"] == "한국어"
    assert "tips" in data
