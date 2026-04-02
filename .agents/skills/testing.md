---
name: testing
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - test
  - pytest
  - factory
  - fixture
  - api test
---

# Testing — Django 5 (pytest-django + FactoryBoy)

## Config

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
addopts = "-ra --strict-markers --reuse-db"
```

## Factory Boy

```python
# apps/users/tests/factories.py
import factory
from apps.users.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    name = factory.Faker("name")
    email = factory.LazyAttribute(lambda o: f"{o.name.lower().replace(' ', '.')}@test.com")
```

## Service Testing

```python
def test_create_user(db):
    user = create_user(name="Alice", email="alice@test.com")
    assert user.name == "Alice"
    assert User.objects.count() == 1

def test_create_user_duplicate_email(db):
    UserFactory(email="alice@test.com")
    with pytest.raises(DuplicateEmailError):
        create_user(name="Bob", email="alice@test.com")
```

## API Testing

```python
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

def test_list_users(api_client, db):
    UserFactory.create_batch(3)
    response = api_client.get("/api/users/")
    assert response.status_code == 200
    assert len(response.data) == 3

def test_create_user_unauthenticated(api_client, db):
    response = api_client.post("/api/users/", {"name": "Alice"})
    assert response.status_code == 401
```

## Celery Task Testing

```python
@pytest.mark.django_db
def test_send_welcome_email(mocker):
    mock_send = mocker.patch("apps.users.tasks.EmailService.send")
    user = UserFactory()
    send_welcome_email(user.id)
    mock_send.assert_called_once()
```

## Rules

- Use `FactoryBoy` for data creation — not raw `Model.objects.create()`.
- Test services directly, then test API endpoints.
- Use `pytest-django`'s `db` fixture — don't use `TestCase`.
- `@pytest.mark.django_db` for tests that need database.
