format:
	uv run ruff format .
	uv run ruff check . --fix

dev:
	uv run uvicorn app.main:app --reload

worker:
	uv run celery -A app.celery worker --pool=threads -c 2

# Alembic helpers
# Create a new migration (pass message with m="message").
# Example: make alembic-create m="create users table"
alembic-create:
	uv run alembic revision --autogenerate -m "$(m)"

# Apply migrations to the latest head
# Example: make alembic-up
alembic-up:
	uv run alembic upgrade head

# Rollback migrations. By default rolls back one revision (REV=-1).
# Example: make alembic-down REV=-1  or make alembic-down REV=base
alembic-down:
	uv run alembic downgrade $(REV)