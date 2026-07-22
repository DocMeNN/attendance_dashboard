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
- Determine unique activity types.
- Determine first and last activities.
- Provide activity lookup utilities.
- Provide activity value counts.
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
- Activity analytics are session-oriented.
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

# ============================================================================
# Retrieval
# ============================================================================


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


# ============================================================================
# Counts
# ============================================================================


def count_activity_events(
    activity_events: Iterable[ActivityEvent],
) -> int:
    """
    Return the total number of activity events.
    """

    return len(
        get_activity_events(
            activity_events,
        )
    )


def count_activity_types(
    activity_events: Iterable[ActivityEvent],
) -> Counter[ActivityType]:
    """
    Count activity events grouped by ActivityType.

    Example
    -------
    {
        ActivityType.PRAYER: 2,
        ActivityType.SCRIPTURE_READING: 1,
        ActivityType.WORSHIP: 1,
    }
    """

    return Counter(event.activity_type for event in activity_events)


def activity_value_counts(
    activity_events: Iterable[ActivityEvent],
) -> Counter[ActivityType]:
    """
    Return frequency counts of each activity type.

    This is the domain equivalent of value_counts
    for activity classifications.
    """

    return count_activity_types(
        activity_events,
    )


def count_unique_activity_types(
    activity_events: Iterable[ActivityEvent],
) -> int:
    """
    Return the number of unique activity types.
    """

    return len(set(event.activity_type for event in activity_events))


# ============================================================================
# Timeline
# ============================================================================


def first_activity_event(
    activity_events: Iterable[ActivityEvent],
) -> ActivityEvent | None:
    """
    Return the first recorded activity.
    """

    events = get_activity_events(
        activity_events,
    )

    if not events:
        return None

    return events[0]


def last_activity_event(
    activity_events: Iterable[ActivityEvent],
) -> ActivityEvent | None:
    """
    Return the last recorded activity.
    """

    events = get_activity_events(
        activity_events,
    )

    if not events:
        return None

    return events[-1]


# ============================================================================
# Activity Lookup
# ============================================================================


def has_activity(
    activity_events: Iterable[ActivityEvent],
    activity_type: ActivityType,
) -> bool:
    """
    Return True if the specified activity exists.
    """

    return any(event.activity_type is activity_type for event in activity_events)


def activity_names(
    activity_events: Iterable[ActivityEvent],
) -> tuple[str, ...]:
    """
    Return activity names preserving chronological order.
    """

    return tuple(
        event.activity_name
        for event in get_activity_events(
            activity_events,
        )
    )


# ============================================================================
# Unique Activities
# ============================================================================


def unique_activity_types(
    activity_events: Iterable[ActivityEvent],
) -> tuple[ActivityType, ...]:
    """
    Return unique ActivityTypes preserving chronological order.
    """

    seen: set[ActivityType] = set()

    unique: list[ActivityType] = []

    for event in get_activity_events(
        activity_events,
    ):
        if event.activity_type in seen:
            continue

        seen.add(
            event.activity_type,
        )

        unique.append(
            event.activity_type,
        )

    return tuple(
        unique,
    )


def unique_activity_names(
    activity_events: Iterable[ActivityEvent],
) -> tuple[str, ...]:
    """
    Return unique activity names preserving chronological order.
    """

    return tuple(
        activity_type.name.replace(
            "_",
            " ",
        ).title()
        for activity_type in unique_activity_types(
            activity_events,
        )
    )


# ============================================================================
# Summary
# ============================================================================


def activity_summary(
    activity_events: Iterable[ActivityEvent],
) -> dict[str, object]:
    """
    Return a summary of activity events.

    Summary includes:

    - Total activity event count.
    - Number of unique activity types.
    - Value counts by activity type.
    - Unique activity types.
    - First activity.
    - Last activity.
    """

    events = get_activity_events(
        activity_events,
    )

    counts = activity_value_counts(
        events,
    )

    unique_types = unique_activity_types(
        events,
    )

    return {
        "activity_count": len(events),
        "unique_activity_count": len(unique_types),
        "activity_types": counts,
        "activity_value_counts": counts,
        "unique_activity_types": unique_types,
        "first_activity": first_activity_event(events),
        "last_activity": last_activity_event(events),
    }


# ============================================================================
# Convenience
# ============================================================================


def first_activity_type(
    activity_events: Iterable[ActivityEvent],
) -> ActivityType | None:
    """
    Return the ActivityType of the first activity.
    """

    event = first_activity_event(
        activity_events,
    )

    if event is None:
        return None

    return event.activity_type


def last_activity_type(
    activity_events: Iterable[ActivityEvent],
) -> ActivityType | None:
    """
    Return the ActivityType of the last activity.
    """

    event = last_activity_event(
        activity_events,
    )

    if event is None:
        return None

    return event.activity_type


def first_activity_name(
    activity_events: Iterable[ActivityEvent],
) -> str | None:
    """
    Return the name of the first activity.
    """

    event = first_activity_event(
        activity_events,
    )

    if event is None:
        return None

    return event.activity_name


def last_activity_name(
    activity_events: Iterable[ActivityEvent],
) -> str | None:
    """
    Return the name of the last activity.
    """

    event = last_activity_event(
        activity_events,
    )

    if event is None:
        return None

    return event.activity_name
