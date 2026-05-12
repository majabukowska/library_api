from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.books.models import Book