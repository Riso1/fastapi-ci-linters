from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    Book,
    get_all_books,
    init_db,
    add_book,
    get_book_by_id,
    update_book_by_id,
    delete_book_by_id,
    add_author,
    get_author_by_id,
    delete_author_by_id,
    get_books_by_author_id,
)
from schemas import BookSchema, AuthorSchema, BookWithAuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookWithAuthorSchema()
        try:
            loaded_data = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        if loaded_data.get("author_id") is not None:
            book_schema = BookSchema()
            try:
                book = book_schema.load(
                    {
                        "title": loaded_data["title"],
                        "author_id": loaded_data["author_id"],
                    }
                )
            except ValidationError as exc:
                return exc.messages, 400

        elif loaded_data.get("author") is not None:
            author = loaded_data["author"]
            author = add_author(author)

            book_schema = BookSchema()
            book = book_schema.load(
                {
                    "title": loaded_data["title"],
                    "author_id": author.id,
                }
            )

        else:
            return {"message": "Either author_id or author must be provided."}, 400

        book = add_book(book)
        return BookSchema().dump(book), 201


class BookResource(Resource):
    def get(self, book_id: int) -> tuple[dict, int] | tuple[dict, int]:
        book = get_book_by_id(book_id)
        if book is None:
            return {"message": "Book not found."}, 404

        return BookSchema().dump(book), 200

    def put(self, book_id: int):
        existing_book = get_book_by_id(book_id)
        if existing_book is None:
            return {"message": "Book not found."}, 404

        data = request.json
        title = data.get("title")
        author_id = data.get("author_id")

        if title is None or author_id is None:
            return {"message": "Both title and author_id are required."}, 400

        if get_author_by_id(author_id) is None:
            return {"message": f"Author with id={author_id} does not exist."}, 400

        updated_book = Book(id=book_id, title=title, author_id=author_id)
        update_book_by_id(updated_book)

        return BookSchema().dump(updated_book), 200

    def delete(self, book_id: int) -> tuple[dict, int]:
        if get_book_by_id(book_id) is None:
            return {"message": "Book not found."}, 404

        delete_book_by_id(book_id)
        return {"message": f"Book {book_id} deleted."}, 200


class AuthorResource(Resource):
    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = AuthorSchema()

        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201

    def get(self, author_id: int) -> tuple[dict, int]:
        author = get_author_by_id(author_id)
        if author is None:
            return {"message": "Author not found."}, 404

        books = get_books_by_author_id(author_id)
        return {
            "author": AuthorSchema().dump(author),
            "books": BookSchema().dump(books, many=True),
        }, 200

    def delete(self, author_id: int) -> tuple[dict, int]:
        author = get_author_by_id(author_id)
        if author is None:
            return {"message": "Author not found."}, 404

        delete_author_by_id(author_id)
        return {"message": f"Author {author_id} deleted."}, 200


api.add_resource(BookList, '/api/books')
api.add_resource(BookResource, "/api/books/<int:book_id>")
api.add_resource(AuthorResource, "/api/authors/", "/api/authors/<int:author_id>")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
