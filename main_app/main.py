from aiohttp import web
from os.path import join
from settings import SRV_HOST, SRV_PORT, ROOT_DIR, LOG_FILE
from app_log import get_logger
from routes import routes


def main():
    app = web.Application()
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    log = get_logger(join(ROOT_DIR, LOG_FILE))
    log.info('Start server')
    web.run_app(app, host=SRV_HOST, port=SRV_PORT)
    log.info('Stop server')


if __name__ == '__main__':
    main()
