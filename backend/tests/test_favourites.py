import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock

MOCK_STATION = {
    "name": "Test Station",
    "address": "Teststraße 1",
    "isOpen": True,
    "brand": "ARAL",
    "openingTimes": [],
    "overrides": [],
    "wholeDay": False,
}

STATION_ID = "abc123"


@pytest_asyncio.fixture
async def authorized_client(client: AsyncClient) -> AsyncClient:
    await client.post(
        "/auth/register",
        json={
            "login": "favuser",
            "email": "fav@test.com",
            "password": "Secret123!@#",
        },
    )
    response = await client.post(
        "/auth/login",
        json={"login": "favuser", "password": "Secret123!@#"},
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


class TestAddFavourite:
    async def test_add_favourite_success(self, authorized_client: AsyncClient):
        with patch(
            "app.services.tankerkoenig.TankerkoenigService.get_redis_response",
            new=AsyncMock(return_value=[MOCK_STATION]),
        ):
            response = await authorized_client.post(f"/stations/{STATION_ID}/favourite")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Station"
        assert data["address"] == "Teststraße 1"

    async def test_add_favourite_duplicate(self, authorized_client: AsyncClient):
        with patch(
            "app.services.tankerkoenig.TankerkoenigService.get_redis_response",
            new=AsyncMock(return_value=[MOCK_STATION]),
        ):
            await authorized_client.post(f"/stations/{STATION_ID}/favourite")
            response = await authorized_client.post(f"/stations/{STATION_ID}/favourite")
        assert response.status_code == 409

    async def test_add_favourite_unauthorized(self, client: AsyncClient):
        response = await client.post(f"/stations/{STATION_ID}/favourite")
        assert response.status_code == 401


class TestGetFavourites:
    async def test_get_favourites_empty(self, authorized_client: AsyncClient):
        response = await authorized_client.get("/users/me/favourites")
        assert response.status_code == 200
        assert response.json() == []

    async def test_get_favourites_with_data(self, authorized_client: AsyncClient):
        with patch(
            "app.services.tankerkoenig.TankerkoenigService.get_redis_response",
            new=AsyncMock(return_value=[MOCK_STATION]),
        ):
            await authorized_client.post(f"/stations/{STATION_ID}/favourite")

        response = await authorized_client.get("/users/me/favourites")
        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_get_favourites_unauthorized(self, client: AsyncClient):
        response = await client.get("/users/me/favourites")
        assert response.status_code == 401


class TestDeleteFavourite:
    async def test_delete_favourite_success(self, authorized_client: AsyncClient):
        with patch(
            "app.services.tankerkoenig.TankerkoenigService.get_redis_response",
            new=AsyncMock(return_value=[MOCK_STATION]),
        ):
            await authorized_client.post(f"/stations/{STATION_ID}/favourite")

        response = await authorized_client.delete(f"/stations/{STATION_ID}/favourite")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    async def test_delete_favourite_not_found(self, authorized_client: AsyncClient):
        response = await authorized_client.delete(f"/stations/{STATION_ID}/favourite")
        assert response.status_code == 404

    async def test_delete_favourite_unauthorized(self, client: AsyncClient):
        response = await client.delete(f"/stations/{STATION_ID}/favourite")
        assert response.status_code == 401
