# src/domain/analytics/sessions.py

"""
Domain Session Analytics

Purpose
-------
Provides pure business logic for analysing meeting sessions.

Responsibilities
----------------
- Count sessions.
- Calculate aggregate session metrics.
- Locate earliest and latest sessions.
- Calculate average session duration.
- Calculate session attendance and activity metrics.
- Remain technology independent.

Notes
-----
- Operates only on immutable Domain models.
- Assumes Session objects are valid.
- No pandas.
- No Streamlit.
- No file I/O.
- No database access.
- No infrastructure dependencies.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterable
from datetime import timedelta

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.models.session import Session

# ============================================================================
# Session Counts
# ============================================================================


def count_sessions(
    sessions: Iterable[Session],
) -> int:
    """
    Return the total number of sessions.
    """

    return sum(1 for _ in sessions)


# ============================================================================
# Session Retrieval
# ============================================================================


def get_latest_session(
    sessions: Iterable[Session],
) -> Session | None:
    """
    Return the latest session by session date.
    """

    sessions = tuple(sessions)

    if not sessions:
        return None

    return max(
        sessions,
        key=lambda session: session.session_date,
    )


def get_earliest_session(
    sessions: Iterable[Session],
) -> Session | None:
    """
    Return the earliest session by session date.
    """

    sessions = tuple(sessions)

    if not sessions:
        return None

    return min(
        sessions,
        key=lambda session: session.session_date,
    )


# ============================================================================
# Duration Analytics
# ============================================================================


def calculate_average_duration(
    sessions: Iterable[Session],
) -> timedelta:
    """
    Return the average duration of all sessions.
    """

    sessions = tuple(sessions)

    if not sessions:
        return timedelta(0)

    total_duration = sum(
        (session.duration for session in sessions),
        start=timedelta(0),
    )

    return total_duration / len(sessions)


def calculate_total_duration(
    sessions: Iterable[Session],
) -> timedelta:
    """
    Return the combined duration of all sessions.
    """

    return sum(
        (session.duration for session in sessions),
        start=timedelta(0),
    )


# ============================================================================
# Attendance Analytics
# ============================================================================


def total_attendance_events(
    sessions: Iterable[Session],
) -> int:
    """
    Return the total number of attendance events.
    """

    return sum(session.attendance_count for session in sessions)


def total_unique_attendees(
    sessions: Iterable[Session],
) -> int:
    """
    Return the total number of unique attendees across sessions.

    Each session's attendee count is summed independently.
    """

    return sum(session.attendee_count for session in sessions)


# ============================================================================
# Activity Analytics
# ============================================================================


def total_activity_events(
    sessions: Iterable[Session],
) -> int:
    """
    Return the total number of activity events.
    """

    return sum(session.activity_count for session in sessions)


# ============================================================================
# Summary
# ============================================================================


def session_summary(
    sessions: Iterable[Session],
) -> dict[str, object]:
    """
    Return aggregate session analytics.
    """

    sessions = tuple(sessions)

    return {
        "session_count": len(sessions),
        "earliest_session": get_earliest_session(sessions),
        "latest_session": get_latest_session(sessions),
        "total_duration": calculate_total_duration(sessions),
        "average_duration": calculate_average_duration(sessions),
        "total_attendance_events": total_attendance_events(sessions),
        "total_activity_events": total_activity_events(sessions),
    }
