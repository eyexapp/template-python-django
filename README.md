# Python Django — Master Template

Production-ready Django REST Framework API template with JWT authentication,
Celery task queue, PostgreSQL, and Docker support.

## Features

- **Django 5** with Django REST Framework
- **JWT Authentication** — email-based login via `simplejwt`
- **Custom User Model** — email as username, no username field
- **Service Layer Pattern** — business logic separated from views
- **Celery + Redis** — async task queue with periodic task support
- **PostgreSQL** — production database (SQLite fallback for dev)
- **Docker Compose** — full stack: app, postgres, redis, celery worker/beat
- **Settings Split** — base / dev / prod / test configurations
- **Testing** — pytest-django with fixtures, factory-boy ready
- **Code Quality** — ruff linter+formatter, mypy strict with django-stubs
- **CI/CD** — GitHub Actions (lint, test matrix, Docker build)
- **i18n** — English + Turkish locale support
- **API Standards** — consistent error format, UUID primary keys, pagination

## Quick Start

### Prerequisites

- Python 3.11+
- [UV](https://docs.astral.sh/uv/) package manager

### Local Development

```bash
# Install dependencies
uv sync

# Copy environment file
cp .env.example .env

# Run migrations (SQLite in dev)
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser

# Start dev server
uv run python manage.py runserver
```

### Docker (Full Stack)

```bash
docker compose up --build
```

This starts: Django app, PostgreSQL, Redis, Celery worker, Celery beat.

## Project Structure

```
├── apps/
│   ├── core/                   # Shared utilities
│   │   ├── models.py           # Abstract base models (UUID, timestamps)
│   │   ├── permissions.py      # IsOwner permission
│   │   ├── pagination.py       # Standard pagination
│   │   ├── exceptions.py       # Custom exception handler
│   │   └── middleware.py       # Request ID middleware
│   └── users/                  # User management
│       ├── models.py           # Custom User (email-based)
│       ├── serializers.py      # Register, Profile, ChangePassword
│       ├── views.py            # RegisterView, UserViewSet
│       ├── services.py         # Business logic (UserService)
│       ├── tasks.py            # Celery tasks
│       └── urls.py             # Router + auth endpoints
├── config/
│   ├── settings/
│   │   ├── base.py             # Shared settings
│   │   ├── dev.py              # Development (DEBUG, SQLite)
│   │   ├── prod.py             # Production (security headers)
│   │   └── test.py             # Test optimizations
│   ├── celery.py               # Celery configuration
│   ├── urls.py                 # Root URL routing
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point
├── deploy/
│   └── entrypoint.sh           # Docker entrypoint (wait DB → migrate → serve)
├── tests/                      # Global tests
├── locale/                     # i18n (en, tr)
├── Dockerfile                  # Multi-stage production build
├── docker-compose.yml          # Dev stack definition
├── pyproject.toml              # Dependencies & tool config
└── .github/
    ├── workflows/ci.yml        # CI pipeline
    └── copilot-instructions.md # AI assistant context
```

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/health/` | No | Health check |
| `POST` | `/api/v1/auth/register/` | No | User registration |
| `POST` | `/api/v1/auth/token/` | No | Obtain JWT tokens |
| `POST` | `/api/v1/auth/token/refresh/` | No | Refresh access token |
| `GET` | `/api/v1/users/me/` | Yes | Get current user profile |
| `PATCH` | `/api/v1/users/me/` | Yes | Update profile |
| `POST` | `/api/v1/users/me/change-password/` | Yes | Change password |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SETTINGS_MODULE` | `config.settings.dev` | Active settings |
| `DJANGO_SECRET_KEY` | — | Secret key (required in prod) |
| `DJANGO_DEBUG` | `True` | Debug mode |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Allowed hosts |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | Celery broker |
| `CORS_ALLOWED_ORIGINS` | — | Comma-separated origins |

## Adding a New App

```bash
# 1. Create the app
uv run python manage.py startapp products apps/products

# 2. Update apps/products/apps.py
class ProductsConfig(AppConfig):
    name = "apps.products"

# 3. Add to config/settings/base.py LOCAL_APPS
LOCAL_APPS = [
    "apps.core",
    "apps.users",
    "apps.products",  # ← new
]

# 4. Create models inheriting from BaseModel
from apps.core.models import BaseModel

class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

# 5. Create services.py, tasks.py, serializers.py, views.py, urls.py
# 6. Include in config/urls.py
# 7. Add tests in apps/products/tests/
```

## Commands

```bash
# Development
uv run python manage.py runserver         # Start dev server
uv run python manage.py makemigrations    # Generate migrations
uv run python manage.py migrate           # Apply migrations
uv run python manage.py createsuperuser   # Create admin user

# Testing
uv run pytest                             # Run all tests
uv run pytest --cov                       # With coverage

# Code Quality
uv run ruff check .                       # Lint
uv run ruff format .                      # Format
uv run mypy .                             # Type check

# Docker
docker compose up --build                 # Start full stack
docker compose down -v                    # Stop & clean volumes

# Celery (local, without Docker)
celery -A config worker -l info           # Start worker
celery -A config beat -l info             # Start beat scheduler
```

## Tech Stack

| Category | Tool |
|----------|------|
| Framework | Django 5, DRF |
| Auth | JWT (simplejwt) |
| Database | PostgreSQL (psycopg3) |
| Task Queue | Celery + Redis |
| Static Files | WhiteNoise |
| Package Manager | UV |
| Linter/Formatter | Ruff |
| Type Checker | Mypy (django-stubs) |
| Testing | pytest-django, factory-boy |
| CI/CD | GitHub Actions |
| Container | Docker + Compose |

