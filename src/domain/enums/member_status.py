# src/domain/enums/member_status.py

"""
Member Status Enumeration

Purpose:
    Defines the final attendance status of a member.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from enum import auto

from .base_enum import BaseEnum


class MemberStatus(BaseEnum):
    """Enumeration of member attendance status."""

    PRESENT = auto()
    ABSENT = auto()
    LATE = auto()
    EXCUSED = auto()
    UNKNOWN = auto()

    @classmethod
    def default(cls) -> "MemberStatus":
        """Return the default member status."""
        return cls.UNKNOWN
