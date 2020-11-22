import json
import requests
from os.path import join
from settings import SRV_HOST, SRV_PORT, ROOT_DIR


def test():
    search_string = 'Полы'
    url_base = f'http://{SRV_HOST}:{str(SRV_PORT)}'
    result_info = requests.get(url_base, headers=None, params=None)
    if result_info.status_code == 200:
        data_info = json.loads(result_info.text, encoding='utf-8')
        print(data_info)

        types = data_info.get('data')
        type = types.get('4')[0]
        offset = ''
        query = f'query={search_string}&type={type}&offset={offset}'
        url_search = url_base + r'/search?' + query
        result_search = requests.get(url_search, headers=None, params=None)
        if result_search.status_code == 200:
            result_search_data = json.loads(result_search.text, encoding='utf-8')
            data_search = result_search_data.get('data')
            items = data_search.get('items')
            offset = data_search.get('offset')
            count = data_search.get('count')
            print(data_search)

            query1 = f'query={search_string}&type={type}&offset={str(offset)}'
            url_search1 = url_base + r'/search?' + query1
            result_search1 = requests.get(url_search1, headers=None, params=None)
            if result_search1.status_code == 200:
                result_search_data1 = json.loads(result_search1.text, encoding='utf-8')
                data_search1 = result_search_data1.get('data')
                items1 = data_search1.get('items')
                offset1 = data_search1.get('offset')
                count1 = data_search1.get('count')
                print(data_search)

                doc_item = items1[1]
                url_item = url_base + r'/document'
                result_doc = requests.post(url_item, json=doc_item)
                if result_doc.status_code == 200:
                    result_doc_data = json.loads(result_doc.text, encoding='utf-8')
                    if result_doc_data.get('success'):
                        result_data = result_doc_data.get('data')
                        name = result_data.get('id')
                        out_file = join(ROOT_DIR, f'{name}.html')
                        with open(out_file, 'w', encoding='utf-8') as ff:
                            ff.write(result_data.get('html'))
    pass


if __name__ == '__main__':
    test()
