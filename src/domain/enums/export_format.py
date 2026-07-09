# src/domain/enums/export_format.py

"""
Export Format Enumeration

Purpose:
    Defines the supported export formats.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from enum import auto

from .base_enum import BaseEnum


class ExportFormat(BaseEnum):
    """Enumeration of supported export formats."""

    CSV = auto()
    EXCEL = auto()
    PDF = auto()

    @classmethod
    def default(cls) -> "ExportFormat":
        """Return the default export format."""
        return cls.CSV
