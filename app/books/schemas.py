from datetime import datetime

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    serial_number: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)


class BookResponse(BaseModel):
    id: int
    serial_number: str
    title: str
    author: str
    is_borrowed: bool
    borrowed_by: str | None
    borrowed_at: datetime | None

    model_config = {
        "from_attributes": True,
    }


class BorrowBookRequest(BaseModel):
    borrower_card_number: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")