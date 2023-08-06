from typing import Type

from .emitter import EventEmitter
from .event import BaseEvent


def event_listener(emitter: EventEmitter, event_type: Type[BaseEvent]):
    """
    A decorator factory for creating easy inline event listeners.

    ::
        my_emitter = EventEmitter()
        MyEvent = type("MyEvent", (BaseEvent, ), {})

        @event_listener(my_emitter, MyEvent)
        def on_my_event(event):
            print("Got MyEvent!")

        # Prints "Got MyEvent!" on next iteration of event loop.
        my_emitter.emit(MyEvent())

    :param emitter:
    :param event_type:
    :return:
    """
    def decorator(method):
        print("Decorator!")
        emitter.listen(event_type, method)
        return method
    return decorator
