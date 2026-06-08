import asyncio
from pathlib import Path
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup


START_URLS = [
    "https://docs.python.org/3/",
]

MAX_DEPTH = 3
RESULT_FILE = Path("external_links.txt")


class AsyncCrawler:
    """
    Простой асинхронный интернет-краулер.

    Краулер получает стартовые страницы, скачивает их HTML,
    достаёт ссылки и рекурсивно переходит по внутренним ссылкам.
    Внешние ссылки сохраняются отдельно.
    """

    def __init__(self, start_urls: list[str], max_depth: int = 3, max_pages: int = 100) -> None:
        self.start_urls = start_urls
        self.max_depth = max_depth
        self.max_pages = max_pages

        self.visited_urls: set[str] = set()
        self.external_links: set[str] = set()

    async def fetch_html(
        self,
        session: aiohttp.ClientSession,
        url: str,
    ) -> str | None:
        """
        Загружает HTML страницы.

        Если страница недоступна или вернулся не HTML,
        метод возвращает None.
        """

        try:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    return None

                content_type = response.headers.get("Content-Type", "")

                if "text/html" not in content_type:
                    return None

                return await response.text(errors="ignore")

        except aiohttp.ClientError:
            return None
        except asyncio.TimeoutError:
            return None

    @staticmethod
    def normalize_url(base_url: str, href: str) -> str | None:
        """
        Превращает относительную ссылку в абсолютную
        и отбрасывает неподходящие ссылки.
        """

        absolute_url = urljoin(base_url, href)
        parsed_url = urlparse(absolute_url)

        if parsed_url.scheme not in ("http", "https"):
            return None

        # Убираем якорь, чтобы ссылки вида /page#title
        # не считались разными страницами.
        normalized_url = absolute_url.split("#")[0]

        return normalized_url

    @staticmethod
    def is_external_link(base_url: str, link: str) -> bool:
        """
        Проверяет, является ли ссылка внешней относительно текущей страницы.
        """

        base_domain = urlparse(base_url).netloc
        link_domain = urlparse(link).netloc

        return bool(link_domain) and base_domain != link_domain

    def extract_links(self, html: str, base_url: str) -> list[str]:
        """
        Достаёт все ссылки из HTML-кода страницы.
        """

        soup = BeautifulSoup(html, "html.parser")
        links = []

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            normalized_url = self.normalize_url(base_url, href)

            if normalized_url is not None:
                links.append(normalized_url)

        return links

    async def crawl(
        self,
        session: aiohttp.ClientSession,
        url: str,
        depth: int,
    ) -> None:
        """
        Рекурсивно обходит страницу.

        Внутренние ссылки используются для дальнейшего обхода.
        Внешние ссылки только сохраняются в результат.
        """

        if len(self.visited_urls) >= self.max_pages:
            return

        if depth > self.max_depth:
            return

        if url in self.visited_urls:
            return

        self.visited_urls.add(url)

        html = await self.fetch_html(session, url)

        if html is None:
            return

        links = self.extract_links(html, url)
        tasks = []

        for link in links:
            if self.is_external_link(url, link):
                self.external_links.add(link)
            else:
                tasks.append(self.crawl(session, link, depth + 1))

        if tasks:
            await asyncio.gather(*tasks)

    async def run(self) -> None:
        """
        Запускает обход всех стартовых страниц.
        """

        async with aiohttp.ClientSession() as session:
            tasks = [
                self.crawl(session, url, depth=1)
                for url in self.start_urls
            ]

            await asyncio.gather(*tasks)

    def save_external_links(self, filename: Path) -> None:
        """
        Сохраняет найденные внешние ссылки в файл.
        """

        with open(filename, "w", encoding="utf-8") as file:
            for link in sorted(self.external_links):
                file.write(link + "\n")


async def main() -> None:
    crawler = AsyncCrawler(
        start_urls=START_URLS,
        max_depth=MAX_DEPTH,
        max_pages=100,
    )

    await crawler.run()
    crawler.save_external_links(RESULT_FILE)

    print(f"Просмотрено страниц: {len(crawler.visited_urls)}")
    print(f"Найдено внешних ссылок: {len(crawler.external_links)}")
    print(f"Результат сохранён в файл: {RESULT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())