# src/domain/constants/keywords.py

"""
Business Keywords

Purpose:
    Defines the canonical business keywords used throughout the
    OYBS Attendance Dashboard domain.

Responsibilities:
    - Centralize attendance-related keywords.
    - Centralize activity-related keywords.
    - Provide a single source of truth for business vocabulary.
    - Remain technology independent.

Notes:
    - Contains constants only.
    - No regular expressions.
    - No parsing logic.
    - No business logic.
    - No infrastructure dependencies.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from typing import Final

# ============================================================================
# Attendance Keywords
# ============================================================================

DONE_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "done",
    }
)

# ============================================================================
# Session Markers
# ============================================================================

SESSION_START_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "scripture reading",
        "scriptures reading",
        "scripture reading for today",
        "scriptures reading for today",
    }
)

# ============================================================================
# Activity Keywords
# ============================================================================

OPENING_PRAYER_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "opening prayer",
    }
)

SCRIPTURE_READING_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "scripture reading",
        "scriptures reading",
    }
)

WORSHIP_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "worship",
        "praise and worship",
    }
)

ANNOUNCEMENT_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "announcement",
        "announcements",
    }
)

MESSAGE_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "message",
        "ministration",
        "teaching",
        "sermon",
    }
)

OFFERING_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "offering",
        "tithe",
    }
)

CLOSING_PRAYER_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "closing prayer",
        "closing prayers",
        "closing",
    }
)

# ============================================================================
# Exported Collections
# ============================================================================

ATTENDANCE_KEYWORDS: Final[frozenset[str]] = DONE_KEYWORDS

ACTIVITY_KEYWORDS: Final[dict[str, frozenset[str]]] = {
    "opening_prayer": OPENING_PRAYER_KEYWORDS,
    "scripture_reading": SCRIPTURE_READING_KEYWORDS,
    "worship": WORSHIP_KEYWORDS,
    "announcement": ANNOUNCEMENT_KEYWORDS,
    "message": MESSAGE_KEYWORDS,
    "offering": OFFERING_KEYWORDS,
    "closing_prayer": CLOSING_PRAYER_KEYWORDS,
}
