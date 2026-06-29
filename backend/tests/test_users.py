import pytest_asyncio
import pytest
from httpx import AsyncClient


@pytest_asyncio.fixture
async def authorized_client(client: AsyncClient) -> AsyncClient:
    await client.post(
        "/auth/register",
        json={
            "login": "meuser",
            "email": "me@test.com",
            "password": "Secret123!@#",
        },
    )
    response = await client.post(
        "/auth/login",
        json={"login": "meuser", "password": "Secret123!@#"},
    )
    token = response.cookies.get("access_token")
    client.cookies.set("access_token", token)
    return client


class TestGetMe:
    async def test_get_me_success(self, authorized_client: AsyncClient):
        response = await authorized_client.get("/users/me")
        assert response.status_code == 200
        data = response.json()
        assert data["login"] == "meuser"
        assert data["email"] == "me@test.com"

    async def test_get_me_unauthorized(self, client: AsyncClient):
        response = await client.get("/users/me")
        assert response.status_code == 401


class TestPatchMe:
    async def test_patch_me_success(self, authorized_client: AsyncClient):
        response = await authorized_client.patch(
            "/users/me",
            json={"name": "Alex", "surname": "Test"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alex"
        assert data["surname"] == "Test"


class TestPatchPassword:
    async def test_patch_password_success(self, authorized_client: AsyncClient):
        response = await authorized_client.patch(
            "/users/me/password",
            json={"old_password": "Secret123!@#", "new_password": "NewPass456!@#"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    async def test_patch_password_wrong_old(self, authorized_client: AsyncClient):
        response = await authorized_client.patch(
            "/users/me/password",
            json={"old_password": "wrongpass", "new_password": "NewPass456!@#"},
        )
        assert response.status_code == 401


class TestDeleteMe:
    async def test_delete_me_success(self, authorized_client: AsyncClient):
        response = await authorized_client.delete("/users/me")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

        # после удаления токен в blacklist → 401
        response = await authorized_client.get("/users/me")
        assert response.status_code == 403
