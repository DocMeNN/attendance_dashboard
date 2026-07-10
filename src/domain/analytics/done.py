# src/domain/analytics/done.py

"""
Domain Done Analytics

Purpose
-------
Provides pure business logic for Done acknowledgement analytics.

Responsibilities
----------------
- Filter Done events.
- Count Done events.
- Determine first and last Done acknowledgements.
- Remove duplicate Done events according to business rules.
- Remain technology independent.

Rules
-----
- No pandas.
- No Streamlit.
- No plotting.
- No file I/O.
- No infrastructure dependencies.

Business Rules
--------------
- Every Done acknowledgement is counted.
- Multiple Done messages from the same attendee are valid.
- Only an identical attendee AND identical timestamp is treated
  as a duplicate.
- Same attendee with different timestamps counts as separate Done
  acknowledgements.

Notes
-----
- Operates only on immutable Domain models.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterable

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.models.done_event import DoneEvent

# ------------------------------------------------------------------
# Retrieval
# ------------------------------------------------------------------


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


# ------------------------------------------------------------------
# Duplicate Handling
# ------------------------------------------------------------------


def unique_done_events(
    done_events: Iterable[DoneEvent],
) -> tuple[DoneEvent, ...]:
    """
    Return Done events with duplicate timestamps removed.

    Duplicate Definition
    --------------------
    Duplicate means:

        attendee + timestamp

    If the timestamp differs, the Done acknowledgement
    remains valid and is retained.
    """

    unique: list[DoneEvent] = []
    seen: set[tuple[str, object]] = set()

    for event in get_done_events(done_events):

        key = (
            event.attendee.casefold(),
            event.timestamp,
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(event)

    return tuple(unique)


# ------------------------------------------------------------------
# Counts
# ------------------------------------------------------------------


def count_done_events(
    done_events: Iterable[DoneEvent],
) -> int:
    """
    Return the total number of valid Done events.

    Duplicate Done acknowledgements are ignored using
    the Domain duplicate rule.
    """

    return len(unique_done_events(done_events))


# ------------------------------------------------------------------
# Timeline
# ------------------------------------------------------------------


def first_done_event(
    done_events: Iterable[DoneEvent],
) -> DoneEvent | None:
    """
    Return the first valid Done acknowledgement.

    Returns
    -------
    DoneEvent | None
    """

    events = unique_done_events(done_events)

    if not events:
        return None

    return events[0]


# ------------------------------------------------------------------
# Timeline
# ------------------------------------------------------------------


def last_done_event(
    done_events: Iterable[DoneEvent],
) -> DoneEvent | None:
    """
    Return the last valid Done acknowledgement.

    Returns
    -------
    DoneEvent | None
    """

    events = unique_done_events(done_events)

    if not events:
        return None

    return events[-1]


# ------------------------------------------------------------------
# Attendee Analytics
# ------------------------------------------------------------------


def done_attendees(
    done_events: Iterable[DoneEvent],
) -> tuple[str, ...]:
    """
    Return attendees that submitted a Done acknowledgement.

    Order is preserved according to the first valid
    Done acknowledgement.
    """

    attendees: list[str] = []
    seen: set[str] = set()

    for event in unique_done_events(done_events):

        key = event.attendee.casefold()

        if key in seen:
            continue

        seen.add(key)
        attendees.append(event.attendee)

    return tuple(attendees)


def done_count_by_attendee(
    done_events: Iterable[DoneEvent],
    attendee: str,
) -> int:
    """
    Return the number of valid Done acknowledgements
    submitted by an attendee.

    Different timestamps are counted separately.
    """

    normalized = attendee.casefold()

    return sum(
        event.attendee.casefold() == normalized
        for event in unique_done_events(done_events)
    )


def has_done_event(
    done_events: Iterable[DoneEvent],
) -> bool:
    """
    Return True if at least one valid Done event exists.
    """

    return bool(unique_done_events(done_events))


# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------


def done_summary(
    done_events: Iterable[DoneEvent],
) -> dict[str, object]:
    """
    Return a summary of Done acknowledgements.
    """

    events = unique_done_events(done_events)

    return {
        "done_count": len(events),
        "unique_attendees": len(done_attendees(events)),
        "first_done": first_done_event(events),
        "last_done": last_done_event(events),
    }


# ------------------------------------------------------------------
# Convenience
# ------------------------------------------------------------------


def first_done_attendee(
    done_events: Iterable[DoneEvent],
) -> str | None:
    """
    Return the attendee that submitted the first
    valid Done acknowledgement.
    """

    event = first_done_event(done_events)

    if event is None:
        return None

    return event.attendee


def last_done_attendee(
    done_events: Iterable[DoneEvent],
) -> str | None:
    """
    Return the attendee that submitted the last
    valid Done acknowledgement.
    """

    event = last_done_event(done_events)

    if event is None:
        return None

    return event.attendee
