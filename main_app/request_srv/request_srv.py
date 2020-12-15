import aiohttp
from .Result import Result


async def get_data(url, headers=None, cookies=None):
    result = Result(url)
    async with aiohttp.ClientSession(headers=headers, cookies=cookies) as s:
        async with s.get(url) as res:
            result.status = res.status
            result.params['user_agent'] = headers.get('User-Agent')
            result.params['cookies'] = cookies if not res.cookies else res.cookies
            if result.status == 200:
                result.message = 'Success'
                result.data = await res.content.read()
    return result
