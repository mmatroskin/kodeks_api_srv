import configparser
from aiohttp import web
import os
from settings import ROOT_DIR, LOG_FILE, CONFIG
from app_log import get_logger
from routes import routes
from shared import user_agent


def main():
    config_path = os.path.join(ROOT_DIR, CONFIG)
    config = configparser.ConfigParser()
    config.read(config_path)

    ON_HEROKU = os.environ.get('ON_HEROKU')
    
    SRV_HOST = config.get("server", "host")
    SRV_PORT = int(config.get("server", "port"))
    if ON_HEROKU:
        SRV_PORT = os.environ.get("PORT", SRV_PORT)

    user_agent.update()

    log = get_logger(os.path.join(ROOT_DIR, LOG_FILE))

    app = web.Application(logger=log)
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    log.info('Start server')
    web.run_app(app, host=SRV_HOST, port=SRV_PORT)


if __name__ == '__main__':
    main()
