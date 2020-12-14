from pathlib import Path
from main_app.shared import DocType


# kodeks api settings
BASE_URL = r'http://newapi.kodeks.ru'
EXT_URL = r'http://docs.cntd.ru'

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

# parameter for offset (=20)
ITEMS_ON_RESULTS = 20

# other settings
ROOT_DIR = Path(__file__).resolve().parent
CONFIG = 'app.ini'
REQUESTS_CONFIG = 'requests.ini'
LOG_FILE = 'log.txt'
