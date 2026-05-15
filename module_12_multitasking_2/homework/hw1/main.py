from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import sqlite3
import requests
import time


BASE_URL = "https://swapi.py4e.com/api/people/{}/"
DB_NAME = "star_wars_characters.db"
CHARACTERS_IDS = range(1, 21)

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age TEXT NOT NULL,
                gender TEXT NOT NULL
            )
        """)
        conn.commit()

def clean_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM characters")
        conn.commit()

def fetch_character(character_id):
    url = BASE_URL.format(character_id)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data["name"], data["birth_year"], data["gender"]
    except Exception as er:
        print(f"Возникла ошибка при получении персонажа {character_id}: {er}")

def save_characters(characters):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO characters (name, age, gender) VALUES (?, ?, ?)",
            characters
        )
        conn.commit()

def load_characters_with_thread_pool():
    clean_db()
    start_time = time.perf_counter()

    with ThreadPool(10) as pool:
        characters = pool.map(fetch_character, CHARACTERS_IDS)

    characters = [character for character in characters if character is not None]
    save_characters(characters)

    elapsed = time.perf_counter() - start_time
    print(f"ThreadPool: {elapsed:.4f} сек.")
    return elapsed

def load_characters_with_process_pool():
    clean_db()
    start_time = time.perf_counter()

    with Pool(4) as pool:
        characters = pool.map(fetch_character, CHARACTERS_IDS)

    characters = [character for character in characters if character is not None]
    save_characters(characters)

    elapsed = time.perf_counter() - start_time
    print(f"Pool: {elapsed:.4f} сек.")
    return elapsed

if __name__ == "__main__":
    init_db()

    thread_time = load_characters_with_thread_pool()
    process_time = load_characters_with_process_pool()

    if thread_time < process_time:
        print("ThreadPool faster")
    elif thread_time > process_time:
        print("Process Pool faster")
    else:
        print("Same execution time")