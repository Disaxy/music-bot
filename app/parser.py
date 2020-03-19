import asyncio

from aiohttp import ClientSession
from bs4 import BeautifulSoup


class SounCloudDownloader:
    def __init__(self, url):
        self.url = url

    async def fetch(self, sc_path):
        payload = {
            'formurl': sc_path}
        async with ClientSession() as session:
            async with session.post(self.url, data=payload) as response:
                return await response.content.read()

    async def get_link(self, sc_path):
        html = await self.fetch(sc_path)
        bs = BeautifulSoup(html, 'lxml')
        data = bs.find('td').div.attrs.get('onclick').split("'")
        raw_link = data[1]
        title = data[-2]
        return raw_link, title


async def main(scd):
    print(await scd.get_link('https://soundcloud.com/phace/phaces-shape-the-random-lp-in-5-minutes-minimixmedley-1'))


if __name__ == '__main__':
    scd = SounCloudDownloader('https://www.forhub.io/download.php')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(scd))
