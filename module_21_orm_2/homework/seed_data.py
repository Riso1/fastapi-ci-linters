from datetime import date
from database import SessionLocal
from models import Author, Book, Student

with SessionLocal() as session:
    author_1 = Author(name="Александр", surname="Пушкин")
    author_2 = Author(name="Лев", surname="Толстой")

    session.add_all([author_1, author_2])
    session.commit()

    book_1 = Book(
        name="Капитанская дочка",
        count=3,
        release_date=date(1836, 1, 1),
        author_id=author_1.id,
    )
    book_2 = Book(
        name="Война и мир",
        count=2,
        release_date=date(1869, 1, 1),
        author_id=author_2.id,
    )

    student_1 = Student(
        name="Иван",
        surname="Иванов",
        phone="79990000001",
        email="ivan@example.com",
        average_score=4.8,
        scholarship=True,
    )
    student_2 = Student(
        name="Петр",
        surname="Петров",
        phone="79990000002",
        email="petr@example.com",
        average_score=3.9,
        scholarship=False,
    )

    session.add_all([book_1, book_2, student_1, student_2])
    session.commit()

print("Test data inserted.")