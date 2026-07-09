# filepath: src/domain/analytics/leaderboards.py

"""
Domain Leaderboard Analytics.

This module contains pure business logic for ranking members based on
attendance and activity metrics.

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

from collections import Counter
from typing import Iterable

from src.domain.enums.attendance_type import AttendanceType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.attendance_event import AttendanceEvent


def rank_attendance(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[tuple[str, int], ...]:
    """
    Rank members by the number of attended sessions.

    Present and Late are both counted as attendance.

    Returns
    -------
    tuple[tuple[str, int], ...]
        (member_id, attendance_count) sorted descending.
    """
    counter: Counter[str] = Counter()

    for event in attendance_events:
        if event.attendance_type in (
            AttendanceType.PRESENT,
            AttendanceType.LATE,
        ):
            counter[event.member_id] += 1

    return tuple(counter.most_common())


def rank_lateness(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[tuple[str, int], ...]:
    """
    Rank members by lateness count.

    Higher values indicate more late arrivals.
    """
    counter: Counter[str] = Counter()

    for event in attendance_events:
        if event.attendance_type == AttendanceType.LATE:
            counter[event.member_id] += 1

    return tuple(counter.most_common())


def rank_activities(
    activity_events: Iterable[ActivityEvent],
) -> tuple[tuple[str, int], ...]:
    """
    Rank members by number of recorded activities.
    """
    counter: Counter[str] = Counter()

    for event in activity_events:
        counter[event.member_id] += 1

    return tuple(counter.most_common())


def top_members(
    rankings: Iterable[tuple[str, int]],
    limit: int = 10,
) -> tuple[tuple[str, int], ...]:
    """
    Return the top N ranked members.

    Parameters
    ----------
    rankings:
        Ranking produced by one of the rank_* functions.

    limit:
        Maximum number of results.

    Returns
    -------
    tuple[tuple[str, int], ...]
    """
    return tuple(rankings)[: max(limit, 0)]


def member_rank(
    member_id: str,
    rankings: Iterable[tuple[str, int]],
) -> int | None:
    """
    Return a member's ranking position.

    Positions start at 1.

    Returns
    -------
    int | None
        Ranking position or None if member is not ranked.
    """
    for position, (current_member, _) in enumerate(rankings, start=1):
        if current_member == member_id:
            return position

    return None
