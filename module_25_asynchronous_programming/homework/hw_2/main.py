import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path

import aiohttp
import requests


CAT_URL = "https://cataas.com/cat"
COUNTS = [10, 50, 100]


async def save_image_async(filename: Path, content: bytes) -> None:
    """
    Асинхронное сохранение файла через стандартный open.

    Сам open остаётся синхронным, поэтому запись вынесена в отдельный поток
    с помощью asyncio.to_thread. Так event loop не блокируется во время
    записи изображения на диск.
    """

    def write_file() -> None:
        with open(filename, "wb") as file:
            file.write(content)

    await asyncio.to_thread(write_file)


async def download_cat_async(
    session: aiohttp.ClientSession,
    cat_number: int,
    images_dir: Path,
) -> None:
    """
    Скачивает одну картинку кота с помощью aiohttp.

    Если внешний сервис временно отвечает ошибкой, делаем несколько попыток.
    """

    for attempt in range(1, 4):
        try:
            async with session.get(CAT_URL) as response:
                response.raise_for_status()
                image_content = await response.read()

            filename = images_dir / f"cat_{cat_number}.jpg"
            await save_image_async(filename, image_content)

            return

        except aiohttp.ClientError as error:
            if attempt == 3:
                print(f"Не удалось скачать cat_{cat_number}: {error}")


async def run_async_version(cats_count: int) -> float:
    """
    Запускает асинхронную версию загрузки картинок.
    Возвращает время выполнения в секундах.
    """

    images_dir = Path(f"images_async_{cats_count}")
    images_dir.mkdir(exist_ok=True)

    start_time = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = [
            download_cat_async(session, cat_number, images_dir)
            for cat_number in range(1, cats_count + 1)
        ]

        await asyncio.gather(*tasks)

    return time.perf_counter() - start_time


def download_cat_sync(cat_number: int, images_dir: Path) -> None:
    """
    Синхронно скачивает одну картинку кота через requests.
    Эта функция используется и в потоках, и в процессах.

    Если сервис временно отдаёт ошибку, делаем несколько попыток.
    """

    for attempt in range(1, 4):
        try:
            response = requests.get(CAT_URL, timeout=20)
            response.raise_for_status()

            filename = images_dir / f"cat_{cat_number}.jpg"

            with open(filename, "wb") as file:
                file.write(response.content)

            return

        except requests.RequestException as error:
            if attempt == 3:
                print(f"Не удалось скачать cat_{cat_number}: {error}")


def run_threads_version(cats_count: int) -> float:
    """
    Запускает загрузку картинок в нескольких потоках.
    Такой подход подходит для IO-задач, где много ожидания сети.
    """

    images_dir = Path(f"images_threads_{cats_count}")
    images_dir.mkdir(exist_ok=True)

    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(download_cat_sync, cat_number, images_dir)
            for cat_number in range(1, cats_count + 1)
        ]

        for future in futures:
            future.result()

    return time.perf_counter() - start_time


def run_processes_version(cats_count: int) -> float:
    """
    Запускает загрузку картинок в нескольких процессах.

    Для сетевых задач процессы обычно менее выгодны, чем потоки или asyncio,
    но в задании нужно сравнить и этот подход.
    """

    images_dir = Path(f"images_processes_{cats_count}")
    images_dir.mkdir(exist_ok=True)

    start_time = time.perf_counter()

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(download_cat_sync, cat_number, images_dir)
            for cat_number in range(1, cats_count + 1)
        ]

        for future in futures:
            future.result()

    return time.perf_counter() - start_time


async def main() -> None:
    """
    Измеряет время работы трёх подходов и выводит результат
    в формате Markdown-таблицы.
    """

    print("| Количество картинок |   Async   |  Threads  | Processes |")
    print("|---------------------|-----------|-----------|-----------|")

    for cats_count in COUNTS:
        async_time = await run_async_version(cats_count)
        threads_time = run_threads_version(cats_count)
        processes_time = run_processes_version(cats_count)

        print(
            f"|         {cats_count}          | "
            f"{async_time:.2f} сек  | "
            f"{threads_time:.2f} сек  | "
            f"{processes_time:.2f} сек  |"
        )


if __name__ == "__main__":
    asyncio.run(main())