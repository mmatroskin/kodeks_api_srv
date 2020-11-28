import configparser
from os.path import join
from main_app.settings import ROOT_DIR, REQUESTS_CONFIG, CONFIG


config = configparser.ConfigParser()

# request settings
config_requests_path = join(ROOT_DIR, REQUESTS_CONFIG)
config.read(config_requests_path)

HEADERS = dict(config.items('headers'))

# app settings
config_path = join(ROOT_DIR, CONFIG)
config.read(config_path)

MESSAGE_SUCCESS = config.get("messages", "message_success")
MESSAGE_ERROR = config.get("messages", "message_error")
MESSAGE_404 = config.get("messages", "message_404")
MESSAGE_BAD_QUERY = config.get("messages", "message_bad_query")
