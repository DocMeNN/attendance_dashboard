# src/domain/analytics/leaderboards.py

"""
Domain Leaderboard Analytics

Purpose
-------
Provides pure business logic for ranking attendance and activity
participation across members.

Responsibilities
----------------
- Rank attendees by attendance frequency.
- Rank attendees by lateness frequency.
- Rank senders by activity frequency.
- Return top-ranked entries.
- Locate a participant's ranking.

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
- Rankings are returned in descending order.
"""

from __future__ import annotations

# Standard library imports
from collections import Counter
from typing import Iterable

# Third-party imports
# None
# Local imports
from src.domain.enums.attendance_type import AttendanceType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.attendance_event import AttendanceEvent


def rank_attendance(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[tuple[str, int], ...]:
    """
    Rank attendees by attendance count.

    PRESENT and LATE are both considered attendance.
    """
    counter: Counter[str] = Counter()

    for event in attendance_events:
        if event.is_present or event.is_late:
            counter[event.attendee] += 1

    return tuple(counter.most_common())


def rank_lateness(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[tuple[str, int], ...]:
    """
    Rank attendees by lateness count.
    """
    counter: Counter[str] = Counter()

    for event in attendance_events:
        if event.attendance_type is AttendanceType.LATE:
            counter[event.attendee] += 1

    return tuple(counter.most_common())


def rank_activities(
    activity_events: Iterable[ActivityEvent],
) -> tuple[tuple[str, int], ...]:
    """
    Rank message senders by activity count.
    """
    counter: Counter[str] = Counter()

    for event in activity_events:
        counter[event.sender] += 1

    return tuple(counter.most_common())


def top_members(
    rankings: Iterable[tuple[str, int]],
    limit: int = 10,
) -> tuple[tuple[str, int], ...]:
    """
    Return the top-ranked participants.

    Parameters
    ----------
    rankings:
        Ranking produced by one of the rank_* functions.

    limit:
        Maximum number of entries to return.
    """
    return tuple(rankings)[: max(limit, 0)]


def participant_rank(
    participant: str,
    rankings: Iterable[tuple[str, int]],
) -> int | None:
    """
    Return the ranking position of a participant.

    Ranking positions start at 1.

    Returns
    -------
    int | None
        Ranking position if found, otherwise None.
    """
    normalized = participant.casefold()

    for position, (current, _) in enumerate(rankings, start=1):
        if current.casefold() == normalized:
            return position

    return None
