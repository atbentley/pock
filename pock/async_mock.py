import asyncio

from .mock import Mock


class AsyncMock(Mock):
    @asyncio.coroutine
    def __aenter__(self,):
        result = yield from getattr(self, '__aenter__')()
        return result

    @asyncio.coroutine
    def __aexit__(self, *args):
        pass
