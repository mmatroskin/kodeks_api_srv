import aiohttp
from .Result import Result


async def get_data(url, headers=None):
    async with aiohttp.ClientSession(headers=headers) as s:
        async with s.get(url) as res:
            result = Result(url)
            result.status = res.status
            resp_headers = dict(res.headers)
            result.headers['User-Agent'] = headers.get('User-Agent')
            cookie = resp_headers.get('Set-Cookie', headers.get('Cookie'))
            if cookie is not None:
                idx = cookie.find(';')
                result.headers['Cookie'] = cookie[:idx] if idx != -1 else cookie
            if result.status == 200:
                result.message = 'Success'
                result.data = await res.content.read()
            return result
