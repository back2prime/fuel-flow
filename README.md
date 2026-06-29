# fuel-flow

A gas station price aggregator for Germany. Enter an address and search radius — get a list of nearby stations with current fuel prices, powered by the Tankerkönig API.

**Live demo:** https://fuel-flow-eta.vercel.app

---

## Stack

### Backend
Python 3.12 · FastAPI · PostgreSQL · Redis
SQLAlchemy (async) · Alembic · httpx · Pydantic v2
bcrypt · PyJWT · Poetry · Docker · resend

### Frontend
React 19 · Vite · Tailwind CSS v4
React Router v7 · Axios

---

## Features

- Search stations by address and radius with live prices
- Redis caching (30 min TTL) to minimize API calls
- JWT authentication stored in httpOnly cookies (XSS-safe)
- Redis token blacklist — logout invalidates token server-side
- Rate limiting on auth and station endpoints via slowapi
- Password strength validation (length, uppercase, lowercase, digit, special character)
- Save and manage favourite stations per user
- Forgot / reset password flow via email (Resend)
- Full user profile management (edit info, change password, delete account)
- Global 401 interceptor — auto-redirect to login on expired token
- Fully async backend (asyncpg + SQLAlchemy async)
- 21 passing tests, 83% coverage

---

## Project Structure

```
fuel-flow/
├── backend/
│   ├── app/
│   │   ├── database/           # DB session dependency
│   │   ├── stations/           # Station search endpoints
│   │   ├── favourites/         # Favourites management
│   │   ├── users/              # Auth, user profile
│   │   └── services/           # Tankerkönig API client, utils
│   ├── core/
│   │   ├── helpers/            # DB, HTTP, Redis, JWT, Email, Limiter helpers
│   │   ├── models/             # SQLAlchemy base model
│   │   ├── schemes/            # Shared Pydantic schemas
│   │   ├── templates/          # HTML email templates
│   │   ├── middleware.py       # Body size limit middleware
│   │   ├── config.py           # Settings (Pydantic BaseSettings)
│   │   └── constants.py
│   ├── alembic/                # Database migrations
│   ├── tests/                  # pytest test suite
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/                # Axios client with 401 interceptor
│   │   ├── components/         # Navbar
│   │   └── pages/              # SearchPage, LoginPage, RegisterPage,
│   │                           # FavouritesPage, ProfilePage,
│   │                           # ForgotPasswordPage, ResetPasswordPage
│   ├── index.html
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- A Tankerkönig API key — get one free at [creativecommons.tankerkoenig.de](https://creativecommons.tankerkoenig.de)
- A Resend account for password reset emails — [resend.com](https://resend.com)

### Setup

Clone the repository:
```bash
git clone https://github.com/back2prime/fuel-flow.git
cd fuel-flow
```

Create a `.env` file:
```bash
cp backend/.env.example backend/.env
```

Fill in your values in `backend/.env`:
```env
API_KEY=your_tankerkoenig_api_key
REDIS_URL=redis://redis:6379/0
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
DB_NAME=fuel_flow
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=fuel_flow
ALLOWED_ORIGINS=["http://localhost:5173","https://your-frontend-url.vercel.app"]
RESEND_API_KEY=your_resend_api_key
FRONTEND_URL=https://your-frontend-url.vercel.app
FROM_EMAIL=onboarding@resend.dev
```

Start all backend services:
```bash
docker-compose up --build
```

Apply database migrations:
```bash
docker-compose exec app alembic upgrade head
```

Start the frontend dev server:
```bash
cd frontend
npm install
npm run dev
```

Open the app: http://localhost:5173  
API docs: http://localhost:8000/docs

---

## API Overview

### Stations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/stations?limit=N` | Search stations by address + radius |
| POST | `/stations/{station_id}` | Get details for a specific station |

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new account |
| POST | `/auth/login` | Login — JWT set as httpOnly cookie |
| POST | `/auth/logout` | Invalidate token via Redis blacklist |
| POST | `/auth/forgot-password` | Send password reset email |
| POST | `/auth/reset-password` | Reset password using token from email |

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

---

## Authentication

JWT tokens are stored in httpOnly cookies — inaccessible to JavaScript, protected against XSS attacks. The cookie is set automatically on login and cleared on logout.

Tokens expire after 30 minutes. Logout invalidates the token server-side via a Redis blacklist.

---

## Running Tests

```bash
docker-compose exec app pytest tests/ --cov=app --cov-report=term-missing
```

> **Note (Windows):** stop the local PostgreSQL service before running tests to avoid port conflicts:
> ```
> Stop-Service postgresql-x64-18
> ```

---

## Deployment

| Service | Platform |
|---------|----------|
| Backend (FastAPI) | Railway |
| PostgreSQL | Railway |
| Redis | Railway |
| Frontend (React) | Vercel |

---

## License

MIT