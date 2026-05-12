from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.books.schemas import BookCreate, BookResponse, BorrowBookRequest
from app.books.service import BookService
from app.db.dependencies import get_db

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    data: BookCreate,
    db: Session = Depends(get_db),
):
    return BookService.create_book(db, data)


@router.get(
    "",
    response_model=list[BookResponse],
)
def get_books(
    db: Session = Depends(get_db),
):
    return BookService.get_books(db)


@router.delete(
    "/{serial_number}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(
    serial_number: str,
    db: Session = Depends(get_db),
):
    BookService.delete_book(db, serial_number)


@router.patch(
    "/{serial_number}/borrow",
    response_model=BookResponse,
)
def borrow_book(
    serial_number: str,
    data: BorrowBookRequest,
    db: Session = Depends(get_db),
):
    return BookService.borrow_book(
        db=db,
        serial_number=serial_number,
        borrower_card_number=data.borrower_card_number,
    )


@router.patch(
    "/{serial_number}/return",
    response_model=BookResponse,
)
def return_book(
    serial_number: str,
    db: Session = Depends(get_db),
):
    return BookService.return_book(db, serial_number)