.PHONY: dev format lint lint-fix test migrate makemigrations up up-build down

# ==============================================================================
# Local Development (uv)
# ==============================================================================

dev:
	PYTHONPATH=src uv run fastapi dev src/travel_planner/main.py

format:
	uvx ruff format src/

lint:
	uvx ruff check src/

lint-fix:
	uvx ruff check --fix src/

test:
	uv run pytest

# ==============================================================================
# Database Migrations (alembic)
# ==============================================================================

migrate:
	PYTHONPATH=src uv run alembic upgrade head

# Usage: make makemigrations m="migration message"
makemigrations:
	PYTHONPATH=src uv run alembic revision --autogenerate -m "$(m)"

# ==============================================================================
# Docker Environment
# ==============================================================================

up:
	docker compose up -d

up-build:
	docker compose up --build -d

down:
	docker compose down
