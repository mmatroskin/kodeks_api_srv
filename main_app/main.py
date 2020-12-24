import configparser
from aiohttp import web
from os import path, environ
from settings import ROOT_DIR, LOG_FILE, CONFIG
from app_log import get_logger
from routes import routes
from shared import user_agent


def main():
    config_path = path.join(ROOT_DIR, CONFIG)
    config = configparser.ConfigParser()
    config.read(config_path)

    ON_HEROKU = environ.get('ON_HEROKU')
    
    SRV_HOST = config.get("server", "host")
    SRV_PORT = config.get("server", "port")
    if ON_HEROKU:
        # get the heroku port 
        SRV_PORT = int(os.environ.get("PORT", SRV_PORT))  # as per OP comments default is SRV_PORT

    user_agent.update()

    log = get_logger(path.join(ROOT_DIR, LOG_FILE))

    app = web.Application(logger=log)
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    log.info('Start server')
    web.run_app(app, host=SRV_HOST, port=SRV_PORT)


if __name__ == '__main__':
    main()
