import sqlite3

with open("create_schema.sql", "r", encoding="utf-8") as sql_file:
    sql_script = sql_file.read()

with sqlite3.connect("schema_test.db") as conn:
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.executescript(sql_script)
    conn.commit()

print("Схема была создана.")
