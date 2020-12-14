import configparser
from os.path import join
from settings import ROOT_DIR, REQUESTS_CONFIG, CONFIG


config = configparser.ConfigParser()

# request settings
config_requests_path = join(ROOT_DIR, REQUESTS_CONFIG)
config.read(config_requests_path, encoding='utf-8')

HEADERS = dict(config.items('headers'))

# app settings
config_path = join(ROOT_DIR, CONFIG)
config.read(config_path)

MESSAGE_SUCCESS = config.get("messages", "message_success")
MESSAGE_ERROR = config.get("messages", "message_error")
MESSAGE_404 = 'Кодекс не хочет делиться :('
MESSAGE_BAD_QUERY = 'Неверный запрос'
