import asyncio
import aiohttp
import async_timeout

BASEURL = 'https://bastet.socialblade.com/{service}/lookup?query={query}'
HEADERS = {
    'authority': 'bastet.socialblade.com',
    'origin': 'https://socialblade.com',
    'accept': '*/*'
}


class SocialKnife():

    def __init__(self, loop, session):
        self._loop = loop
        self._session = session

    async def get_count(self, service, query):
        url = BASEURL.format(service = service, query = query)
        data = ""
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                header = HEADERS
                header['referer'] = self._generate_referer(service, query)
                response = await self._session.get(url, headers=header)
                data = await response.text()
        except (asyncio.TimeoutError, aiohttp.ClientError) as error:
            print(error)
        return data.strip()
    
    def _generate_referer(self, service, query):
        if service is 'youtube':
            return "https://socialblade.com/youtube/channel/{}".format(query)
        return "https://socialblade.com/{}/user/{}".format(service, query)
