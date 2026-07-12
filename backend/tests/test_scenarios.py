import pytest


@pytest.mark.asyncio
async def test_list_scenarios(client):
    resp = await client.get("/api/v1/scenarios")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 10
    assert data[0]["id"] == "cafe"


@pytest.mark.asyncio
async def test_get_scenario_detail(client):
    resp = await client.get("/api/v1/scenarios/cafe")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "☕ 买咖啡"
    assert "context" in data
    assert "starter" in data
    assert "tips" in data


@pytest.mark.asyncio
async def test_scenario_404(client):
    resp = await client.get("/api/v1/scenarios/nonexistent")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_scenario_chat_cafe(client):
    resp = await client.post("/api/v1/scenarios/cafe/chat", json={"message": "아메리카노 한 잔 주세요"})
    assert resp.status_code == 200
    data = resp.json()
    assert "reply" in data
    assert "reply_zh" in data


@pytest.mark.asyncio
async def test_scenario_chat_empty_message(client):
    resp = await client.post("/api/v1/scenarios/cafe/chat", json={"message": ""})
    assert resp.status_code == 400
