#!/usr/bin/env bash
set -euo pipefail

echo "⏳ Waiting for database..."
python << 'EOF'
import sys, time, environ

env = environ.Env()
environ.Env.read_env(".env", overwrite=True)

db_url = env("DATABASE_URL", default="")
if "postgres" not in db_url:
    print("No Postgres URL found — skipping wait")
    sys.exit(0)

import psycopg
for i in range(30):
    try:
        conn = psycopg.connect(db_url)
        conn.close()
        print("✅ Database is ready")
        sys.exit(0)
    except psycopg.OperationalError:
        print(f"  Attempt {i+1}/30 — database not ready, retrying...")
        time.sleep(1)

print("❌ Database connection timed out")
sys.exit(1)
EOF

echo "🔄 Running migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting server..."
exec "$@"
