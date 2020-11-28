import configparser
from os.path import join
from main_app.settings import ROOT_DIR, REQUESTS_CONFIG


config_path = join(ROOT_DIR, REQUESTS_CONFIG)
config = configparser.ConfigParser()
config.read(config_path)

# request settings
HEADERS = dict(config.items('headers'))
