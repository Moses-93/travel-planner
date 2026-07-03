# Travel Planner API

A RESTful API for managing travel projects and places, built strictly adhering to Clean Architecture and Domain-Driven Design (DDD) principles.

## System Architecture

The application is structured in isolated layers, following the Dependency Rule:

- **Domain (`src/travel_planner/domain`)**: Pure Python entities (`TravelProject`, `TravelPlace`) and domain-specific exceptions. Encapsulates core business invariants (e.g., maximum 10 places per project, uniqueness, deletion protection if places are visited).
- **Application (`src/travel_planner/application`)**: Use cases (interactors) orchestrating domain logic. Defines DTOs and abstract interfaces (Ports) for repositories and external gateways.
- **Infrastructure (`src/travel_planner/infrastructure`)**: Adapters implementing application interfaces. Contains async SQLAlchemy 2.0 repositories and an HTTPX-based gateway integrating with the Art Institute of Chicago API.
- **Presentation (`src/travel_planner/api`)**: FastAPI controllers, Pydantic schemas, and centralized exception handling that maps domain errors to standard HTTP status codes.

## Tech Stack

- **Framework**: FastAPI (Python 3.12+)
- **Database**: PostgreSQL
- **ORM & Migrations**: SQLAlchemy 2.0 (Async) + Alembic
- **Package Manager**: `uv`

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Or locally: Python 3.12+, `uv`, and PostgreSQL

### Setup

1. Clone the repository.
2. Initialize environment variables:

   ```bash
   cp .env.example .env
   ```

### Running with Docker (Recommended)

Launch the API and PostgreSQL container:

```bash
make up-build
```

The API is available at: `http://localhost:8000`

Stop services:

```bash
make down
```

### Running Locally

1. Ensure PostgreSQL is running on `localhost:5432` and `.env` is adjusted.
2. Sync dependencies:

   ```bash
   uv sync
   ```

3. Run database migrations:

   ```bash
   make migrate
   ```

4. Start the development server:

   ```bash
   make dev
   ```

## API Documentation

FastAPI provides automatic OpenAPI documentation. Once running, access:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

All endpoints, DTOs, and HTTP error responses are self-documented here, replacing the need for an external Postman collection.

## Development Workflow

Available `make` commands:

- `make lint` / `make format` - Code formatting and linting via `ruff`.
- `make makemigrations m="description"` - Generate new Alembic migration.
- `make migrate` - Apply pending migrations.
