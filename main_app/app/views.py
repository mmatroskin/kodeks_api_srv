from os.path import join
import json
from aiohttp import web
from main_app.app_log import get_logger
from main_app.shared import user_agent
from main_app.settings import ROOT_DIR, LOG_FILE, EXT_URL, BASE_URL, DOC_URL_JSON, DOCTOC_URL, \
    DOC_TYPES, SEARCH_URL_BASE, SEARCH_URL_TYPE, SEARCH_URL_OFFSET, SEARCH_URL_SITE, ITEMS_ON_RESULTS
from .config import HEADERS
from parsers.SearchSrv import SearchSrv
from parsers.DocItem import DocItem
from request_srv.request_srv import get_data


class CustomView(web.View):

    def __init__(self, *args, **kwargs):
        super(web.View, self).__init__(*args, **kwargs)
        self.log = get_logger(join(ROOT_DIR, LOG_FILE), __name__)
        self.result = {
            'success': False,
            'message': 'Неверный запрос',
            'data': None
        }

    @staticmethod
    def _get_request_headers(params):
        headers = HEADERS
        if params is not None:
            headers['User-Agent'] = params.get('User-Agent')
            cookie = params.get('Cookie')
            if cookie is not None:
                headers['Cookie'] = cookie
        else:
            ua = user_agent.random
            headers['User-Agent'] = ua
        return headers

    def save_log(self, action, info=None):
        success = 'Success' if self.result['success'] else 'Error'
        self.log.info(f'action: {action}, info: {info}, success: {success}')


class InfoView(CustomView):

    async def get(self):
        params = self.request.rel_url.query
        data = dict(params)
        action = 'start'
        info = None
        try:
            self.result['success'] = True
            self.result['message'] = 'Success'
            query = data.get('query')
            if query is None:
                self.result['data'] = DOC_TYPES
            else:
                self.result['data'] = self._get_help()
                action = 'help'
                info = f'query={query}'
        except Exception:
            self.log.error("Exception", exc_info=True)
            self.result['message'] = 'Internal error!'
        finally:
            self.save_log(action, info=info)
            response = web.json_response(self.result)
            return response

    @staticmethod
    def _get_help():
        file = join(ROOT_DIR, r'templates/help.txt')
        with open(file, 'r', encoding='utf-8') as fh:
            content = fh.readlines()
        return content


class DocView(CustomView):

    async def post(self):
        """
        post: JSON
            query: document info (id, name, etc) - from result of search query
            headers: User-Agent, Cookie
        :return: JSON
        """
        doc_id = ''
        try:
            post = await self.request.json()
            headers = self.request.headers
            data = dict(post)
            if data is not None:
                doc_id = data.get('query').get('id')
                result = await self._get_document(data)
                self.result = result
        except Exception:
            self.log.error("Exception", exc_info=True)
        finally:
            self.save_log('get_doc', f'id={doc_id}')
            response = web.json_response(self.result)
            return response

    async def _get_document(self, input_data):
        result = {
            'status': 404,
            'success': False,
            'message': 'Ничего нет :(',
        }
        try:
            headers = self._get_request_headers(input_data.get('headers'))
            query = input_data.get('query')
            doc_id = query.get('id')
            doc_name = query.get('name')
            if doc_id is not None:
                url = f'{BASE_URL}{DOC_URL_JSON}{doc_id}'
                resp = await get_data(url, headers)
                if resp.status == 200:
                    document = DocItem(query)
                    data = json.loads(resp.data)
                    html_data = data.get('html')
                    if html_data:
                        template = join(ROOT_DIR, r'templates/doc_template.html')
                        url = f'{BASE_URL}{DOCTOC_URL}{doc_id}'
                        resp = await get_data(url, headers)
                        doctoc_data_item = json.loads(resp.data)
                        doctoc_html_data = doctoc_data_item.get('doctoc')
                        document.fill_body(template=template, content=html_data, doctoc=doctoc_html_data, ext_url=EXT_URL)
                    result['status'] = resp.status
                    result['success'] = True
                    result['message'] = 'Success'
                    result['data'] = {'id': doc_id, 'name': doc_name, 'html': document.html}
        except Exception as e:
            result['message'] = str(e)
            self.log.error("Exception", exc_info=True)
        finally:
            return result


class SearchView(CustomView):

    async def post(self):
        """
        post: JSON
            type: document type,
            query: string,
            offset: offset API parameter, default: 0
            headers: User-Agent, Cookie
        :return: JSON
        """

        post = await self.request.json()
        headers = dict(self.request.headers)
        data = dict(post)
        doc_type = data.get('type', 'all')
        query = data.get('query')
        offset = data.get('offset')
        params = data.get('headers')
        try:
            if offset is None:
                offset = 0
            result = await self._search(query, doc_type, offset, params)
            self.result = result
        except Exception as e:
            self.log.error("Exception", exc_info=True)
        finally:
            self.save_log('search', f'query={query}')
            response = web.json_response(self.result)
            return response

    async def _search(self, query, type, offset, params):
        result = {
            'success': False,
            'message': 'Кодекс инфой не делится :('
        }
        doc_type = DOC_TYPES.get(type)
        headers = self._get_request_headers(params)

        url = f'{BASE_URL}{SEARCH_URL_BASE}{query}{SEARCH_URL_TYPE}{doc_type.id}{SEARCH_URL_OFFSET}{str(offset)}{SEARCH_URL_SITE}'
        data_item = await get_data(url, headers)
        if data_item.status == 200:
            srv = SearchSrv()
            result = srv.get_search_results(text=data_item.data, offset=offset, delta=ITEMS_ON_RESULTS)
            result['headers'] = data_item.headers
        return result
