# src/domain/constants/keywords.py

"""
Business Keywords

Purpose
-------
Defines the canonical business vocabulary used throughout the
Online Bible Study Community Analytics Platform.

Responsibilities
----------------
- Centralize attendance keywords.
- Centralize session detection markers.
- Centralize activity detection keywords.
- Centralize prayer session boundary markers.
- Provide one source of truth for domain vocabulary.

Domain Context
--------------
This system analyzes participation in an online Bible Study community.

It is not a church service analytics system.

Therefore, the vocabulary intentionally excludes:

- Worship
- Offering
- Tithe
- Sermon
- Ministration
- Generic church-service message categories

Rules
-----
- Constants only.
- No regular expressions.
- No parsing logic.
- No business logic.
- No infrastructure dependencies.
- Boundary matching logic belongs to the consuming domain policy
  or analytics component.
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
# Session Detection Markers
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
# Prayer Session Opening Markers
# ============================================================================

PRAYER_SESSION_OPENING_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "opening prayer",
        "prayer session opens",
    }
)

# Compatibility alias for domain policy consumers.
OPENING_PRAYER_KEYWORDS: Final[frozenset[str]] = PRAYER_SESSION_OPENING_KEYWORDS


# ============================================================================
# Prayer Session Closing Markers
# ============================================================================

PRAYER_SESSION_CLOSING_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "closing prayer",
        "closing prayers",
        "prayer session closes",
    }
)

# Compatibility alias for domain policy consumers.
CLOSING_PRAYER_KEYWORDS: Final[frozenset[str]] = PRAYER_SESSION_CLOSING_KEYWORDS


# ============================================================================
# Activity Keywords
# ============================================================================

SCRIPTURE_READING_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "scripture reading",
        "scriptures reading",
    }
)


INSIGHT_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "insight",
        "insights",
    }
)


DISCUSSION_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "discussion",
        "discussions",
    }
)


ANNOUNCEMENT_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "announcement",
        "announcements",
    }
)


# ============================================================================
# Exported Collections
# ============================================================================

ATTENDANCE_KEYWORDS: Final[frozenset[str]] = DONE_KEYWORDS


ACTIVITY_KEYWORDS: Final[dict[str, frozenset[str]]] = {
    "scripture_reading": SCRIPTURE_READING_KEYWORDS,
    "insight": INSIGHT_KEYWORDS,
    "discussion": DISCUSSION_KEYWORDS,
    "announcement": ANNOUNCEMENT_KEYWORDS,
    "done": DONE_KEYWORDS,
    "prayer_session_opening": PRAYER_SESSION_OPENING_KEYWORDS,
    "prayer_session_closing": PRAYER_SESSION_CLOSING_KEYWORDS,
}
