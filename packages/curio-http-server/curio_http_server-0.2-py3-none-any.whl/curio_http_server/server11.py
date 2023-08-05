from .request import Request
from .response import Response
from curio import TaskTimeout
from curio import tcp_server
from curio import timeout_after
from html import escape
from socket import SHUT_RDWR
from traceback import format_exc


class Connection11(object):
    def __init__(self, socket, address, server):
        self.socket = socket
        self.server = server
        self.request = None
        self.address = address
        self.match_result = None
        self.match_handler = None
        self.match_parameters = None

    async def read_request(self, max_length=64 * 1024):
        if max_length <= 0:
            return b''

        try:
            return await timeout_after(1, self.socket.recv, max_length)
        except TaskTimeout:
            return b''

    async def write_response(self, data):
        await self.socket.sendall(data)


class Server11(object):
    def __init__(self, router, middlewares=None, default_headers=None):
        self.router = router
        self.middlewares = []

        if middlewares:
            self.middlewares += list(middlewares)

        self.default_headers = default_headers

    async def client_connected(self, client, addr):
        connection = Connection11(client, addr, self)

        while True:
            request = Request(connection)

            if not await request._try_read_headers():
                break

            match_result, match_handler, match_parameters = self.router.match(request.path, request.method)

            if match_result >= 400:
                response = Response(connection, request.version, status_code=match_result, headers=self.default_headers)
                await self.on_4xx_error(request, response)
            else:
                response = Response(connection, request.version, status_code=200, headers=self.default_headers)

                try:
                    has_response = False

                    for middleware in self.middlewares:
                        if await middleware.before(request, response) is True:
                            has_response = True
                            break

                    if not has_response:
                        await match_handler(request, response, **match_parameters)

                    for middleware in self.middlewares:
                        await middleware.after(request, response)
                except:
                    if not response._are_headers_sent:
                        response = Response(connection, request.version, status_code=500, headers=self.default_headers)
                        await self.on_5xx_error(request, response, match_handler)

            await response._send_headers()
            await response._send_body(b'')

            if not request.keep_alive:
                break

        await client.shutdown(SHUT_RDWR)
        await client.close()

    async def run(self, host='0.0.0.0', port=80, ssl=None):
        await tcp_server(
            host, port,
            self.client_connected,
            backlog=1024,
            ssl=None,
            reuse_address=True) #,  reuse_port=True)

    async def on_4xx_error(self, request, response):
        await response.send_html('''<html>
<head><title>{0}: {1}</title></head>
<body>
    <h1>{0}: {1}</h1>
    <h2>Method: "{2}"</h2>
    <h2>Path: "{3}"</h2>
</body>'''.format(
    response.status_code,
    response.status_text,
    request.method,
    request.raw_path.decode('ascii')))

    async def on_5xx_error(self, request, response, handler):
        await response.send_html('''<html>
<head><title>{0}: {1}</title></head>
<body>
    <h1>{0}: {1}</h1>
    <h2>Method: "{2}"</h2>
    <h2>Path: "{3}"</h2>
    <h2>Handler: "{4}"</h2>
    <pre>{5}</pre>
</body>'''.format(
    response.status_code,
    response.status_text,
    request.method,
    request.raw_path.decode('ascii'),
    escape(str(handler)),
    format_exc()))
