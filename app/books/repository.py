from sqlalchemy import select
from sqlalchemy.orm import Session

from app.books.models import Book
from app.books.schemas import BookCreate


class BookRepository:

    @staticmethod
    def get_all(db: Session) -> list[Book]:
        statement = select(Book).order_by(Book.id)
        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_serial_number(db: Session, serial_number: str) -> Book | None:
        statement = select(Book).where(Book.serial_number == serial_number)
        return db.scalar(statement)

    @staticmethod
    def create(db: Session, data: BookCreate) -> Book:
        book = Book(
            serial_number=data.serial_number,
            title=data.title,
            author=data.author,
        )

        db.add(book)
        db.commit()
        db.refresh(book)

        return book

    @staticmethod
    def update(db: Session, book: Book) -> Book:
        db.commit()
        db.refresh(book)
        return book

    @staticmethod
    def delete(db: Session, book: Book) -> None:
        db.delete(book)
        db.commit()