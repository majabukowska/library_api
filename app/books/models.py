from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)

    serial_number: Mapped[str] = mapped_column(
        String(6),
        unique=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    author: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_borrowed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    borrowed_by: Mapped[str | None] = mapped_column(
        String(6),
        nullable=True,
    )