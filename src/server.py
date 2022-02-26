import logging

from aiohttp import web

from .config import CONFIG


logger = logging.getLogger('swish')


class Server(web.Application):

    def __init__(self):
        super().__init__()

        self.add_routes(
            [
                web.get('/', self.websocket_handler)
            ]
        )

        self.websockets = {}

    async def websocket_handler(self, request: web.Request):
        logger.info(f'Received request to upgrade websocket from:: {request.remote}.')

        ws = web.WebSocketResponse()
        await ws.prepare(request)

        password = CONFIG['SERVER']['password']
        auth = request.headers.get('Authorization')

        if password != auth:
            logger.error(f'Authorization failed for request from:: {request.remote} with Authorization: {auth}')
            raise web.HTTPUnauthorized

        logger.info(f'Successful websocket handshake completed from:: {request.remote}.')

        async for message in ws:
            pass

    async def _run_app(self):
        host_ = CONFIG['SERVER']['host']
        port_ = CONFIG['SERVER']['port']

        logger.info(f'Starting Swish server on {host_}:{port_}...')

        runner = web.AppRunner(app=self)
        await runner.setup()

        site = web.TCPSite(
            runner=runner,
            host=host_,
            port=port_
        )

        await site.start()
        logger.info('Successfully started swish server...')
