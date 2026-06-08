import asyncio
from pathlib import Path

import aiohttp


CAT_URL = "https://cataas.com/cat"
IMAGES_DIR = Path("images")
CATS_COUNT = 10


async def save_image(filename: Path, content: bytes) -> None:
    """
    Сохраняет картинку на диск.

    В задании нельзя использовать aiofiles, поэтому используется обычный open.
    Чтобы синхронная запись файла не блокировала event loop, она запускается
    в отдельном потоке через asyncio.to_thread.
    """

    def write_file() -> None:
        with open(filename, "wb") as file:
            file.write(content)

    await asyncio.to_thread(write_file)


async def download_cat(session: aiohttp.ClientSession, cat_number: int) -> None:
    """
    Скачивает одну картинку кота и сохраняет её в папку images.
    """

    async with session.get(CAT_URL) as response:
        response.raise_for_status()
        image_content = await response.read()

    filename = IMAGES_DIR / f"cat_{cat_number}.jpg"
    await save_image(filename, image_content)


async def main() -> None:
    """
    Создаёт задачи на скачивание нескольких картинок котов.
    """

    IMAGES_DIR.mkdir(exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = [
            download_cat(session, cat_number)
            for cat_number in range(1, CATS_COUNT + 1)
        ]

        await asyncio.gather(*tasks)

    print(f"Готово. Скачано картинок: {CATS_COUNT}")


if __name__ == "__main__":
    asyncio.run(main())