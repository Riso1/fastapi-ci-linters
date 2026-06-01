from datetime import datetime
import csv
from io import TextIOWrapper

from flask import Flask, jsonify, request
from sqlalchemy import func, extract
from database import Base, SessionLocal, engine
from models import Book, Student, ReceivingBook, Author

app = Flask(__name__)

Base.metadata.create_all(bind=engine)


@app.route("/books", methods=["GET"])
def get_books():
    with SessionLocal() as session:
        books = session.query(Book).all()
        return jsonify([book.to_dict() for book in books]), 200


@app.route("/debtors", methods=["GET"])
def get_debtors():
    with SessionLocal() as session:
        debtors = (
            session.query(ReceivingBook)
            .filter(ReceivingBook.date_of_return.is_(None))
            .all()
        )

        result = [item.to_dict() for item in debtors if item.count_date_with_book > 14]
        return jsonify(result), 200


@app.route("/receive-book", methods=["POST"])
def receive_book():
    data = request.get_json()

    book_id = data.get("book_id")
    student_id = data.get("student_id")

    if not book_id or not student_id:
        return jsonify({"error": "book_id and student_id are required"}), 400

    with SessionLocal() as session:
        book = session.query(Book).filter(Book.id == book_id).first()
        student = session.query(Student).filter(Student.id == student_id).first()

        if book is None:
            return jsonify({"error": "Book not found"}), 404
        if student is None:
            return jsonify({"error": "Student not found"}), 404
        if book.count < 1:
            return jsonify({"error": "No available copies"}), 400

        record = ReceivingBook(
            book_id=book_id,
            student_id=student_id,
            date_of_issue=datetime.now(),
            date_of_return=None,
        )
        book.count -= 1

        session.add(record)
        session.commit()

        return jsonify({"message": "Book was issued successfully"}), 201


@app.route("/return-book", methods=["POST"])
def return_book():
    data = request.get_json()

    book_id = data.get("book_id")
    student_id = data.get("student_id")

    if not book_id or not student_id:
        return jsonify({"error": "book_id and student_id are required"}), 400

    with SessionLocal() as session:
        record = (
            session.query(ReceivingBook)
            .filter(
                ReceivingBook.book_id == book_id,
                ReceivingBook.student_id == student_id,
                ReceivingBook.date_of_return.is_(None),
            )
            .first()
        )

        if record is None:
            return jsonify({"error": "This book was not issued to this student"}), 404

        book = session.query(Book).filter(Book.id == book_id).first()
        record.date_of_return = datetime.now()
        if book:
            book.count += 1

        session.commit()

        return jsonify({"message": "Book was returned successfully"}), 200


@app.route("/books/search", methods=["GET"])
def search_books():
    query = request.args.get("q", "").strip()

    with SessionLocal() as session:
        books = session.query(Book).all()
        result = [
            book.to_dict()
            for book in books
            if query.lower() in book.name.lower()
        ]
        return jsonify(result), 200

@app.route("/authors/<int:author_id>/books/count", methods=["GET"])
def get_books_count_by_author(author_id: int):
    with SessionLocal() as session:
        total_count = session.query(func.sum(Book.count)).filter(Book.author_id == author_id).scalar()
        return jsonify({
            "author_id": author_id,
            "books_left": total_count or 0,
        }), 200

@app.route("/students/<int:student_id>/unread-by-read-authors", methods=["GET"])
def get_unread_books_by_known_authors(student_id: int):
    with SessionLocal() as session:
        read_author_ids_subq = (
            session.query(Book.author_id)
            .join(ReceivingBook, ReceivingBook.book_id == Book.id)
            .filter(ReceivingBook.student_id == student_id)
            .distinct()
            .subquery()
        )

        read_book_ids_subq = (
            session.query(ReceivingBook.book_id)
            .filter(ReceivingBook.student_id == student_id)
            .subquery()
        )

        books = (
            session.query(Book)
            .filter(Book.author_id.in_(read_author_ids_subq))
            .filter(~Book.id.in_(read_book_ids_subq))
            .all()
        )

        return jsonify([book.to_dict() for book in books]), 200

@app.route("/stats/average-books-this-month", methods=["GET"])
def get_average_books_this_month():
    now = datetime.now()

    with SessionLocal() as session:
        subq = (
            session.query(
                ReceivingBook.student_id,
                func.count(ReceivingBook.id).label("books_count")
            )
            .filter(extract("year", ReceivingBook.date_of_issue) == now.year)
            .filter(extract("month", ReceivingBook.date_of_issue) == now.month)
            .group_by(ReceivingBook.student_id)
            .subquery()
        )

        avg_value = session.query(func.avg(subq.c.books_count)).scalar()
        return jsonify({"average_books_this_month": float(avg_value or 0)}), 200

@app.route("/stats/most-popular-book-among-good-students", methods=["GET"])
def get_most_popular_book_among_good_students():
    with SessionLocal() as session:
        result = (
            session.query(
                Book,
                func.count(ReceivingBook.id).label("take_count")
            )
            .join(ReceivingBook, ReceivingBook.book_id == Book.id)
            .join(Student, Student.id == ReceivingBook.student_id)
            .filter(Student.average_score > 4.0)
            .group_by(Book.id)
            .order_by(func.count(ReceivingBook.id).desc())
            .first()
        )

        if result is None:
            return jsonify({"message": "No data"}), 404

        book, take_count = result
        return jsonify({
            "book": book.to_dict(),
            "take_count": take_count,
        }), 200

@app.route("/stats/top-10-students-this-year", methods=["GET"])
def get_top_10_students_this_year():
    now = datetime.now()

    with SessionLocal() as session:
        results = (
            session.query(
                Student,
                func.count(ReceivingBook.id).label("books_count")
            )
            .join(ReceivingBook, ReceivingBook.student_id == Student.id)
            .filter(extract("year", ReceivingBook.date_of_issue) == now.year)
            .group_by(Student.id)
            .order_by(func.count(ReceivingBook.id).desc())
            .limit(10)
            .all()
        )

        return jsonify([
            {
                "student": student.to_dict(),
                "books_count": books_count,
            }
            for student, books_count in results
        ]), 200

@app.route("/students/upload-csv", methods=["POST"])
def upload_students_csv():
    if "file" not in request.files:
        return jsonify({"error": "CSV file is required"}), 400

    file = request.files["file"]

    with SessionLocal() as session:
        reader = csv.DictReader(TextIOWrapper(file.stream, encoding="utf-8"), delimiter=";")
        students_data = []

        for row in reader:
            students_data.append({
                "name": row["name"],
                "surname": row["surname"],
                "phone": row["phone"],
                "email": row["email"],
                "average_score": float(row["average_score"]),
                "scholarship": row["scholarship"].lower() in ("true", "1", "yes", "да"),
            })

        session.bulk_insert_mappings(Student, students_data)
        session.commit()

    return jsonify({"inserted": len(students_data)}), 201

if __name__ == "__main__":
    app.run(debug=True)