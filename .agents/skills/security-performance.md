---
name: security-performance
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - security
  - performance
  - query optimization
  - n+1
  - csrf
  - authentication
---

# Security & Performance — Django 5

## Performance

### Query Optimization

```python
# N+1 prevention
User.objects.select_related("profile")     # FK (single JOIN)
User.objects.prefetch_related("orders")    # M2M/reverse (separate query)

# Only fetch needed fields
User.objects.only("id", "email")
User.objects.values_list("email", flat=True)

# Count without loading objects
User.objects.filter(active=True).count()
```

### Database Indexes

```python
class Meta:
    indexes = [
        models.Index(fields=["email"]),
        models.Index(fields=["-created_at"]),
        models.Index(fields=["status", "created_at"]),  # compound
    ]
```

### Caching

```python
from django.core.cache import cache

def get_popular_products():
    key = "popular_products"
    result = cache.get(key)
    if result is None:
        result = Product.objects.filter(sales__gt=100).values()[:10]
        cache.set(key, list(result), timeout=300)
    return result
```

### Pagination

- Always paginate list endpoints — `PageNumberPagination` default.
- `CursorPagination` for large datasets (no COUNT query).

## Security

### Authentication — JWT

```python
# config/settings/base.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### CSRF / CORS

- DRF API views exempt from CSRF via `SessionAuthentication`.
- Use `django-cors-headers` — whitelist specific origins only.
- Never `CORS_ALLOW_ALL_ORIGINS = True` in production.

### SQL Injection — Prevented by ORM

- Django ORM parameterizes all queries automatically.
- If using `raw()` or `extra()`, use parameterized args.
- **Never** f-string SQL: `User.objects.raw(f"SELECT ... {user_input}")`.

### Secrets & Settings

- `SECRET_KEY` from environment variable.
- `django-environ` or `pydantic-settings` for env vars.
- `python manage.py check --deploy` for security audit.

### Permissions

```python
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
```
