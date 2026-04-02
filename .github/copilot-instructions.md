# Python Django — Copilot Instructions

## Project Overview

Production-ready Django REST Framework API template with JWT authentication,
Celery task queue, and PostgreSQL.

## Architecture

- **Framework**: Django 5 + Django REST Framework
- **Auth**: JWT via `djangorestframework-simplejwt` (email-based login, no username)
- **Database**: PostgreSQL (psycopg3), SQLite fallback for dev
- **Task Queue**: Celery + Redis broker, django-celery-beat for periodic tasks
- **Package Manager**: UV (fast Python package manager)

## Project Layout

```
config/              # Django project configuration
  settings/
    base.py          # Shared settings
    dev.py           # Development overrides
    prod.py          # Production security settings
    test.py          # Test speed optimizations
  celery.py          # Celery app configuration
  urls.py            # Root URL routing
apps/                # Django applications
  core/              # Shared: abstract models, permissions, pagination, exceptions, middleware
  users/             # Custom User model, auth endpoints, profile management
tests/               # Global test directory
deploy/              # Deployment scripts (entrypoint.sh)
locale/              # i18n translation files (en, tr)
```

## Key Conventions

### Service Layer Pattern
Business logic lives in `services.py`, NOT in views or serializers.
Views delegate to services; serializers handle validation and representation.

```python
# ✅ Correct — view calls service
class RegisterView(CreateAPIView):
    def perform_create(self, serializer):
        UserService.create_user(**serializer.validated_data)

# ❌ Wrong — logic in view
class RegisterView(CreateAPIView):
    def perform_create(self, serializer):
        user = serializer.save()
        send_welcome_email.delay(user.id)
```

### Adding a New App

1. Create app: `python manage.py startapp <name> apps/<name>`
2. Set `name = "apps.<name>"` in `apps.py`
3. Add `"apps.<name>"` to `LOCAL_APPS` in `config/settings/base.py`
4. Inherit models from `apps.core.models.BaseModel`
5. Create `services.py` for business logic
6. Create `tasks.py` for Celery tasks
7. Use `ViewSet` + `Router` in `urls.py`
8. Include in `config/urls.py`: `path("api/v1/", include("apps.<name>.urls"))`
9. Add tests in `apps/<name>/tests/`

### Custom User Model
User model uses **email** as `USERNAME_FIELD`. No username field exists.
Always use `get_user_model()` to reference the user model.

### Abstract Base Models
All models should inherit from `apps.core.models.BaseModel` which provides:
- `id` — UUID primary key
- `created_at` — auto-set on create
- `updated_at` — auto-set on save
- Default ordering by `-created_at`

### API Response Format
Errors use a consistent format via custom exception handler:
```json
{"error": {"code": "validation_error", "message": "...", "details": [...]}}
```

### Settings
- Environment variables loaded via `django-environ` from `.env`
- Never hardcode secrets — use `env("VAR_NAME")`
- `DJANGO_SETTINGS_MODULE` determines active settings file

## Commands

```bash
uv sync                              # Install dependencies
uv run python manage.py runserver    # Dev server
uv run pytest                        # Run tests
uv run ruff check .                  # Lint
uv run ruff format .                 # Format
uv run mypy .                        # Type check
docker compose up                    # Full stack (app + postgres + redis + celery)
```
