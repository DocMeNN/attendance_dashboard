# src/domain/analytics/leaderboards.py

"""
Domain Leaderboard Analytics

Purpose
-------
Provides pure business logic for ranking member participation
across sessions.

Responsibilities
----------------
- Rank members by participation frequency.
- Rank members by activity frequency.
- Rank members by Scripture Reading acknowledgement frequency.
- Return top-ranked entries.
- Locate a participant's ranking.

Notes
-----
- Operates only on immutable Domain models.
- Rankings are returned in descending order.
- Attendance is participation of any kind within a session.
- There is no late or absent attendance classification.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections import Counter
from collections.abc import Iterable

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.attendance_event import AttendanceEvent

# ============================================================================
# Participation Rankings
# ============================================================================


def rank_participation(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[tuple[str, int], ...]:
    """
    Rank members by participation frequency.

    Each attendance event represents participation within a session.
    """

    counter: Counter[str] = Counter()

    for attendance_event in attendance_events:
        counter[attendance_event.attendee] += 1

    return tuple(
        counter.most_common(),
    )


# ============================================================================
# Activity Rankings
# ============================================================================


def rank_activities(
    activity_events: Iterable[ActivityEvent],
) -> tuple[tuple[str, int], ...]:
    """
    Rank members by activity frequency.

    Each activity event contributes one activity participation
    to the sender's total.
    """

    counter: Counter[str] = Counter()

    for activity_event in activity_events:
        counter[activity_event.sender] += 1

    return tuple(
        counter.most_common(),
    )


# ============================================================================
# Combined Participation Rankings
# ============================================================================


def rank_total_participation(
    attendance_events: Iterable[AttendanceEvent],
    activity_events: Iterable[ActivityEvent],
) -> tuple[tuple[str, int], ...]:
    """
    Rank members by total participation.

    Total participation is the combined count of:

    - Attendance participation events.
    - Activity events.

    This provides a broader participation ranking than
    attendance or activity ranking alone.
    """

    counter: Counter[str] = Counter()

    for attendance_event in attendance_events:
        counter[attendance_event.attendee] += 1

    for activity_event in activity_events:
        counter[activity_event.sender] += 1

    return tuple(
        counter.most_common(),
    )


# ============================================================================
# Ranking Utilities
# ============================================================================


def top_members(
    rankings: Iterable[tuple[str, int]],
    limit: int = 10,
) -> tuple[tuple[str, int], ...]:
    """
    Return the top-ranked participants.

    Parameters
    ----------
    rankings:
        Ranking produced by a ranking function.

    limit:
        Maximum number of entries to return.
    """

    if limit < 0:
        raise ValueError(
            "limit cannot be negative.",
        )

    return tuple(
        rankings,
    )[:limit]


def participant_rank(
    participant: str,
    rankings: Iterable[tuple[str, int]],
) -> int | None:
    """
    Return the ranking position of a participant.

    Ranking positions start at 1.

    Matching is case-insensitive.
    """

    normalized = participant.casefold()

    for position, (current, _) in enumerate(
        rankings,
        start=1,
    ):
        if current.casefold() == normalized:
            return position

    return None
