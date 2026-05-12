from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.books.models import Book
from app.books.repository import BookRepository
from app.books.schemas import BookCreate


class BookService:

    @staticmethod
    def create_book(db: Session, data: BookCreate) -> Book:
        existing_book = BookRepository.get_by_serial_number(db, data.serial_number)

        if existing_book:
            raise HTTPException(
                status_code=409,
                detail="Book already exists",
            )

        return BookRepository.create(db, data)

    @staticmethod
    def get_books(db: Session) -> list[Book]:
        return BookRepository.get_all(db)

    @staticmethod
    def delete_book(db: Session, serial_number: str) -> None:
        book = BookRepository.get_by_serial_number(db, serial_number)

        if not book:
            raise HTTPException(
                status_code=404,
                detail="Book not found",
            )

        BookRepository.delete(db, book)

    @staticmethod
    def borrow_book(
        db: Session,
        serial_number: str,
        borrower_card_number: str,
    ) -> Book:
        book = BookRepository.get_by_serial_number(db, serial_number)

        if not book:
            raise HTTPException(
                status_code=404,
                detail="Book not found",
            )

        if book.is_borrowed:
            raise HTTPException(
                status_code=409,
                detail="Book is already borrowed",
            )

        book.is_borrowed = True
        book.borrowed_by = borrower_card_number
        book.borrowed_at = datetime.now(UTC)

        return BookRepository.update(db, book)

    @staticmethod
    def return_book(db: Session, serial_number: str) -> Book:
        book = BookRepository.get_by_serial_number(db, serial_number)

        if not book:
            raise HTTPException(
                status_code=404,
                detail="Book not found",
            )

        if not book.is_borrowed:
            raise HTTPException(
                status_code=409,
                detail="Book is already available",
            )

        book.is_borrowed = False
        book.borrowed_by = None
        book.borrowed_at = None

        return BookRepository.update(db, book)