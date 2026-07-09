# src/domain/enums/message_type.py

"""
Message Type Enumeration

Purpose:
    Defines the supported message classifications.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from enum import auto

from .base_enum import BaseEnum


class MessageType(BaseEnum):
    """Enumeration of message classifications."""

    ATTENDANCE = auto()
    ACTIVITY = auto()
    SYSTEM = auto()
    MEDIA = auto()
    TEXT = auto()
    UNKNOWN = auto()

    @classmethod
    def default(cls) -> "MessageType":
        """Return the default message type."""
        return cls.UNKNOWN
