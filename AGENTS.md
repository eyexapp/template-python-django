# AGENTS.md — Django REST Framework API

## Project Identity

| Key | Value |
|-----|-------|
| Framework | Django 5 + Django REST Framework |
| Language | Python 3.12 |
| Category | Fullstack API |
| Auth | JWT (simplejwt, email-based login) |
| Database | PostgreSQL (psycopg3) |
| Task Queue | Celery + Redis |
| Package Manager | UV |
| Linting | Ruff + mypy |
| Testing | pytest + pytest-django |
| i18n | Django translations (en, tr) |

---

## Architecture — Django Apps with Service Layer

```
config/                     ← Django project configuration
├── settings/
│   ├── base.py             ← Shared settings
│   ├── dev.py              ← Development overrides
│   ├── prod.py             ← Production security
│   └── test.py             ← Test speed optimizations
├── celery.py               ← Celery app configuration
└── urls.py                 ← Root URL routing (api/v1/*)
apps/                       ← Django applications
├── core/                   ← Shared: abstract models, permissions, pagination
│   ├── models.py           ← BaseModel (UUID pk, timestamps)
│   ├── permissions.py      ← Custom DRF permissions
│   ├── pagination.py       ← Standardized pagination
│   ├── exceptions.py       ← Custom exception handler
│   └── middleware.py       ← Request ID, timing middleware
├── users/                  ← Custom User model (email-based)
│   ├── models.py           ← User, Profile
│   ├── serializers.py      ← Registration, login, profile
│   ├── services.py         ← UserService business logic
│   ├── views.py            ← ViewSets
│   ├── tasks.py            ← Celery async tasks
│   └── urls.py             ← Router registration
└── <app>/                  ← Each new domain app
tests/                      ← Global test directory
deploy/                     ← Deployment scripts
locale/                     ← i18n translation files (en, tr)
```

### Dependency Flow
```
urls.py → views.py → services.py → models.py
                                  → tasks.py (async)
                   → serializers.py (validation + representation)
```

### Strict Layer Rules

| Layer | Can Import From | NEVER Imports |
|-------|----------------|---------------|
| `views.py` | serializers, services, permissions | models directly for writes, tasks |
| `services.py` | models, tasks, external APIs | views, serializers |
| `serializers.py` | models | services, views |
| `tasks.py` | models, services, external APIs | views, serializers |
| `models.py` | core/models | views, services, serializers |

---

## Adding New Code — Where Things Go

### New Django App
1. `python manage.py startapp <name> apps/<name>`
2. Set `name = "apps.<name>"` in `apps.py`
3. Add `"apps.<name>"` to `LOCAL_APPS` in `config/settings/base.py`
4. Inherit models from `apps.core.models.BaseModel`
5. Create `services.py` for business logic
6. Create `tasks.py` for Celery tasks
7. Use `ViewSet` + `Router` in `urls.py`
8. Include in `config/urls.py`: `path("api/v1/", include("apps.<name>.urls"))`
9. Add tests in `apps/<name>/tests/` or `tests/<name>/`
10. Run `python manage.py makemigrations <name>`

### New API Endpoint
1. Add serializer in `serializers.py`
2. Add business logic in `services.py`
3. Add ViewSet method or new ViewSet in `views.py`
4. Register in `urls.py` router

### New Celery Task
1. Define in `apps/<name>/tasks.py`
2. Use `@shared_task` decorator
3. Call from services: `task_name.delay(args)`
4. For periodic: register in `config/celery.py` beat schedule

---

## Design & Architecture Principles

### Service Layer Pattern — Mandatory
```python
# ✅ CORRECT — views delegate to services
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        UserService.create_user(**serializer.validated_data)

# ❌ WRONG — business logic in view
class RegisterView(CreateAPIView):
    def perform_create(self, serializer):
        user = serializer.save()
        send_welcome_email.delay(user.id)  # Logic belongs in service!
```

### BaseModel — All Models Inherit
```python
# ✅ All models inherit from BaseModel
from apps.core.models import BaseModel

class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # BaseModel provides: id (UUID), created_at, updated_at, ordering
```

### Custom User Model — Email-Based
```python
# ✅ Always reference user model indirectly
from django.contrib.auth import get_user_model

User = get_user_model()

# ❌ NEVER import User model directly
from apps.users.models import User  # WRONG
```

### Fat Models, Thin Views, Service Layer
- **Models**: Data, validation, queryset managers
- **Views**: HTTP concerns, permission checks, delegation
- **Services**: Business logic, orchestration, side effects
- **Serializers**: Request validation, response representation

---

## Error Handling

### Custom Exception Handler
```python
# ✅ Consistent error response format
{
    "error": {
        "code": "validation_error",
        "message": "Invalid input data",
        "details": [
            {"field": "email", "message": "Enter a valid email address"}
        ]
    }
}
```

