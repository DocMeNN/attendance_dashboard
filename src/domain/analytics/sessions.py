# filepath: src/domain/analytics/sessions.py

"""
Domain Session Analytics.

This module contains pure business logic for analysing sessions.

Rules
-----
- No pandas
- No Streamlit
- No file I/O
- No database access
- No logging

All functions operate on immutable Domain models.
"""

from __future__ import annotations

from typing import Iterable

from src.domain.enums.session_status import SessionStatus
from src.domain.models.session import Session


def get_completed_sessions(
    sessions: Iterable[Session],
) -> tuple[Session, ...]:
    """
    Return all completed sessions.

    Parameters
    ----------
    sessions:
        Collection of Session objects.

    Returns
    -------
    tuple[Session, ...]
        Completed sessions.
    """
    return tuple(
        session for session in sessions if session.status == SessionStatus.COMPLETED
    )


def get_pending_sessions(
    sessions: Iterable[Session],
) -> tuple[Session, ...]:
    """
    Return all pending sessions.
    """
    return tuple(
        session for session in sessions if session.status == SessionStatus.PENDING
    )


def get_cancelled_sessions(
    sessions: Iterable[Session],
) -> tuple[Session, ...]:
    """
    Return all cancelled sessions.
    """
    return tuple(
        session for session in sessions if session.status == SessionStatus.CANCELLED
    )


def count_sessions(
    sessions: Iterable[Session],
) -> int:
    """
    Return the total number of sessions.
    """
    return sum(1 for _ in sessions)


def calculate_completion_rate(
    sessions: Iterable[Session],
) -> float:
    """
    Calculate the percentage of completed sessions.

    Completion Rate =
        Completed Sessions / Total Sessions × 100
    """
    sessions = tuple(sessions)

    if not sessions:
        return 0.0

    completed = len(get_completed_sessions(sessions))

    return (completed / len(sessions)) * 100.0


def get_latest_session(
    sessions: Iterable[Session],
) -> Session | None:
    """
    Return the most recent session.

    Assumes Session.date uniquely identifies chronological order.
    """
    sessions = tuple(sessions)

    if not sessions:
        return None

    return max(sessions, key=lambda session: session.date)


def get_earliest_session(
    sessions: Iterable[Session],
) -> Session | None:
    """
    Return the earliest session.
    """
    sessions = tuple(sessions)

    if not sessions:
        return None

    return min(sessions, key=lambda session: session.date)
