import pytest


@pytest.mark.asyncio
async def test_get_me_authenticated(client):
    # register + get token
    resp = await client.post("/api/v1/auth/register", json={
        "email": "me@example.com",
        "username": "me",
        "password": "testpass123",
    })
    token = resp.json()["access_token"]

    resp = await client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "me@example.com"


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client):
    resp = await client.get("/api/v1/users/me")
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_get_progress_initial(client):
    resp = await client.post("/api/v1/auth/register", json={
        "email": "progress@example.com",
        "username": "prog",
        "password": "testpass123",
    })
    token = resp.json()["access_token"]

    resp = await client.get(
        "/api/v1/users/me/progress",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["stage"] == 1
    assert data["total_xp"] == 0
    assert data["streak_days"] == 0
    assert data["joy_name"] == "Joy"
