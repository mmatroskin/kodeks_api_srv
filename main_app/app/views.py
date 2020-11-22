from os.path import join
import json
from aiohttp import web
from main_app.app_log import get_logger
from main_app.settings import ROOT_DIR, LOG_FILE, HEADERS, HOST, BASE_URL, DOC_URL_JSON, DOCTOC_URL, \
    DOC_TYPES, SEARCH_URL_BASE, SEARCH_URL_TYPE, SEARCH_URL_OFFSET, SEARCH_URL_SITE, ITEMS_ON_RESULTS
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

    def save_log(self):
        success = 'Success' if self.result['success'] else 'Error'
        self.log.info(f'action: get_doc, success: {success}')


class InfoView(CustomView):

    async def get(self):
        self.result['success'] = True
        self.result['message'] = 'Success'
        self.result['data'] = DOC_TYPES
        response = web.json_response(self.result)
        return response


class DocView(CustomView):

    async def post(self):
        post = await self.request.json()
        data = dict(post)
        if data is not None:
            result = await self._get_document(data)
            self.result = result

        self.save_log()

        response = web.json_response(self.result)
        return response

    async def _get_document(self, doc_info):
        result = {
            'status': 404,
            'success': False,
            'message': 'Ничего нет :(',
        }
        try:
            doc_id = doc_info.get('id')
            if doc_id is not None:
                url = f'{HOST}{DOC_URL_JSON}{doc_id}'
                resp = await get_data(url, HEADERS)
                if resp.status == 200:
                    document = DocItem(doc_info)
                    data = json.loads(resp.data)
                    html_data = data.get('html')
                    if html_data:
                        template = join(ROOT_DIR, r'templates/doc_template.html')
                        url = f'{HOST}{DOCTOC_URL}{doc_id}'
                        resp = await get_data(url, HEADERS)
                        doctoc_data_item = json.loads(resp.data)
                        doctoc_html_data = doctoc_data_item.get('doctoc')
                        document.fill_body(template=template, content=html_data, doctoc=doctoc_html_data, ext_url=BASE_URL)
                    result['status'] = resp.status
                    result['success'] = True
                    result['message'] = 'Success'
                    result['data'] = {'id': doc_id, 'html': document.html}
        except Exception as e:
            result['message'] = str(e)
            self.log.error("Exception", exc_info=True)
        finally:
            return result


class SearchView(CustomView):

    async def get(self):
        self.result['message'] = 'Неверный зарос'
        try:
            params = self.request.rel_url.query
            data = dict(params)
            type = data.get('type', 'all')
            query = data.get('query')
            offset = data.get('offset')
            if offset is None or not offset.isdigit():
                offset = 0
            result = await self._search(query, type, offset)
            self.result = result

            self.save_log()
        except Exception as e:
            self.log.error("Exception", exc_info=True)
        finally:
            response = web.json_response(self.result)
            return response

    @staticmethod
    async def _search(query, type, offset):
        result = {
            'success': False,
            'message': 'Кодекс болеет :('
        }
        doc_type = DOC_TYPES.get(type)
        url = f'{HOST}{SEARCH_URL_BASE}{query}{SEARCH_URL_TYPE}{doc_type.id}{SEARCH_URL_OFFSET}{str(offset)}{SEARCH_URL_SITE}'
        data_item = await get_data(url, HEADERS)
        if data_item.status == 200:
            srv = SearchSrv()
            result = srv.get_search_results(text=data_item.data, offset=offset, delta=ITEMS_ON_RESULTS)
        return result

