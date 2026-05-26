import sqlite3

query_files = ["2_1.sql", "2_2.sql", "2_3.sql", "2_4.sql", "2_5.sql"]

with sqlite3.connect("../hw.db") as conn:
    cursor = conn.cursor()

    for file_name in query_files:
        print(f"\n--- {file_name} ---")
        with open(file_name, "r", encoding="utf-8") as sql_file:
            query = sql_file.read()

        cursor.execute(query)
        rows = cursor.fetchmany(5)
        for row in rows:
            print(row)