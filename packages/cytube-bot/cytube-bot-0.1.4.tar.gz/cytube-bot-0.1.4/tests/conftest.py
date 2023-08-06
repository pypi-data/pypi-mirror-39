import asyncio
import json


class MockGetError(Exception):
    pass


class MockGet:
    DEFAULT_SOCKET_CONFIG = {
        'servers': [
            {
                'url': 'http:127.0.0.1:1234',
                'secure': False
            },
            {
                'url': 'https://127.0.0.1:5678',
                'secure': True
            }
        ]
    }
    DEFAULT_SOCKETIO_CONFIG = {
        'sid': '123',
        'pingTimeout': 1000,
        'pingInterval': 1000
    }
    DEFAULT_URLS = {
        'https://127.0.0.1'
        '/socketconfig/channel.json': DEFAULT_SOCKET_CONFIG,
        'https://127.0.0.1:5678'
        '/socket.io/?EID=2&transport=polling': DEFAULT_SOCKETIO_CONFIG
    }

    def __init__(self, urls=None, delay=0.1):
        if urls is None:
            urls = self.DEFAULT_URLS
        self.delay = delay
        self.urls = urls

    @asyncio.coroutine
    def __call__(self, url, loop):
        yield from asyncio.sleep(self.delay, loop=loop)
        try:
            data = self.urls[url]
        except KeyError:
            raise MockGetError('unexpected url %r' % url)
        data = data() if callable(data) else data
        return json.dumps(data)