### Raise DRF Exceptions
```python
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied

# ✅ Use DRF exceptions — they integrate with custom exception handler
def get_product(product_id: str) -> Product:
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise NotFound(f"Product {product_id} not found")
```

### Celery Task Error Handling
```python
# ✅ Tasks handle their own errors with retry
@shared_task(bind=True, max_retries=3)
def send_email(self, user_id: str):
    try:
        user = User.objects.get(id=user_id)
        # send email...
    except User.DoesNotExist:
        pass  # User deleted, skip
    except SMTPError as exc:
        self.retry(exc=exc, countdown=60)
```

---

## Code Quality

### Naming Conventions
| Artifact | Convention | Example |
|----------|-----------|---------|
| Apps | snake_case | `apps/user_profiles/` |
| Models | PascalCase singular | `Product`, `OrderItem` |
| Serializers | PascalCase + `Serializer` | `ProductSerializer` |
| Views | PascalCase + `ViewSet` | `ProductViewSet` |
| Services | PascalCase + `Service` | `ProductService` |
| Tasks | snake_case | `send_welcome_email` |
| URLs | kebab-case | `/api/v1/user-profiles/` |
| Settings | UPPER_SNAKE | `SECRET_KEY`, `DATABASE_URL` |

### Migrations
- Always name migrations descriptively: `python manage.py makemigrations --name add_category_to_product`
- Review auto-generated migrations before committing
- Never modify applied migrations

---

## Testing Strategy

### Test Pyramid
| Level | What | Where | Tool |
|-------|------|-------|------|
| Unit | Services, utils, model methods | `tests/unit/` | pytest |
| Integration | Views (API endpoints) | `tests/integration/` | pytest + DRF APIClient |
| Task | Celery tasks | `tests/tasks/` | pytest + eager mode |

### DRF API Testing Pattern
```python
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user)
    return api_client

def test_create_product(auth_client):
    response = auth_client.post('/api/v1/products/', {'name': 'Widget', 'price': '9.99'})
    assert response.status_code == 201
    assert response.data['name'] == 'Widget'
```

### What MUST Be Tested
- All service methods (business logic)
- All API endpoints (status codes, response shapes, permissions)
- All custom model methods and managers
- All serializer validations (valid + invalid)
- All Celery tasks (use `CELERY_ALWAYS_EAGER=True` in test settings)
- All custom permissions

---

## Security & Performance

### Django Security
- `config/settings/prod.py` enables: SECURE_SSL_REDIRECT, SECURE_HSTS, SESSION_COOKIE_SECURE
- CSRF protection on cookie-based endpoints
- All secrets from environment variables (`env("VAR")`)
- `django-cors-headers` with explicit allowed origins

### Auth Security
- JWT access tokens: short-lived (15min)
- JWT refresh tokens: longer-lived (7 days)
- No username field — email is `USERNAME_FIELD`
- Password hashing via Django's PBKDF2

### Performance — Django-Specific
```python
# ✅ Prevent N+1 queries
Product.objects.select_related('category').prefetch_related('tags')

# ✅ Only fetch needed fields
Product.objects.values('id', 'name', 'price')

# ❌ N+1 query pattern
products = Product.objects.all()
for p in products:
    print(p.category.name)  # Triggers separate query per product!
```

### Database Optimization
- Use `select_related()` for ForeignKey / OneToOne
- Use `prefetch_related()` for ManyToMany / reverse FK
- Use `values()` / `only()` when full model not needed
- Use `django-debug-toolbar` in development to spot slow queries
- Index frequently filtered/sorted fields

---

## Commands

| Action | Command |
|--------|---------|
| Install deps | `uv sync` |
| Dev server | `uv run python manage.py runserver` |
| Test | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run mypy .` |
| Migrations | `uv run python manage.py makemigrations` |
| Migrate | `uv run python manage.py migrate` |
| Docker stack | `docker compose up` |

---

## Prohibitions — NEVER Do These

1. **NEVER** put business logic in views — use service layer
2. **NEVER** import User model directly — use `get_user_model()`
3. **NEVER** skip inheriting from `BaseModel` — UUID pk + timestamps required
4. **NEVER** modify applied migrations — create new ones
5. **NEVER** hardcode secrets — use `env("VAR")`
6. **NEVER** write N+1 queries — use `select_related`/`prefetch_related`
7. **NEVER** use `FBV` (function-based views) — use ViewSets
8. **NEVER** skip serializer validation — DRF serializers validate ALL input
9. **NEVER** use synchronous code in Celery tasks for I/O — use task retry
10. **NEVER** commit `.env` or `local.py` settings files
