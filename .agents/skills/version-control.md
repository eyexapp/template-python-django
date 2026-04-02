---
name: version-control
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - git
  - commit
  - ci
  - deploy
  - docker
---

# Version Control — Django 5

## Commits (Conventional)

- `feat(users): add password reset service`
- `fix(orders): handle race condition in stock check`
- `db(users): add email index migration`

## CI Pipeline

1. `uv sync`
2. `uv run ruff check .` + `ruff format --check .`
3. `uv run mypy apps/`
4. `uv run pytest --cov`
5. `python manage.py check --deploy` — Django deployment checklist
6. `python manage.py makemigrations --check` — no unmigrated changes

## .gitignore

```
__pycache__/
*.pyc
.venv/
.env
db.sqlite3
media/
staticfiles/
htmlcov/
```

## Docker

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000"]
```

## Deployment Checklist

- `DEBUG = False` in production.
- `ALLOWED_HOSTS` set explicitly.
- `SECURE_SSL_REDIRECT = True`.
- `python manage.py check --deploy` passes all checks.
