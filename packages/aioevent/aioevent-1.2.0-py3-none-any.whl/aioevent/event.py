"""
Provides BaseEvent ABC.
"""

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .emitter import EventEmitter


# pylint: disable=too-few-public-methods
class BaseEvent:
    """
    ABC for events.
    """

    def __init__(self, *, target: "EventEmitter" = None):
        self.target = target

    target: "EventEmitter"
