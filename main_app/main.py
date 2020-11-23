import configparser
from aiohttp import web
from os.path import join
from settings import ROOT_DIR, LOG_FILE, CONFIG
from app_log import get_logger
from routes import routes


def main():
    config_path = join(ROOT_DIR, CONFIG)
    config = configparser.ConfigParser()
    config.read(config_path)

    SRV_HOST = config.get("server", "host")
    SRV_PORT = config.get("server", "port")

    log = get_logger(join(ROOT_DIR, LOG_FILE))

    app = web.Application()
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    log.info('Start server')
    web.run_app(app, host=SRV_HOST, port=SRV_PORT)
    log.info('Stop server')


if __name__ == '__main__':
    main()
