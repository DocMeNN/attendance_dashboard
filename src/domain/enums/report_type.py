# src/domain/enums/report_type.py

"""
Report Type Enumeration

Purpose:
    Defines the supported report categories.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from enum import auto

from .base_enum import BaseEnum


class ReportType(BaseEnum):
    """Enumeration of report types."""

    ATTENDANCE = auto()
    ACTIVITY = auto()
    SUMMARY = auto()
    DASHBOARD = auto()

    @classmethod
    def default(cls) -> "ReportType":
        """Return the default report type."""
        return cls.SUMMARY
