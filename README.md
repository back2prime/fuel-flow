# fuel-flow

A gas station price aggregator for Germany. Enter an address and search radius — get a list of nearby stations with current fuel prices, powered by the [Tankerkönig API](https://creativecommons.tankerkoenig.de/).

## Stack

- **Python 3.12** · **FastAPI** · **PostgreSQL** · **Redis**
- **SQLAlchemy** (async) · **Alembic** · **httpx** · **Pydantic v2**
- **bcrypt** · **PyJWT** · **Poetry** · **Docker**

## Features

- Search stations by address and radius with live prices
- Redis caching (30 min TTL) to minimize API calls
- JWT-based authentication (register, login, protected routes)
- Save and manage favourite stations per user
- Fully async backend (asyncpg + SQLAlchemy async)

## Project Structure

```
fuel-flow/
├── app/
│   ├── stations/       # Station search endpoints
│   ├── favourites/     # Favourites management
│   ├── users/          # Auth, user profile
│   └── services/       # Tankerkönig API client, utils
├── core/
│   ├── helpers/        # DB, HTTP, Redis, JWT helpers
│   ├── config.py       # Settings (Pydantic BaseSettings)
│   └── constants.py
├── alembic/            # Database migrations
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- A Tankerkönig API key — get one free at [creativecommons.tankerkoenig.de](https://creativecommons.tankerkoenig.de/)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/back2prime/fuel-flow.git
cd fuel-flow
```

2. Create a `.env` file based on the example:

```bash
cp .env.example .env
```

3. Fill in your values in `.env`:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
DB_NAME=fuel_flow
REDIS_URL=redis://redis:6379/0
API_KEY=your_tankerkoenig_api_key
```

4. Start all services:

```bash
docker-compose up --build
```

5. Apply database migrations:

```bash
docker-compose exec app alembic upgrade head
```

6. Open the interactive API docs:

```
http://localhost:8000/docs
```

## API Overview

### Stations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/stations` | Search stations by address + radius |
| POST | `/stations/{station_id}` | Get details for a specific station |

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new account |
| POST | `/auth/login` | Login and receive a JWT token |
| POST | `/auth/logout` | Stateless logout (client deletes token) |

### User (protected)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user profile |
| PATCH | `/users/me` | Update profile |
| PATCH | `/users/me/password` | Change password |
| DELETE | `/users/me` | Delete account |

### Favourites (protected)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/stations/{station_id}/favourite` | Add station to favourites |
| DELETE | `/stations/{station_id}/favourite` | Remove from favourites |
| GET | `/users/me/favourites` | List saved favourites |

## Authentication

Send the JWT token returned from `/auth/login` as a Bearer token:

```
Authorization: Bearer <token>
```

Tokens expire after 30 minutes.

## Local Development (without Docker)

1. Install dependencies:

```bash
poetry install
```

2. Update `.env` — set `DB_HOST=localhost` and `REDIS_URL=redis://localhost:6379/0`

3. Run the app:

```bash
poetry run uvicorn app.main:app --reload
```

## License

MIT