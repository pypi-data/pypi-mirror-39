import asyncio
from functools import partial
from typing import Callable, NamedTuple


class Subscription:
    def __init__(
            self,
            method: Callable,
            unsubscribe: Callable[["Subscription"], None],
            *,
            loop: "asyncio.events.AbstractEventLoop",
    ):
        self._method = method
        self._unsubscribe = unsubscribe
        self._loop = loop

    def invoke(self, *args, **kwargs):
        if asyncio.iscoroutinefunction(self._method):
            asyncio.ensure_future(self._method(*args, **kwargs), loop=self._loop)
        else:
            self._loop.call_soon(partial(self._method, *args, **kwargs))

    def unsubscribe(self):
        self._unsubscribe(self)
