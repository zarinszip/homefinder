import asyncio
import aiohttp

from sslv.parser.advert import AdvertBuilder

async def fetch_html(url: str) -> str:
    """
    Asynchronously fetches HTML content from the given URL using aiohttp.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()

def main():
    url = input("Enter URL: ").strip()
    if not url:
        print("No URL provided. Exiting.")
        return

    try:
        html = asyncio.run(fetch_html(url))
    except Exception as e:
        print(f"Failed to fetch URL asynchronously: {e}")
        return

    builder = AdvertBuilder()
    home = builder.feed(html, url = url)
    print(home)

if __name__ == "__main__":
    main()
