# Library API
Library management API built with FastAPI, PostgreSQL and Docker Compose.

## Features

- Add new books
- Delete books
- List all books
- Borrow books
- Return books

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker Compose
- Pytest

## Run Project

```bash
docker compose up --build
```

## API Documentation

Available at:

```bash
http://localhost:8000/docs
```

## Run Tests

```bash
pytest
```

## Example books

```json
{
  "serial_number": "100001",
  "title": "Clean Code",
  "author": "Robert C. Martin"
}
```

```json
{
  "serial_number": "100002",
  "title": "The Pragmatic Programmer",
  "author": "Andrew Hunt"
}
```

```json
{
  "serial_number": "100003",
  "title": "Design Patterns",
  "author": "Erich Gamma"
}
```