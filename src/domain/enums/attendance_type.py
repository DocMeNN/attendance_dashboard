# src/domain/enums/attendance_type.py

"""
Attendance Type Enumeration

Purpose:
    Defines the supported attendance event types.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from enum import auto

from .base_enum import BaseEnum


class AttendanceType(BaseEnum):
    """Enumeration of attendance event types."""

    DONE = auto()
    PRESENT = auto()
    LATE = auto()
    ABSENT = auto()
    UNKNOWN = auto()

    @classmethod
    def default(cls) -> "AttendanceType":
        """Return the default attendance type."""
        return cls.UNKNOWN
