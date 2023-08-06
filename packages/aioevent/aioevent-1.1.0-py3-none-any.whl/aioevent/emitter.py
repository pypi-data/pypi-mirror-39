"""
Provides EventEmitter class.
"""

import asyncio
import functools
from typing import (
    Callable,
    Dict,
    List,
    Type,
    Union,
    Coroutine,
)
from .event import BaseEvent


# pylint: disable=invalid-name
EventCallbackType = Callable[[BaseEvent], Union[None, Coroutine[None, None, None]]]


class EventEmitter:
    """
    ABC for a class whose instances emit events.

    :ivar _event_listeners: A dictionary whose keys are subclasses of BaseEvent
            and whose values are lists of event handlers. Event handlers should
            be callables that accept a single argument: the event being emitted.
    """

    _event_listeners: Dict[Type[BaseEvent], List[EventCallbackType]]

    def __init__(
            self,
            *args,
            loop: "asyncio.AbstractEventLoop" = None,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.event_loop = loop or asyncio.get_event_loop()
        self._event_listeners = {}

    def listen(self, event_type: Type[BaseEvent], callback: EventCallbackType):
        """
        Register a callback to be fired when an event is emitted.
        :param event_type: The type of event (subclass of :py:class:`BaseEvent`)
                to listen for.
        :param callback: The callback to trigger when the event is emitted;
                should accept a single parameter which is the instance of
                `event_type` that was emitted.
        :return:
        """
        if event_type not in self._event_listeners:
            self._event_listeners[event_type] = []
        self._event_listeners[event_type].append(callback)

    def emit(self, event: BaseEvent):
        """
        Emit an event.
        :param event: The event to be omitted.
        :return:
        """
        handlers = self._get_handlers_for_type(type(event))
        for handler in handlers:
            self._call_handler(handler, event)

    def proxy(self, emitter):
        """
        Proxy events from another emitter.

        Useful in a grandparent-parent-child type pattern where the grandparent
        cares about events emitted in the child.
        :param emitter:
        :return:
        """
        emitter.listen(BaseEvent, self._proxy_event)

    def _proxy_event(self, event):
        """
        Emit an event via proxy.
        :param event: The event to proxy.
        :return:
        """
        self.emit(event)

    def _get_handlers_for_type(
            self, event_type: Type,
    ) -> List[EventCallbackType]:
        """
        Get all handlers for an event type.

        This method will walk up the subclass tree so that (e.g.) a handle
        for `SomeEventType` will also handle events of type
        `SubclassOfSomeEventType`.
        :param event_type: The event type to find handlers for.
        :return: A list of event handlers.
        """
        handlers = []
        if not issubclass(event_type, BaseEvent):
            return []
        if event_type in self._event_listeners:
            handlers.extend(self._event_listeners[event_type])
        for event_supertype in event_type.__bases__:
            handlers.extend(self._get_handlers_for_type(event_supertype))
        return handlers

    def _call_handler(self, handler: EventCallbackType, event: BaseEvent):
        if asyncio.iscoroutinefunction(handler):
            asyncio.ensure_future(handler(event), loop=self.event_loop)
        else:
            self.event_loop.call_soon(functools.partial(handler, event))
