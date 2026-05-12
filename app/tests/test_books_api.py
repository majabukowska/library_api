import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.dependencies import get_db
from app.main import app


TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_create_book(client: TestClient):
    response = client.post(
        "/books",
        json={
            "serial_number": "123456",
            "title": "Clean Code",
            "author": "Robert C. Martin",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["serial_number"] == "123456"
    assert data["title"] == "Clean Code"
    assert data["author"] == "Robert C. Martin"
    assert data["is_borrowed"] is False
    assert data["borrowed_by"] is None
    assert data["borrowed_at"] is None


def test_create_book_with_duplicate_serial_number_returns_409(client: TestClient):
    book = {
        "serial_number": "123456",
        "title": "Clean Code",
        "author": "Robert C. Martin",
    }

    client.post("/books", json=book)
    response = client.post("/books", json=book)

    assert response.status_code == 409
    assert response.json()["detail"] == "Book already exists"


def test_get_books_returns_created_books(client: TestClient):
    client.post(
        "/books",
        json={
            "serial_number": "100001",
            "title": "Clean Code",
            "author": "Robert C. Martin",
        },
    )

    client.post(
        "/books",
        json={
            "serial_number": "100002",
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
        },
    )

    response = client.get("/books")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["serial_number"] == "100001"
    assert data[1]["serial_number"] == "100002"


def test_delete_book(client: TestClient):
    client.post(
        "/books",
        json={
            "serial_number": "123456",
            "title": "Clean Code",
            "author": "Robert C. Martin",
        },
    )

    response = client.delete("/books/123456")

    assert response.status_code == 204

    get_response = client.get("/books")

    assert get_response.status_code == 200
    assert get_response.json() == []


def test_delete_not_existing_book_returns_404(client: TestClient):
    response = client.delete("/books/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_borrow_book(client: TestClient):
    client.post(
        "/books",
        json={
            "serial_number": "123456",
            "title": "Clean Code",
            "author": "Robert C. Martin",
        },
    )

    response = client.patch(
        "/books/123456/borrow",
        json={
            "borrower_card_number": "654321",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["serial_number"] == "123456"
    assert data["is_borrowed"] is True
    assert data["borrowed_by"] == "654321"
    assert data["borrowed_at"] is not None


def test_borrow_already_borrowed_book_returns_409(client: TestClient):
    client.post(
        "/books",
        json={
            "serial_number": "123456",
            "title": "Clean Code",
            "author": "Robert C. Martin",
        },
    )

    client.patch(
        "/books/123456/borrow",
        json={
            "borrower_card_number": "654321",
        },
    )

    response = client.patch(
        "/books/123456/borrow",
        json={
            "borrower_card_number": "111111",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Book is already borrowed"


def test_return_book(client: TestClient):
    client.post(
        "/books",
        json={
            "serial_number": "123456",
            "title": "Clean Code",
            "author": "Robert C. Martin",
        },
    )

    client.patch(
        "/books/123456/borrow",
        json={
            "borrower_card_number": "654321",
        },
    )

    response = client.patch("/books/123456/return")

    assert response.status_code == 200

    data = response.json()

    assert data["is_borrowed"] is False
    assert data["borrowed_by"] is None
    assert data["borrowed_at"] is None


def test_return_available_book_returns_409(client: TestClient):
    client.post(
        "/books",
        json={
            "serial_number": "123456",
            "title": "Clean Code",
            "author": "Robert C. Martin",
        },
    )

    response = client.patch("/books/123456/return")

    assert response.status_code == 409
    assert response.json()["detail"] == "Book is already available"


def test_invalid_serial_number_returns_422(client: TestClient):
    response = client.post(
        "/books",
        json={
            "serial_number": "123",
            "title": "Clean Code",
            "author": "Robert C. Martin",
        },
    )

    assert response.status_code == 422

def test_borrow_not_existing_book_returns_404(client: TestClient):
    response = client.patch(
        "/books/999999/borrow",
        json={
            "borrower_card_number": "654321",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_return_not_existing_book_returns_404(client: TestClient):
    response = client.patch("/books/999999/return")

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_invalid_borrower_card_number_returns_422(client: TestClient):
    client.post(
        "/books",
        json={
            "serial_number": "123456",
            "title": "Clean Code",
            "author": "Robert C. Martin",
        },
    )

    response = client.patch(
        "/books/123456/borrow",
        json={
            "borrower_card_number": "123",
        },
    )

    assert response.status_code == 422