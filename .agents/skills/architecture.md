---
name: architecture
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - architecture
  - django
  - app
  - model
  - service layer
  - drf
  - celery
---

# Architecture — Django 5 + DRF

## App-Based Structure

```
project/
├── manage.py
├── pyproject.toml
├── config/               ← Project settings (renamed from project/)
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── apps/
│   ├── users/
│   │   ├── models.py     ← Django ORM models
│   │   ├── services.py   ← Business logic (NOT in views)
│   │   ├── selectors.py  ← Complex queries
│   │   ├── serializers.py ← DRF serializers
│   │   ├── views.py      ← DRF ViewSets/APIViews
│   │   ├── urls.py       ← URL patterns
│   │   ├── admin.py      ← Django Admin config
│   │   ├── tasks.py      ← Celery tasks
│   │   └── tests/
│   └── orders/
└── tests/
```

## Service Layer Pattern

Business logic lives in `services.py`, NOT in views or serializers:

```python
# apps/users/services.py
from apps.users.models import User

def create_user(*, name: str, email: str) -> User:
    """Create user with validation and side effects."""
    if User.objects.filter(email=email).exists():
        raise DuplicateEmailError(email)
    user = User.objects.create(name=name, email=email)
    send_welcome_email.delay(user.id)  # Celery task
    return user
```

- Views call services, services call ORM.
- Views handle HTTP, services handle business logic.
- Use keyword-only arguments (`*`) for explicit calls.

## Django REST Framework

```python
# apps/users/views.py
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Delegate to service layer
        user = create_user(**serializer.validated_data)
        serializer.instance = user
```

## Celery (Async Tasks)

```python
# apps/users/tasks.py
@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_id: int):
    user = User.objects.get(id=user_id)
    EmailService.send(to=user.email, template="welcome")
```

- Long-running work → Celery task (emails, reports, webhooks).
- Redis as broker and result backend.

## Rules

- No business logic in views/serializers — use services.
- No raw SQL — use Django ORM (or `selectors.py` for complex queries).
- One Django app per domain (users, orders, payments).
- Custom User model from day one: `AUTH_USER_MODEL`.
