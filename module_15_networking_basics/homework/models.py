import sqlite3

DB_NAME = "hotel_rooms.db"

def init_db() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                floor INTEGER NOT NULL,
                guest_num INTEGER NOT NULL,
                beds INTEGER NOT NULL,
                price INTEGER NOT NULL,
                is_booked INTEGER NOT NULL DEFAULT 0
            )
            """
        )

def get_available_rooms(guest_num: int | None = None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        if guest_num is None:
            cursor.execute(
                """
                SELECT room_id, floor, guest_num, beds, price
                FROM rooms
                WHERE is_booked = 0
                """
            )
        else:
            cursor.execute(
                """
                SELECT room_id, floor, guest_num, beds, price
                FROM rooms
                WHERE is_booked = 0 AND guest_num = ?
                """,
                (guest_num,)
            )

        return cursor.fetchall()

def add_room(floor: int, beds: int, guest_num: int, price: int) -> None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO rooms (floor, guest_num, beds, price)
            VALUES (?, ?, ?, ?)
            """,
            (floor, guest_num, beds, price)
        )

def get_room_by_id(room_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT room_id, floor, guest_num, beds, price, is_booked
            FROM rooms
            WHERE room_id = ?
            """,
            (room_id,)
        )

        return cursor.fetchone()

def mark_room_as_booked(room_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE rooms
            SET is_booked = 1
            WHERE room_id = ?
            """,
            (room_id,)
        )