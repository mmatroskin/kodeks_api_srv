from pathlib import Path
from shared import DocType


SRV_HOST = '127.0.0.1'
SRV_PORT = '5001'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
    'accept': '*/*'
}
BASE_URL = r'http://docs.cntd.ru'
HOST = r'http://newapi.kodeks.ru'
SEARCH_URL_BASE = r'/search/intelectual2/q/'
SEARCH_URL_TYPE = r'/r/'
SEARCH_URL_OFFSET = r'/offset/'
SEARCH_URL_SITE = r'/site=tehexpert'
DOC_URL_XML = r'/document/fullcontent/id/'      # xml (info + text)
DOC_URL_HTML = r'/document/html/id/'      # html
DOC_URL_JSON = r'/chapter/get/document_id/'     # json
DOCTOC_URL = r'/document/getdoctoc/id/'     # json
DOC_TYPES = {
    '4': DocType('4', 'Нормы, правила, стандарты'),
    '10': DocType('10', 'Технические описания'),
    '11': DocType('11', 'Техническая документация'),
    '12': DocType('12', 'Типовая проектная документация'),
    '13': DocType('13', 'Все'),
}
ITEMS_ON_RESULTS = 20
ROOT_DIR = Path(__file__).resolve().parent
LOG_FILE = 'log.txt'
