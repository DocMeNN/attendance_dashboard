# src/domain/analytics/activity.py

"""
Domain Activity Analytics

Purpose
-------
Provides pure business logic for meeting activity analytics.

Responsibilities
----------------
- Filter activity events.
- Count activity events.
- Count activities by ActivityType.
- Determine first and last activities.
- Provide activity lookup utilities.
- Remain technology independent.

Rules
-----
- No pandas.
- No Streamlit.
- No plotting.
- No reporting.
- No infrastructure dependencies.

Notes
-----
- Operates only on immutable Domain models.
- Contains only business logic.
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
from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent

# ------------------------------------------------------------------
# Retrieval
# ------------------------------------------------------------------


def get_activity_events(
    activity_events: Iterable[ActivityEvent],
) -> tuple[ActivityEvent, ...]:
    """
    Return activity events ordered chronologically.
    """

    return tuple(
        sorted(
            activity_events,
            key=lambda event: event.timestamp,
        )
    )


def get_events_by_type(
    activity_events: Iterable[ActivityEvent],
    activity_type: ActivityType,
) -> tuple[ActivityEvent, ...]:
    """
    Return all activity events of the specified type.
    """

    return tuple(
        event
        for event in get_activity_events(activity_events)
        if event.activity_type is activity_type
    )


# ------------------------------------------------------------------
# Counts
# ------------------------------------------------------------------


def count_activity_events(
    activity_events: Iterable[ActivityEvent],
) -> int:
    """
    Return total activity event count.
    """

    return len(get_activity_events(activity_events))


def count_activity_types(
    activity_events: Iterable[ActivityEvent],
) -> Counter[ActivityType]:
    """
    Count activity events grouped by ActivityType.
    """

    return Counter(event.activity_type for event in activity_events)


# ------------------------------------------------------------------
# Timeline
# ------------------------------------------------------------------


def first_activity_event(
    activity_events: Iterable[ActivityEvent],
) -> ActivityEvent | None:
    """
    Return the first recorded activity.
    """

    events = get_activity_events(activity_events)

    if not events:
        return None

    return events[0]


def last_activity_event(
    activity_events: Iterable[ActivityEvent],
) -> ActivityEvent | None:
    """
    Return the last recorded activity.
    """

    events = get_activity_events(activity_events)

    if not events:
        return None

    return events[-1]


# ------------------------------------------------------------------
# Activity Lookup
# ------------------------------------------------------------------


def has_activity(
    activity_events: Iterable[ActivityEvent],
    activity_type: ActivityType,
) -> bool:
    """
    Return True if the specified activity exists.
    """

    return bool(
        get_events_by_type(
            activity_events,
            activity_type,
        )
    )


def activity_names(
    activity_events: Iterable[ActivityEvent],
) -> tuple[str, ...]:
    """
    Return activity names preserving chronological order.
    """

    return tuple(event.activity_name for event in get_activity_events(activity_events))


# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------


def activity_summary(
    activity_events: Iterable[ActivityEvent],
) -> dict[str, object]:
    """
    Return a summary of activity events.
    """

    events = get_activity_events(activity_events)

    return {
        "activity_count": count_activity_events(events),
        "activity_types": count_activity_types(events),
        "first_activity": first_activity_event(events),
        "last_activity": last_activity_event(events),
    }


# ------------------------------------------------------------------
# Convenience
# ------------------------------------------------------------------


def first_activity_type(
    activity_events: Iterable[ActivityEvent],
) -> ActivityType | None:
    """
    Return the ActivityType of the first activity.
    """

    event = first_activity_event(activity_events)

    if event is None:
        return None

    return event.activity_type


def last_activity_type(
    activity_events: Iterable[ActivityEvent],
) -> ActivityType | None:
    """
    Return the ActivityType of the last activity.
    """

    event = last_activity_event(activity_events)

    if event is None:
        return None

    return event.activity_type


def first_activity_name(
    activity_events: Iterable[ActivityEvent],
) -> str | None:
    """
    Return the name of the first activity.
    """

    event = first_activity_event(activity_events)

    if event is None:
        return None

    return event.activity_name


def last_activity_name(
    activity_events: Iterable[ActivityEvent],
) -> str | None:
    """
    Return the name of the last activity.
    """

    event = last_activity_event(activity_events)

    if event is None:
        return None

    return event.activity_name


def unique_activity_types(
    activity_events: Iterable[ActivityEvent],
) -> tuple[ActivityType, ...]:
    """
    Return unique ActivityTypes preserving chronological order.
    """

    seen: set[ActivityType] = set()
    unique: list[ActivityType] = []

    for event in get_activity_events(activity_events):

        if event.activity_type in seen:
            continue

        seen.add(event.activity_type)
        unique.append(event.activity_type)

    return tuple(unique)
