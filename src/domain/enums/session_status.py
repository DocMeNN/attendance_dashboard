# src/domain/enums/session_status.py

"""
Session Status Enumeration

Purpose:
    Defines the lifecycle state of a meeting session.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from enum import auto

from .base_enum import BaseEnum


class SessionStatus(BaseEnum):
    """Enumeration of session states."""

    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()

    @classmethod
    def default(cls) -> "SessionStatus":
        """Return the default session status."""
        return cls.NOT_STARTED
