from httpx import AsyncClient


async def test_register_success(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "login": "testuser",
            "email": "test@test.com",
            "password": "Secret123!@#",
        },
    )
    print(response.json())
    assert response.status_code == 201


async def test_register_duplicate_login(client: AsyncClient):
    data = {
        "login": "duplicate",
        "email": "first@test.com",
        "password": "Secret123!@#",
    }
    await client.post("/auth/register", json=data)

    data["email"] = "second@test.com"
    response = await client.post("/auth/register", json=data)
    assert response.status_code == 409


async def test_register_duplicate_email(client: AsyncClient):
    data = {
        "login": "first",
        "email": "duplicate@test.com",
        "password": "Secret123!@#",
    }
    await client.post("/auth/register", json=data)

    data["login"] = "second"
    response = await client.post("/auth/register", json=data)
    assert response.status_code == 409


class TestLogin:
    async def test_login_success(self, client: AsyncClient):
        await client.post(
            "/auth/register",
            json={
                "login": "loginuser",
                "email": "login@test.com",
                "password": "Secret123!@#",
            },
        )
        response = await client.post(
            "/auth/login",
            json={"login": "loginuser", "password": "Secret123!@#"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    async def test_login_wrong_password(self, client: AsyncClient):
        await client.post(
            "/auth/register",
            json={
                "login": "wrongpass",
                "email": "wrongpass@test.com",
                "password": "Secret123!@#",
            },
        )
        response = await client.post(
            "/auth/login",
            json={"login": "wrongpass", "password": "wrongpassword"},
        )
        assert response.status_code == 401

    async def test_login_nonexistent_user(self, client: AsyncClient):
        response = await client.post(
            "/auth/login",
            json={"login": "nobody", "password": "Secret123!@#"},
        )
        assert response.status_code == 401
