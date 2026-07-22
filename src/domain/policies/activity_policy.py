# src/domain/policies/activity_policy.py

"""
Activity Policy

Purpose
-------
Defines the business rules for identifying and classifying
activities within an OYBS study session.

Responsibilities
----------------
- Identify supported OYBS activities.
- Classify messages by activity.
- Recognize prayer-session boundaries.
- Distinguish Scripture Reading acknowledgements.
- Apply Discussion as the fallback activity.
- Preserve the distinction between session detection and
  activity classification.

Domain Rules
------------
Supported activities:

- Scripture Reading
- Insight
- Discussion
- Announcement
- Done
- Prayer Session

Activity Detection
------------------
Scripture Reading:
    Determined by the Scripture Reading session marker.

Insight:
    Any message beginning with:
        "insight"
        "insights"

Announcement:
    Any message beginning with a supported announcement keyword.

Done:
    Any message beginning with:
        "done"

Discussion:
    Any message that does not match another activity and is
    not inside an active Prayer Session.

Prayer Session
--------------
A prayer session opens when a message starts with either:

    "opening prayer"
    "prayer session opens"

A prayer session closes when a message starts with either:

    "closing prayer"
    "closing prayers"
    "prayer session closes"

A prayer session that remains open automatically closes when
a new OYBS session begins.

Important
---------
- Activity classification is based on the beginning of the message
  where explicit activity markers are required.
- Matching is case-insensitive.
- Discussion is the fallback activity for ordinary study messages.
- Discussion does not include messages inside an active Prayer Session.
- No worship, offering, sermon, ministration, or generic Message
  activity exists in the OYBS domain.
- This module contains domain policy only.
- No pandas.
- No Streamlit.
- No infrastructure dependencies.

Author
------
OYBS Attendance Dashboard

Created
-------
July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from typing import Final

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.constants.keywords import (
    ANNOUNCEMENT_KEYWORDS,
    CLOSING_PRAYER_KEYWORDS,
    DONE_KEYWORDS,
    OPENING_PRAYER_KEYWORDS,
    SCRIPTURE_READING_KEYWORDS,
)

# ============================================================================
# Supported Activity Names
# ============================================================================

ACTIVITY_SCRIPTURE_READING: Final[str] = "Scripture Reading"

ACTIVITY_INSIGHT: Final[str] = "Insight"

ACTIVITY_DISCUSSION: Final[str] = "Discussion"

ACTIVITY_ANNOUNCEMENT: Final[str] = "Announcement"

ACTIVITY_DONE: Final[str] = "Done"

ACTIVITY_PRAYER_SESSION: Final[str] = "Prayer Session"


# ============================================================================
# Message Normalization
# ============================================================================


def normalize_message(
    content: str,
) -> str:
    """
    Normalize message content for policy evaluation.

    Rules
    -----
    - Strip leading and trailing whitespace.
    - Collapse repeated whitespace.
    - Convert to casefolded text.
    """

    return " ".join(content.strip().casefold().split())


# ============================================================================
# Prefix Matching
# ============================================================================


def starts_with_keyword(
    content: str,
    keywords: frozenset[str],
) -> bool:
    """
    Return True if content starts with one of the supplied keywords.
    """

    normalized = normalize_message(content)

    return any(normalized.startswith(keyword.casefold()) for keyword in keywords)


# ============================================================================
# Prayer Session Boundaries
# ============================================================================


def is_prayer_session_opening(
    content: str,
) -> bool:
    """
    Return True if the message opens a prayer session.

    Supported opening markers:

    - opening prayer
    - prayer session opens
    """

    return starts_with_keyword(
        content,
        OPENING_PRAYER_KEYWORDS,
    ) or normalize_message(
        content
    ).startswith("prayer session opens")


def is_prayer_session_closing(
    content: str,
) -> bool:
    """
    Return True if the message closes a prayer session.

    Supported closing markers:

    - closing prayer
    - closing prayers
    - prayer session closes
    """

    return starts_with_keyword(
        content,
        CLOSING_PRAYER_KEYWORDS,
    ) or normalize_message(
        content
    ).startswith("prayer session closes")


# ============================================================================
# Explicit Activity Detection
# ============================================================================


def is_done_activity(
    content: str,
) -> bool:
    """
    Return True if the message represents a Done acknowledgement.
    """

    return starts_with_keyword(
        content,
        DONE_KEYWORDS,
    )


def is_scripture_reading_activity(
    content: str,
) -> bool:
    """
    Return True if the message represents Scripture Reading.
    """

    return starts_with_keyword(
        content,
        SCRIPTURE_READING_KEYWORDS,
    )


def is_insight_activity(
    content: str,
) -> bool:
    """
    Return True if the message represents an Insight.

    Insight is identified when the message begins with either:

    - insight
    - insights
    """

    normalized = normalize_message(content)

    return normalized.startswith("insight") or normalized.startswith("insights")


def is_announcement_activity(
    content: str,
) -> bool:
    """
    Return True if the message represents an Announcement.
    """

    return starts_with_keyword(
        content,
        ANNOUNCEMENT_KEYWORDS,
    )


# ============================================================================
# Activity Classification
# ============================================================================


def classify_activity(
    content: str,
    *,
    prayer_session_active: bool = False,
) -> str:
    """
    Classify a message according to OYBS activity rules.

    Parameters
    ----------
    content:
        Message content.

    prayer_session_active:
        Whether the message occurs while a Prayer Session
        is currently active.

    Returns
    -------
    str
        Canonical OYBS activity name.

    Classification Order
    --------------------
    1. Prayer Session opening
    2. Prayer Session closing
    3. Scripture Reading
    4. Done
    5. Insight
    6. Announcement
    7. Prayer Session
    8. Discussion

    Notes
    -----
    Prayer boundaries are evaluated before the active prayer
    session state so that opening and closing markers are
    classified correctly.

    Discussion is the fallback activity for any message that
    does not match another activity and is outside an active
    Prayer Session.
    """

    if is_prayer_session_opening(content):
        return ACTIVITY_PRAYER_SESSION

    if is_prayer_session_closing(content):
        return ACTIVITY_PRAYER_SESSION

    if is_scripture_reading_activity(content):
        return ACTIVITY_SCRIPTURE_READING

    if is_done_activity(content):
        return ACTIVITY_DONE

    if is_insight_activity(content):
        return ACTIVITY_INSIGHT

    if is_announcement_activity(content):
        return ACTIVITY_ANNOUNCEMENT

    if prayer_session_active:
        return ACTIVITY_PRAYER_SESSION

    return ACTIVITY_DISCUSSION


# ============================================================================
# Supported Activity Inspection
# ============================================================================


def is_supported_activity(
    content: str,
    *,
    prayer_session_active: bool = False,
) -> bool:
    """
    Return True if the message represents a supported activity.

    Since Discussion is the fallback activity, every non-empty
    message is classified as a supported activity.
    """

    return bool(normalize_message(content))


def is_session_boundary_activity(
    content: str,
) -> bool:
    """
    Return True if the message marks a Prayer Session boundary.
    """

    return is_prayer_session_opening(content) or is_prayer_session_closing(content)


def supported_activity_names() -> tuple[str, ...]:
    """
    Return all canonical supported activity names.
    """

    return (
        ACTIVITY_SCRIPTURE_READING,
        ACTIVITY_INSIGHT,
        ACTIVITY_DISCUSSION,
        ACTIVITY_ANNOUNCEMENT,
        ACTIVITY_DONE,
        ACTIVITY_PRAYER_SESSION,
    )
