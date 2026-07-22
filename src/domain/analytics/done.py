# src/domain/analytics/done.py

"""
Domain Done Analytics

Purpose
-------
Provides business logic for Scripture Reading acknowledgement analytics.

Responsibilities
----------------
- Retrieve Done acknowledgement events.
- Count Done acknowledgements.
- Count acknowledgements by member.
- Rank members by acknowledgement count.
- Support reporting-period analysis.
- Preserve every Done acknowledgement as an independent event.

Domain Rules
------------
- A DoneEvent represents one Scripture Reading acknowledgement.
- Every DoneEvent counts independently.
- Multiple DoneEvents from the same member must not be deduplicated.
- Done acknowledgements are independent of session boundaries.
- Session detection determines when a Scripture Reading activity occurs,
  but Done acknowledgements may refer to the current or a previous reading.
- Weekly and monthly Done totals are therefore based on the reporting period,
  not on session membership.

Notes
-----
- Pure domain analytics.
- No pandas.
- No Streamlit.
- No database access.
- No file I/O.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections import Counter
from collections.abc import Iterable
from datetime import date, datetime

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.models.done_event import DoneEvent

# ============================================================================
# Retrieval
# ============================================================================


def get_done_events(
    done_events: Iterable[DoneEvent],
) -> tuple[DoneEvent, ...]:
    """
    Return Done events ordered chronologically.
    """

    return tuple(
        sorted(
            done_events,
            key=lambda event: event.timestamp,
        )
    )


def get_done_events_for_member(
    done_events: Iterable[DoneEvent],
    attendee: str,
) -> tuple[DoneEvent, ...]:
    """
    Return all Done events belonging to a member.

    Matching is case-insensitive.
    """

    normalized = attendee.casefold()

    return tuple(
        event
        for event in get_done_events(done_events)
        if event.attendee.casefold() == normalized
    )


def get_done_events_between(
    done_events: Iterable[DoneEvent],
    start: datetime,
    end: datetime,
) -> tuple[DoneEvent, ...]:
    """
    Return Done events within a datetime range.

    The range is inclusive at both boundaries.
    """

    return tuple(
        event
        for event in get_done_events(done_events)
        if start <= event.timestamp <= end
    )


def get_done_events_on_date(
    done_events: Iterable[DoneEvent],
    event_date: date,
) -> tuple[DoneEvent, ...]:
    """
    Return Done events recorded on a specific date.
    """

    return tuple(
        event
        for event in get_done_events(done_events)
        if event.event_date == event_date
    )


# ============================================================================
# Counts
# ============================================================================


def count_done_events(
    done_events: Iterable[DoneEvent],
) -> int:
    """
    Return the total number of Done acknowledgements.

    Every DoneEvent counts independently.
    """

    return len(get_done_events(done_events))


def count_done_for_member(
    done_events: Iterable[DoneEvent],
    attendee: str,
) -> int:
    """
    Return the total number of Done acknowledgements
    recorded by a member.
    """

    return len(
        get_done_events_for_member(
            done_events,
            attendee,
        )
    )


def count_done_by_member(
    done_events: Iterable[DoneEvent],
) -> Counter[str]:
    """
    Count Done acknowledgements by member.

    Member names are normalized for case-insensitive
    counting while preserving the first encountered
    display name.
    """

    counts: Counter[str] = Counter()
    display_names: dict[str, str] = {}

    for event in get_done_events(done_events):
        key = event.attendee.casefold()

        if key not in display_names:
            display_names[key] = event.attendee

        counts[display_names[key]] += 1

    return counts


def unique_done_member_count(
    done_events: Iterable[DoneEvent],
) -> int:
    """
    Return the number of unique members with at least
    one Done acknowledgement.
    """

    return len(count_done_by_member(done_events))


# ============================================================================
# Ranking
# ============================================================================


def rank_members_by_done_count(
    done_events: Iterable[DoneEvent],
) -> tuple[tuple[str, int], ...]:
    """
    Rank members by total Done acknowledgements.

    Members with equal counts are ordered alphabetically.
    """

    counts = count_done_by_member(done_events)

    return tuple(
        sorted(
            counts.items(),
            key=lambda item: (
                -item[1],
                item[0].casefold(),
            ),
        )
    )


def top_done_members(
    done_events: Iterable[DoneEvent],
    limit: int = 10,
) -> tuple[tuple[str, int], ...]:
    """
    Return the members with the highest Done counts.
    """

    if limit < 1:
        raise ValueError("limit must be greater than zero.")

    return rank_members_by_done_count(done_events)[:limit]


# ============================================================================
# Period Analytics
# ============================================================================


def done_count_by_date(
    done_events: Iterable[DoneEvent],
) -> Counter[date]:
    """
    Count Done acknowledgements by calendar date.
    """

    return Counter(event.event_date for event in done_events)


def done_count_by_period(
    done_events: Iterable[DoneEvent],
    start_date: date,
    end_date: date,
) -> int:
    """
    Return the number of Done acknowledgements
    within an inclusive date range.

    This is independent of session boundaries.
    """

    if start_date > end_date:
        raise ValueError("start_date cannot be later than end_date.")

    return sum(1 for event in done_events if start_date <= event.event_date <= end_date)


def done_count_by_member_for_period(
    done_events: Iterable[DoneEvent],
    start_date: date,
    end_date: date,
) -> Counter[str]:
    """
    Count Done acknowledgements by member
    within an inclusive reporting period.

    Every acknowledgement is counted independently.
    """

    if start_date > end_date:
        raise ValueError("start_date cannot be later than end_date.")

    return count_done_by_member(
        event for event in done_events if start_date <= event.event_date <= end_date
    )


# ============================================================================
# Summary
# ============================================================================


def done_summary(
    done_events: Iterable[DoneEvent],
) -> dict[str, object]:
    """
    Return a summary of Done acknowledgement analytics.
    """

    events = get_done_events(done_events)

    return {
        "done_count": len(events),
        "unique_member_count": unique_done_member_count(events),
        "done_by_member": count_done_by_member(events),
        "done_by_date": done_count_by_date(events),
        "first_done": events[0] if events else None,
        "last_done": events[-1] if events else None,
    }
