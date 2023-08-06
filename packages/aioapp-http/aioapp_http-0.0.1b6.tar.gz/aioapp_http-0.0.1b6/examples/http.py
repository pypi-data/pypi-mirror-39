import os
import logging
import asyncio
from aiohttp import web, web_request
from aioapp.app import Application
from aioapp import config
from aioapp.tracer import Span
from aioapp_http import Server, Handler


class Config(config.Config):
    host: str
    port: int
    _vars = {
        'host': {
            'type': str,
            'name': 'HOST',
            'descr': 'TCP/IP host name',
            'default': '127.0.0.1',
        },
        'port': {
            'type': int,
            'name': 'PORT',
            'descr': 'TCP/IP port',
            'min': 0,
            'max': 65535,
            'default': 8080,
        },
    }


class HttpHandler(Handler):

    async def prepare(self):
        self.server.add_route('GET', '/', self.home_handler)
        self.server.set_error_handler(self.error_handler)

    async def error_handler(self, ctx: Span, request: web_request.Request,
                            error: Exception) -> web.Response:
        self.app.log_err(error)
        if isinstance(error, web.HTTPException):
            return error
        return web.Response(body='Internal Error', status=500)

    async def home_handler(self, ctx: Span,
                           request: web_request.Request) -> web.Response:
        return web.Response(text='OK')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()

    cfg = Config(os.environ)

    app = Application(loop=loop)
    app.add(
        'srv',
        Server(
            host=cfg.host,
            port=cfg.port,
            handler=HttpHandler
        ),
        stop_after=[])
    app.run()
