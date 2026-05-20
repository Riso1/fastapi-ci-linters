from flask import Flask, render_template, request, redirect, url_for
from typing import List

from models import init_db, get_all_books, DATA, add_book, get_books_by_author, get_book_by_id, increment_book_views
from forms import BookForm

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"

def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    books = get_all_books()
    for book in books:
        increment_book_views(book.id)

    books = get_all_books()

    return render_template(
        'index.html',
        books=books,
    )


@app.route("/books/<int:book_id>")
def get_book(book_id: int):
    book = get_book_by_id(book_id)

    if book is None:
        return "Book not found", 404

    increment_book_views(book_id)
    book = get_book_by_id(book_id)

    return render_template(
        "book.html",
        book=book,
    )


@app.route('/books/form', methods=["GET", "POST"])
def get_books_form() -> str:
    # if request.method == "POST":
    #     title = request.form["book_title"]
    #     author = request.form["author_name"]
    #     add_book(title, author)
    #     return redirect(url_for("all_books"))
    #
    # return render_template('add_book.html')
    form = BookForm()

    if form.validate_on_submit():
        title = form.book_title.data
        author = form.author_name.data
        add_book(title, author)
        return redirect(url_for("all_books"))

    return  render_template("add_book.html", form=form)

@app.route("/books/author/<author>")
def books_by_author(author: str) -> str:
    books = get_books_by_author(author)
    return render_template(
        "author_books.html",
        books=books,
        author=author
    )


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
