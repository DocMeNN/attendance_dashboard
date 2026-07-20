# src/domain/models/session.py

"""
Session Domain Model

Purpose
-------
Represents a complete meeting session.

Responsibilities
----------------
- Aggregate attendance events.
- Aggregate Done acknowledgement events.
- Aggregate activity events.
- Provide session-level business behaviour.
- Remain technology independent.

Rules
-----
- Immutable.
- Aggregate Root of the Domain.
- No UI.
- No pandas.
- No infrastructure dependencies.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

# ============================================================================
# Local Imports
# ============================================================================
from .activity_event import ActivityEvent
from .attendance_event import AttendanceEvent
from .done_event import DoneEvent

# ============================================================================
# Session
# ============================================================================


@dataclass(frozen=True, slots=True)
class Session:
    """
    Immutable meeting session aggregate.
    """

    session_date: date

    attendance_events: tuple[AttendanceEvent, ...] = field(
        default_factory=tuple,
    )

    done_events: tuple[DoneEvent, ...] = field(
        default_factory=tuple,
    )

    activity_events: tuple[ActivityEvent, ...] = field(
        default_factory=tuple,
    )

    def __post_init__(self) -> None:
        """
        Validate and normalize the session.
        """

        if not isinstance(
            self.session_date,
            date,
        ):
            raise TypeError(
                "session_date must be a date.",
            )

        object.__setattr__(
            self,
            "attendance_events",
            tuple(
                sorted(
                    self.attendance_events,
                    key=lambda event: event.timestamp,
                )
            ),
        )

        object.__setattr__(
            self,
            "done_events",
            tuple(
                sorted(
                    self.done_events,
                    key=lambda event: event.timestamp,
                )
            ),
        )

        object.__setattr__(
            self,
            "activity_events",
            tuple(
                sorted(
                    self.activity_events,
                    key=lambda event: event.timestamp,
                )
            ),
        )

    # ------------------------------------------------------------------
    # Event Counts
    # ------------------------------------------------------------------

    @property
    def attendance_count(self) -> int:
        """
        Return attendance event count.
        """
        return len(self.attendance_events)

    @property
    def done_count(self) -> int:
        """
        Return Done acknowledgement count.
        """
        return len(self.done_events)

    @property
    def activity_count(self) -> int:
        """
        Return activity event count.
        """
        return len(self.activity_events)

    @property
    def total_events(self) -> int:
        """
        Return total event count.
        """
        return self.attendance_count + self.done_count + self.activity_count

    # ------------------------------------------------------------------
    # Attendance
    # ------------------------------------------------------------------

    @property
    def attendees(self) -> tuple[str, ...]:
        """
        Return attendees in chronological order.
        """
        return tuple(event.attendee for event in self.attendance_events)

    @property
    def unique_attendees(self) -> tuple[str, ...]:
        """
        Return unique attendees preserving order.
        """

        seen: set[str] = set()
        attendees: list[str] = []

        for event in self.attendance_events:
            key = event.attendee.casefold()

            if key not in seen:
                seen.add(key)
                attendees.append(event.attendee)

        return tuple(attendees)

    @property
    def present_attendees(self) -> tuple[str, ...]:
        """
        Return attendees marked as present.

        Attendance is derived solely from participants
        found in the exported WhatsApp chat.
        """

        seen: set[str] = set()
        attendees: list[str] = []

        for event in self.attendance_events:
            if event.is_absent:
                continue

            key = event.attendee.casefold()

            if key not in seen:
                seen.add(key)
                attendees.append(event.attendee)

        return tuple(attendees)

    @property
    def attendee_count(self) -> int:
        """
        Return unique attendee count.
        """
        return len(self.unique_attendees)

    @property
    def present_count(self) -> int:
        """
        Return number of participants present.
        """
        return len(self.present_attendees)

    @property
    def late_count(self) -> int:
        """
        Return number of late participants.
        """
        return sum(event.is_late for event in self.attendance_events)

    @property
    def absent_count(self) -> int:
        """
        Return number of explicit absent events.

        WhatsApp exports do not contain a complete
        membership register, so this counts only
        attendance events explicitly classified as
        ABSENT.
        """
        return sum(event.is_absent for event in self.attendance_events)

    @property
    def attendance_types(self) -> dict[str, int]:
        """
        Return attendance classification counts.
        """
        return {
            "present": self.present_count,
            "late": self.late_count,
            "absent": self.absent_count,
            "done": self.done_count,
        }

    @property
    def first_attendance(self) -> AttendanceEvent | None:
        """
        Return first attendance event.
        """

        if not self.attendance_events:
            return None

        return self.attendance_events[0]

    @property
    def last_attendance(self) -> AttendanceEvent | None:
        """
        Return last attendance event.
        """

        if not self.attendance_events:
            return None

        return self.attendance_events[-1]

    @property
    def first_attendee(self) -> str | None:
        """
        Return first attendee.
        """

        event = self.first_attendance

        if event is None:
            return None

        return event.attendee

    # ------------------------------------------------------------------
    # Done Acknowledgements
    # ------------------------------------------------------------------

    @property
    def first_done(self) -> DoneEvent | None:
        """
        Return first Done acknowledgement.
        """

        if not self.done_events:
            return None

        return self.done_events[0]

    @property
    def last_done(self) -> DoneEvent | None:
        """
        Return last Done acknowledgement.
        """

        if not self.done_events:
            return None

        return self.done_events[-1]

    @property
    def has_done(self) -> bool:
        """
        Return True if Done acknowledgements exist.
        """
        return bool(self.done_events)

    # ------------------------------------------------------------------
    # Activities
    # ------------------------------------------------------------------

    @property
    def first_activity(self) -> ActivityEvent | None:
        """
        Return first activity event.
        """

        if not self.activity_events:
            return None

        return self.activity_events[0]

    @property
    def last_activity(self) -> ActivityEvent | None:
        """
        Return last activity event.
        """

        if not self.activity_events:
            return None

        return self.activity_events[-1]

    # ------------------------------------------------------------------
    # Timeline
    # ------------------------------------------------------------------

    @property
    def all_events(
        self,
    ) -> tuple[
        AttendanceEvent | DoneEvent | ActivityEvent,
        ...,
    ]:
        """
        Return every event in chronological order.
        """

        events = (
            list(self.attendance_events)
            + list(self.done_events)
            + list(self.activity_events)
        )

        return tuple(
            sorted(
                events,
                key=lambda event: event.timestamp,
            )
        )

    @property
    def start_time(self) -> datetime | None:
        """
        Return first event timestamp.
        """

        if not self.all_events:
            return None

        return self.all_events[0].timestamp

    @property
    def end_time(self) -> datetime | None:
        """
        Return last event timestamp.
        """

        if not self.all_events:
            return None

        return self.all_events[-1].timestamp

    @property
    def duration(self) -> timedelta:
        """
        Return session duration.
        """

        if self.start_time is None or self.end_time is None:
            return timedelta(0)

        return self.end_time - self.start_time

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    @property
    def has_attendance(self) -> bool:
        """
        Return True if attendance events exist.
        """
        return bool(self.attendance_events)

    @property
    def has_done_events(self) -> bool:
        """
        Return True if Done acknowledgement events exist.
        """
        return bool(self.done_events)

    @property
    def has_activities(self) -> bool:
        """
        Return True if activity events exist.
        """
        return bool(self.activity_events)

    @property
    def is_empty(self) -> bool:
        """
        Return True if the session contains no events.
        """
        return self.total_events == 0

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def attendee_exists(
        self,
        attendee: str,
    ) -> bool:
        """
        Return True if an attendee exists in the session.
        """

        normalized = attendee.casefold()

        return any(
            participant.casefold() == normalized
            for participant in self.unique_attendees
        )

    def done_exists(
        self,
        attendee: str,
    ) -> bool:
        """
        Return True if the attendee has at least one
        Done acknowledgement.
        """

        normalized = attendee.casefold()

        return any(
            event.attendee.casefold() == normalized for event in self.done_events
        )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, object]:
        """
        Return dictionary representation.
        """

        return {
            "session_date": self.session_date,
            "attendance_count": self.attendance_count,
            "present_count": self.present_count,
            "late_count": self.late_count,
            "absent_count": self.absent_count,
            "done_count": self.done_count,
            "activity_count": self.activity_count,
            "attendee_count": self.attendee_count,
            "attendance_types": self.attendance_types,
            "total_events": self.total_events,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": str(self.duration),
        }

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        """
        Return total number of events.
        """
        return self.total_events

    def __bool__(self) -> bool:
        """
        Return True if the session contains events.
        """
        return not self.is_empty

    def __str__(self) -> str:
        """
        Return readable representation.
        """

        return (
            "Session("
            f"date={self.session_date}, "
            f"participants={self.attendee_count}, "
            f"present={self.present_count}, "
            f"done={self.done_count}, "
            f"activities={self.activity_count})"
        )
