# src/domain/policies/attendance_policy.py

"""
Attendance Policy

Purpose
-------
Defines the business rules for determining participation-based
attendance within an OYBS study session.

Responsibilities
----------------
- Determine whether a message represents participation.
- Determine whether a participant is present.
- Apply the OYBS attendance rule.
- Keep attendance independent from Done acknowledgements.

Domain Rules
------------
Attendance is participation.

A participant is considered PRESENT when they perform any
recognized participation activity within a session.

Recognized participation includes:

- Scripture Reading
- Insight
- Discussion
- Announcement
- Done
- Prayer Session participation

Important
---------
- There is no LATE classification.
- There is no ABSENT classification derived from chat activity.
- A participant is either present through participation or has
  no recorded participation within the session.
- Multiple activities by the same participant within a session
  do not create multiple attendance records.
- Done acknowledgements are participation events, but Done counts
  remain independent and may be counted separately.
- A participant may have multiple Done acknowledgements across
  a reporting period.
- Attendance is session-based.
- Done acknowledgement analytics may be reporting-period based.

Architecture
------------
This module contains domain policy only.

- No pandas.
- No Streamlit.
- No infrastructure dependencies.
- No UI dependencies.

Author
------
OYBS Attendance Dashboard

Created
-------
July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterable

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.enums.attendance_type import AttendanceType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.done_event import DoneEvent
from src.domain.models.message import Message

# ============================================================================
# Participation Detection
# ============================================================================


def is_participation_message(
    message: Message,
) -> bool:
    """
    Return True if the message represents participation.

    Any valid message sent by a participant is considered
    participation within the session.

    System messages should already have been excluded by the
    import/parsing pipeline before reaching this policy.
    """

    if not isinstance(
        message,
        Message,
    ):
        raise TypeError(
            "message must be a Message.",
        )

    return bool(message.sender.strip())


def is_participating_sender(
    sender: str,
) -> bool:
    """
    Return True if a sender can be considered a participant.
    """

    return bool(sender.strip())


# ============================================================================
# Attendance Classification
# ============================================================================


def classify_attendance(
    message: Message,
) -> AttendanceType:
    """
    Classify a message for attendance purposes.

    Returns
    -------
    AttendanceType.PRESENT
        When the message represents participation.

    AttendanceType.UNKNOWN
        When the message cannot be treated as valid participation.

    Notes
    -----
    Attendance is participation-based.

    The domain does not classify participants as:

    - LATE
    - ABSENT

    Those concepts are intentionally not used for OYBS
    participation attendance.
    """

    if is_participation_message(
        message,
    ):
        return AttendanceType.PRESENT

    return AttendanceType.UNKNOWN


def is_present(
    message: Message,
) -> bool:
    """
    Return True if a message represents present participation.
    """

    return (
        classify_attendance(
            message,
        )
        is AttendanceType.PRESENT
    )


# ============================================================================
# Event-Based Attendance
# ============================================================================


def attendance_from_message(
    message: Message,
) -> AttendanceEvent | None:
    """
    Create an AttendanceEvent from a participating message.

    Returns
    -------
    AttendanceEvent | None
        A present attendance event when the message represents
        participation.

    Notes
    -----
    This function creates an event for the source participation.

    Session-level deduplication of participants is handled by
    the Session aggregate.
    """

    if (
        classify_attendance(
            message,
        )
        is not AttendanceType.PRESENT
    ):
        return None

    return AttendanceEvent(
        attendee=message.sender,
        source_message=message,
    )


def attendance_from_activity(
    activity_event: ActivityEvent,
) -> AttendanceEvent:
    """
    Create a present AttendanceEvent from an activity event.

    Every recognized activity represents participation by the
    activity event's sender.
    """

    if not isinstance(
        activity_event,
        ActivityEvent,
    ):
        raise TypeError(
            "activity_event must be an ActivityEvent.",
        )

    return AttendanceEvent(
        attendee=activity_event.sender,
        source_message=activity_event.source_message,
    )


def attendance_from_done(
    done_event: DoneEvent,
) -> AttendanceEvent:
    """
    Create a present AttendanceEvent from a Done acknowledgement.

    A Done acknowledgement is participation.

    The DoneEvent itself remains a separate event because:

    - Attendance answers: Was the participant present?
    - Done analytics answer: How many acknowledgements occurred?
    """

    if not isinstance(
        done_event,
        DoneEvent,
    ):
        raise TypeError(
            "done_event must be a DoneEvent.",
        )

    return AttendanceEvent(
        attendee=done_event.attendee,
        source_message=done_event.source_message,
    )


# ============================================================================
# Participant Extraction
# ============================================================================


def participating_senders(
    messages: Iterable[Message],
) -> tuple[str, ...]:
    """
    Return unique participating senders.

    Names are deduplicated case-insensitively while preserving
    the first recorded display name and chronological order.
    """

    seen: set[str] = set()
    participants: list[str] = []

    for message in messages:
        if not is_participation_message(
            message,
        ):
            continue

        key = message.sender.casefold()

        if key in seen:
            continue

        seen.add(
            key,
        )

        participants.append(
            message.sender,
        )

    return tuple(
        participants,
    )


def count_participants(
    messages: Iterable[Message],
) -> int:
    """
    Return the number of unique participating members.
    """

    return len(
        participating_senders(
            messages,
        )
    )


# ============================================================================
# Attendance Event Utilities
# ============================================================================


def unique_attendance_events(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[AttendanceEvent, ...]:
    """
    Return one present attendance event per participant.

    The earliest attendance event for each participant is retained.

    This prevents multiple messages from the same participant
    from becoming multiple attendance records within a session.
    """

    seen: set[str] = set()
    unique_events: list[AttendanceEvent] = []

    ordered_events = sorted(
        attendance_events,
        key=lambda event: event.timestamp,
    )

    for event in ordered_events:
        if not event.is_present:
            continue

        key = event.attendee.casefold()

        if key in seen:
            continue

        seen.add(
            key,
        )

        unique_events.append(
            event,
        )

    return tuple(
        unique_events,
    )


def count_present_participants(
    attendance_events: Iterable[AttendanceEvent],
) -> int:
    """
    Return the number of unique present participants.
    """

    return len(
        unique_attendance_events(
            attendance_events,
        )
    )


# ============================================================================
# Attendance Summary
# ============================================================================


def attendance_summary(
    attendance_events: Iterable[AttendanceEvent],
) -> dict[str, object]:
    """
    Return participation-based attendance statistics.
    """

    unique_events = unique_attendance_events(
        attendance_events,
    )

    attendees = tuple(event.attendee for event in unique_events)

    return {
        "present_count": len(
            unique_events,
        ),
        "attendees": attendees,
        "attendance_events": unique_events,
        "has_attendance": bool(
            unique_events,
        ),
    }
