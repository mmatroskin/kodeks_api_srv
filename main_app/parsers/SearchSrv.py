from os.path import join
from xml.dom.minidom import parseString
from main_app.app_log import get_logger
from main_app.settings import ROOT_DIR, LOG_FILE


class SearchSrv():

    def __init__(self):
        self.log = get_logger(join(ROOT_DIR, LOG_FILE), __name__)

    def get_search_results(self, msg_error, msg_success, **data):
        result = {'success': False, 'message': msg_error}
        try:
            dom = parseString(data.get('text'))
            node_list = dom.getElementsByTagName('document')
            is_available = data.get('is_available', False)
            ret = self._get_data(node_list, is_available)
            tmp = dom.getElementsByTagName('count')
            count = 0
            if len(tmp) > 0:
                count_node = tmp[-1]
                count = int(self._get_node_data(count_node))
            offset_next = data.get('offset') + data.get('delta')
            ret['count'] = count
            ret['offset'] = offset_next if count > offset_next else None
            result['data'] = ret
            result['success'] = True
            result['message'] = msg_success
        except Exception as e:
            result['message'] = str(e)
            self.log.error("Exception", exc_info=True)
        return result

    def _get_data(self, node_list, is_available_only, has_text_only=False):
        items = []
        for i in node_list:
            node_id = i.getElementsByTagName('id')[0]
            id = self._get_node_data(node_id)
            node_name = i.getElementsByTagName('name')[0]
            name = self._get_node_data(node_name, 1)
            node_has_text = i.getElementsByTagName('hasText')[0]
            has_text = self._get_node_data(node_has_text)
            node_available = i.getElementsByTagName('isAvailable')[0]
            is_available = self._get_node_data(node_available)  # доступность документа
            node_active = i.getElementsByTagName('isActive')[0]
            is_active = self._get_node_data(node_active)
            if not is_available_only or is_available_only and is_available == 'true':
                items.append({
                    'id': id,
                    'name': name,
                    'has_text': True if has_text == 'true' else False,
                    'is_active': True if is_active == 'true' else False,
                    'is_available': True if is_available == 'true' else False,
                })
        if has_text_only:
            items = list(filter(lambda x: x['has_text'], items))
        result = {'items': items}
        return result

    @staticmethod
    def _get_node_data(node, pos=0):
        node_target = node.childNodes[pos]
        result = node_target.nodeValue
        return result
