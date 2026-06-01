from datetime import datetime

from sqlalchemy import Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    count: Mapped[int] = mapped_column(Integer, default=1)
    release_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    author: Mapped["Author"] = relationship(
        back_populates="books",
        lazy="joined",
    )

    receiving_books: Mapped[list["ReceivingBook"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    students = association_proxy("receiving_books", "student")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "count": self.count,
            "release_date": str(self.release_date),
            "author_id": self.author_id,
        }


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)

    books: Mapped[list["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
        }


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    average_score: Mapped[float] = mapped_column(Float, nullable=False)
    scholarship: Mapped[bool] = mapped_column(Boolean, nullable=False)

    received_books: Mapped[list["ReceivingBook"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    books = association_proxy("received_books", "book")

    @classmethod
    def get_students_with_scholarship(cls, session: Session) -> list["Student"]:
        return session.query(cls).filter(cls.scholarship.is_(True)).all()

    @classmethod
    def get_students_with_avg_score_above(
        cls,
        session: Session,
        score: float,
    ) -> list["Student"]:
        return session.query(cls).filter(cls.average_score > score).all()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "phone": self.phone,
            "email": self.email,
            "average_score": self.average_score,
            "scholarship": self.scholarship,
        }


class ReceivingBook(Base):
    __tablename__ = "receiving_books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    date_of_issue: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_of_return: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    book: Mapped["Book"] = relationship(
        back_populates="receiving_books",
        lazy="joined",
    )

    student: Mapped["Student"] = relationship(
        back_populates="received_books",
        lazy="joined",
    )

    @hybrid_property
    def count_date_with_book(self) -> int:
        end_date = self.date_of_return or datetime.now()
        return (end_date - self.date_of_issue).days

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "book_id": self.book_id,
            "student_id": self.student_id,
            "date_of_issue": self.date_of_issue.isoformat(),
            "date_of_return": self.date_of_return.isoformat() if self.date_of_return else None,
            "count_date_with_book": self.count_date_with_book,
        }