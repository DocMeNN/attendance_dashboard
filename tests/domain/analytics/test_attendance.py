# tests/domain/analytics/test_attendance.py

"""
Tests for Domain Attendance Analytics.
"""

from datetime import datetime

import pytest

from src.domain.analytics.attendance import (
    attendance_rate,
    attendance_summary,
    count_attendance_events,
    count_participants,
    first_attendance_event,
    first_participant,
    get_attendance_events,
    get_participants,
    has_attendance,
    is_present,
    last_attendance_event,
    last_participant,
    participant_exists,
)
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.message import Message


@pytest.fixture
def events() -> tuple[AttendanceEvent, ...]:
    """Return sample attendance events."""
    return (
        AttendanceEvent(
            attendee="Alice",
            source_message=Message(
                timestamp=datetime(2026, 7, 22, 8, 30),
                sender="Alice",
                content="Done",
                line_number=3,
            ),
        ),
        AttendanceEvent(
            attendee="Bob",
            source_message=Message(
                timestamp=datetime(2026, 7, 22, 8, 15),
                sender="Bob",
                content="Insight",
                line_number=2,
            ),
        ),
        AttendanceEvent(
            attendee="alice",
            source_message=Message(
                timestamp=datetime(2026, 7, 22, 9, 0),
                sender="Alice",
                content="Discussion",
                line_number=4,
            ),
        ),
    )


def test_events_are_sorted_chronologically(
    events: tuple[AttendanceEvent, ...],
) -> None:
    """Events should be returned in chronological order."""
    result = get_attendance_events(events)

    assert [event.attendee for event in result] == [
        "Bob",
        "Alice",
        "alice",
    ]


def test_get_participants_returns_unique_participants_in_first_seen_order(
    events: tuple[AttendanceEvent, ...],
) -> None:
    """Participants should be unique and preserve first participation order."""
    assert get_participants(events) == ("Bob", "Alice")


def test_participant_exists_is_case_insensitive(
    events: tuple[AttendanceEvent, ...],
) -> None:
    """Participant lookup should be case-insensitive."""
    assert participant_exists(events, "alice") is True
    assert participant_exists(events, "ALICE") is True
    assert participant_exists(events, "Charlie") is False


def test_count_attendance_events(
    events: tuple[AttendanceEvent, ...],
) -> None:
    """All participation events should be counted."""
    assert count_attendance_events(events) == 3


def test_count_participants(
    events: tuple[AttendanceEvent, ...],
) -> None:
    """Unique participants should be counted."""
    assert count_participants(events) == 2


def test_first_and_last_attendance_events(
    events: tuple[AttendanceEvent, ...],
) -> None:
    """First and last events should be identified chronologically."""
    assert first_attendance_event(events).attendee == "Bob"
    assert last_attendance_event(events).attendee == "alice"


def test_first_and_last_participants(
    events: tuple[AttendanceEvent, ...],
) -> None:
    """First and last participants should be identified."""
    assert first_participant(events) == "Bob"
    assert last_participant(events) == "alice"


def test_empty_events_return_none() -> None:
    """Empty attendance should have no first or last event."""
    assert first_attendance_event([]) is None
    assert last_attendance_event([]) is None
    assert first_participant([]) is None
    assert last_participant([]) is None


def test_has_attendance(
    events: tuple[AttendanceEvent, ...],
) -> None:
    """Attendance should be detected when events exist."""
    assert has_attendance(events) is True
    assert has_attendance([]) is False


def test_is_present(
    events: tuple[AttendanceEvent, ...],
) -> None:
    """Participation should determine presence."""
    assert is_present(events, "Alice") is True
    assert is_present(events, "Charlie") is False


def test_attendance_summary(
    events: tuple[AttendanceEvent, ...],
) -> None:
    """Attendance summary should contain the expected values."""
    summary = attendance_summary(events)

    assert summary["attendance_event_count"] == 3
    assert summary["participant_count"] == 2
    assert summary["participants"] == ("Bob", "Alice")
    assert summary["first_participant"] == "Bob"
    assert summary["last_participant"] == "alice"


@pytest.mark.parametrize(
    ("expected_attendees", "expected_rate"),
    [
        (0, 0.0),
        (1, 200.0),
        (2, 100.0),
        (4, 50.0),
    ],
)
def test_attendance_rate(
    events: tuple[AttendanceEvent, ...],
    expected_attendees: int,
    expected_rate: float,
) -> None:
    """Participation rate should be based on unique participants."""
    assert attendance_rate(events, expected_attendees) == expected_rate


def test_generator_input_is_supported() -> None:
    """Analytics should support iterable inputs."""
    messages = (
        Message(
            timestamp=datetime(2026, 7, 22, 8, 0),
            sender="Alice",
            content="Done",
            line_number=1,
        ),
        Message(
            timestamp=datetime(2026, 7, 22, 8, 1),
            sender="Bob",
            content="Done",
            line_number=2,
        ),
    )

    generator = (
        AttendanceEvent(
            attendee=message.sender,
            source_message=message,
        )
        for message in messages
    )

    assert count_participants(generator) == 2
