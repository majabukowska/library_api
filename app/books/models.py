from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)

    serial_number: Mapped[str] = mapped_column(
        String(6),
        unique=True,
        nullable=False,
        index=True,
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
        nullable=False,
    )

    borrowed_by: Mapped[str | None] = mapped_column(
        String(6),
        nullable=True,
    )

    borrowed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )