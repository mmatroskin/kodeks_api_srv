import aiohttp
from .Result import Result


async def get_data(url, headers=None):
    async with aiohttp.ClientSession(headers=headers) as s:
        async with s.get(url) as res:
            result = Result(url)
            result.status = res.status
            if result.status == 200:
                result.message = 'Success'
                result.data = await res.content.read()
            return result
