import configparser
from aiohttp import web
from os.path import join
from main_app.settings import ROOT_DIR, LOG_FILE, CONFIG
from main_app.app_log import get_logger
from main_app.routes import routes
from main_app.shared import user_agent


def main():
    config_path = join(ROOT_DIR, CONFIG)
    config = configparser.ConfigParser()
    config.read(config_path)

    SRV_HOST = config.get("server", "host")
    SRV_PORT = config.get("server", "port")

    user_agent.update()

    log = get_logger(join(ROOT_DIR, LOG_FILE))

    app = web.Application(logger=log)
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    log.info('Start server')
    web.run_app(app, host=SRV_HOST, port=SRV_PORT)
    log.info('Stop server')


if __name__ == '__main__':
    main()
