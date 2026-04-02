---
name: code-quality
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - clean code
  - naming
  - lint
  - model
  - serializer
  - migration
---

# Code Quality — Django 5 + DRF

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| App | singular snake_case | `user`, `order` |
| Model | singular PascalCase | `User`, `OrderItem` |
| Serializer | Model + Serializer | `UserSerializer` |
| ViewSet | Model + ViewSet | `UserViewSet` |
| Service function | verb_noun | `create_user()` |
| Selector function | get/filter prefix | `get_active_users()` |
| Task | verb_noun | `send_welcome_email` |
| URL name | app:action-resource | `users:detail` |

## Model Best Practices

```python
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["email"])]

    def __str__(self) -> str:
        return self.name
```

- Always define `__str__`.
- Add `created_at` / `updated_at` timestamps.
- Use `Meta.indexes` for query optimization.
- No business logic in models — only data validation (`clean()`).

## Serializer Patterns

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "created_at"]
        read_only_fields = ["id", "created_at"]
```

- Explicit `fields` — NEVER use `fields = "__all__"`.
- Separate Create/Update serializers when input differs from output.

## Migrations

- `python manage.py makemigrations` — generate from model changes.
- `python manage.py migrate` — apply migrations.
- Migrations are committed to git — never `.gitignore` them.
- Squash when migration count gets excessive.

## Linting

- Ruff for linting + formatting.
- `django-stubs` for mypy type checking.
- `DJ` rules in Ruff for Django-specific checks.
