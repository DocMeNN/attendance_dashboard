# src/domain/analytics/attendance.py

"""
Domain Attendance Analytics

Purpose
-------
Provides pure business logic for attendance and participation analytics.

Domain Rule
-----------
Attendance is participation of any kind within a session.

Therefore:
- Any attendance event represents participation.
- Attendance is counted as Present.
- There is no Late classification.
- There is no Absent classification at session participation level.
- Done acknowledgements are analysed separately.
- Activity events are analysed separately.
- Attendance is based on unique participants.

Responsibilities
----------------
- Retrieve attendance events.
- Determine unique participants.
- Count participation.
- Identify first and last participants.
- Determine whether a participant participated.
- Provide attendance summaries.

Rules
-----
- No pandas.
- No Streamlit.
- No plotting.
- No reporting.
- No infrastructure dependencies.
- No UI dependencies.

Notes
-----
- Operates only on immutable domain models.
- Contains pure domain business logic.
- Attendance means participation within a session.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterable

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.models.attendance_event import AttendanceEvent

# ============================================================================
# Retrieval
# ============================================================================


def get_attendance_events(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[AttendanceEvent, ...]:
    """
    Return attendance events ordered chronologically.
    """

    return tuple(
        sorted(
            attendance_events,
            key=lambda event: event.timestamp,
        )
    )


# ============================================================================
# Participant Retrieval
# ============================================================================


def get_participants(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[str, ...]:
    """
    Return unique participants in chronological order of first participation.

    Attendance is participation of any kind within a session.
    """

    seen: set[str] = set()
    participants: list[str] = []

    for event in get_attendance_events(attendance_events):
        normalized = event.attendee.casefold()

        if normalized in seen:
            continue

        seen.add(normalized)
        participants.append(event.attendee)

    return tuple(participants)


def participant_exists(
    attendance_events: Iterable[AttendanceEvent],
    attendee: str,
) -> bool:
    """
    Return True if the attendee participated.
    """

    normalized = attendee.casefold()

    return any(
        participant.casefold() == normalized
        for participant in get_participants(attendance_events)
    )


# ============================================================================
# Counts
# ============================================================================


def count_attendance_events(
    attendance_events: Iterable[AttendanceEvent],
) -> int:
    """
    Return the total number of attendance events.

    This represents the number of recorded participation events.
    """

    return len(
        get_attendance_events(
            attendance_events,
        )
    )


def count_participants(
    attendance_events: Iterable[AttendanceEvent],
) -> int:
    """
    Return the number of unique participants.
    """

    return len(
        get_participants(
            attendance_events,
        )
    )


# ============================================================================
# Timeline
# ============================================================================


def first_attendance_event(
    attendance_events: Iterable[AttendanceEvent],
) -> AttendanceEvent | None:
    """
    Return the first participation event.
    """

    events = get_attendance_events(
        attendance_events,
    )

    if not events:
        return None

    return events[0]


def last_attendance_event(
    attendance_events: Iterable[AttendanceEvent],
) -> AttendanceEvent | None:
    """
    Return the last participation event.
    """

    events = get_attendance_events(
        attendance_events,
    )

    if not events:
        return None

    return events[-1]


def first_participant(
    attendance_events: Iterable[AttendanceEvent],
) -> str | None:
    """
    Return the first participant.
    """

    event = first_attendance_event(
        attendance_events,
    )

    if event is None:
        return None

    return event.attendee


def last_participant(
    attendance_events: Iterable[AttendanceEvent],
) -> str | None:
    """
    Return the last participant.
    """

    event = last_attendance_event(
        attendance_events,
    )

    if event is None:
        return None

    return event.attendee


# ============================================================================
# Attendance Status
# ============================================================================


def has_attendance(
    attendance_events: Iterable[AttendanceEvent],
) -> bool:
    """
    Return True if at least one participation event exists.
    """

    return (
        count_participants(
            attendance_events,
        )
        > 0
    )


def is_present(
    attendance_events: Iterable[AttendanceEvent],
    attendee: str,
) -> bool:
    """
    Return True if the attendee participated in the session.

    Participation is the domain definition of presence.
    """

    return participant_exists(
        attendance_events,
        attendee,
    )


# ============================================================================
# Summary
# ============================================================================


def attendance_summary(
    attendance_events: Iterable[AttendanceEvent],
) -> dict[str, object]:
    """
    Return a summary of attendance participation.
    """

    events = get_attendance_events(
        attendance_events,
    )

    participants = get_participants(
        events,
    )

    return {
        "attendance_event_count": len(events),
        "participant_count": len(participants),
        "participants": participants,
        "first_attendance": first_attendance_event(events),
        "last_attendance": last_attendance_event(events),
        "first_participant": first_participant(events),
        "last_participant": last_participant(events),
    }


# ============================================================================
# Convenience
# ============================================================================


def attendance_rate(
    attendance_events: Iterable[AttendanceEvent],
    expected_attendees: int,
) -> float:
    """
    Return participation rate as a percentage.

    Attendance is based on unique participants.
    """

    if expected_attendees <= 0:
        return 0.0

    return round(
        (
            count_participants(
                attendance_events,
            )
            / expected_attendees
        )
        * 100,
        2,
    )
