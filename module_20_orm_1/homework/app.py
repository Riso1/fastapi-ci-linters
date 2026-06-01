from datetime import datetime

from flask import Flask, jsonify, request

from database import Base, SessionLocal, engine
from models import Book, Student, ReceivingBook

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


if __name__ == "__main__":
    app.run(debug=True)