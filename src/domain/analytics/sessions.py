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
- Remain technology independent.

Rules
-----
- No pandas.
- No Streamlit.
- No file I/O.
- No database access.
- No infrastructure dependencies.

Notes
-----
- Operates only on immutable Domain models.
- Assumes Session objects are valid.
"""

from __future__ import annotations

# Standard library imports
from datetime import timedelta
from typing import Iterable

# Third-party imports
# None
# Local imports
from src.domain.models.session import Session


def count_sessions(
    sessions: Iterable[Session],
) -> int:
    """
    Return the total number of sessions.
    """
    return sum(1 for _ in sessions)


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


def calculate_average_duration(
    sessions: Iterable[Session],
) -> timedelta:
    """
    Return the average duration of all sessions.
    """
    sessions = tuple(sessions)

    if not sessions:
        return timedelta(0)

    total = sum(
        (session.duration for session in sessions),
        start=timedelta(0),
    )

    return total / len(sessions)


def total_attendance_events(
    sessions: Iterable[Session],
) -> int:
    """
    Return the total number of attendance events.
    """
    return sum(session.attendance_count for session in sessions)


def total_activity_events(
    sessions: Iterable[Session],
) -> int:
    """
    Return the total number of activity events.
    """
    return sum(session.activity_count for session in sessions)
