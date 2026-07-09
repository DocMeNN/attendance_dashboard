# src/domain/enums/activity_type.py

"""
Activity Type Enumeration

Purpose:
    Defines the supported meeting activity types.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from enum import auto

from .base_enum import BaseEnum


class ActivityType(BaseEnum):
    """Enumeration of meeting activity types."""

    OPENING_PRAYER = auto()
    SCRIPTURE_READING = auto()
    WORSHIP = auto()
    ANNOUNCEMENT = auto()
    MESSAGE = auto()
    OFFERING = auto()
    CLOSING_PRAYER = auto()
    OTHER = auto()

    @classmethod
    def default(cls) -> "ActivityType":
        """Return the default activity type."""
        return cls.OTHER
