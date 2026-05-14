import sqlite3
import threading
import time
from typing import Optional

import requests


DB_NAME = "star_wars_characters.db"
TABLE_NAME = "characters"
BASE_URL = "https://swapi.dev/api/people/{}/"
CHARACTER_IDS = range(1, 21)


def init_db() -> None:
    """
    Функция инициализации таблицы.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age TEXT NOT NULL,
                gender TEXT NOT NULL
            )
        """)
        conn.commit()


def clear_db() -> None:
    """
    Функция очистки таблицы для нового запуска теста.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {TABLE_NAME}")
        conn.commit()


def save_character(name: str, age: str, gender: str) -> None:
    """
    Функция для сохранения одного персонажа в БД.
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {TABLE_NAME} (name, age, gender) VALUES (?, ?, ?)",
            (name, age, gender)
        )
        conn.commit()


def fetch_character(character_id: int) -> Optional[dict]:
    """
    Функция для загрузки данных одного персонажа из API.
    """
    url = BASE_URL.format(character_id)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return None

    data = response.json()

    return {
        "name": data.get("name", "unknown"),
        "age": data.get("birth_year", "unknown"),
        "gender": data.get("gender", "unknown"),
    }


def load_characters_sequential() -> float:
    """
    Функция последовательно загружает 20 персонажей и сохраняет в БД.
    """
    clear_db()
    start_time = time.perf_counter()

    for character_id in CHARACTER_IDS:
        character = fetch_character(character_id)
        if character is not None:
            save_character(
                name=character["name"],
                age=character["age"],
                gender=character["gender"],
            )

    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(f"Последовательное выполнение: {elapsed:.4f} сек.")
    return elapsed


def worker(character_id: int) -> None:
    """
    Функция потока: загружает и сохраняет одного персонажа.
    """
    character = fetch_character(character_id)
    if character is not None:
        save_character(
            name=character["name"],
            age=character["age"],
            gender=character["gender"],
        )


def load_characters_threaded() -> float:
    """
    Функция загружает 20 персонажей с использованием потоков и сохраняет их в БД.
    """
    clear_db()
    start_time = time.perf_counter()

    threads = []

    for character_id in CHARACTER_IDS:
        thread = threading.Thread(target=worker, args=(character_id,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(f"Параллельное выполнение с потоками: {elapsed:.4f} сек.")
    return elapsed


if __name__ == "__main__":
    init_db()

    sequential_time = load_characters_sequential()
    threaded_time = load_characters_threaded()

    print()
    print(f"Последовательно: {sequential_time:.4f} сек.")
    print(f"С потоками:      {threaded_time:.4f} сек.")

    if threaded_time < sequential_time:
        print("Потоки отработали быстрее.")
    elif threaded_time > sequential_time:
        print("Последовательный запрос отработал быстрее.")
    else:
        print("Время выполнения одинаково.")