import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]


class Book:

    def __init__(self, id: int, title: str, author: str, views: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.views = views

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    views INTEGER DEFAULT 0
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records
                ]
            )


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )
        return [Book(*row) for row in cursor.fetchall()]

def add_book(title: str, author: str) -> None:
    with sqlite3.connect("table_books.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """ 
            INSERT INTO table_books (title, author) 
            VALUES (?, ?)
            """,
            (title, author)
        )

def get_books_by_author(author: str) -> List[Book]:
    with sqlite3.connect("table_books.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM table_books 
            WHERE author = ?
            """,
            (author,)
        )
        return [Book(*row) for row in cursor.fetchall()]

def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect("table_books.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM table_books
                WHERE id = ?
            """,
            (book_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Book(*row)

def increment_book_views(book_id: int) -> None:
    with sqlite3.connect("table_books.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE table_books
            SET views = views + 1
            WHERE id = ?
            """,
            (book_id,)
        )

def increment_all_books_views() -> None:
    with sqlite3.connect("table_books.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE table_books
            SET views = views + 1
            """
        )
        