"""
aioevents module.
"""

from .emitter import EventEmitter
from .event import BaseEvent

__all__ = [
    "EventEmitter",
    "BaseEvent",
]
