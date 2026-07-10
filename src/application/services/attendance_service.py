# src/application/services/attendance_service.py

"""
Attendance Application Service

Purpose:
    Provides application-level attendance use cases by orchestrating
    the SessionBuilder and Domain analytics.

Responsibilities:
    - Build Session aggregates.
    - Coordinate attendance analytics.
    - Coordinate Done analytics.
    - Expose attendance-related application services.
    - Remain free of business logic.

Rules:
    - No pandas.
    - No Streamlit.
    - No plotting.
    - No reporting.
    - No infrastructure parsing.
    - No business rules.

Notes:
    - Business rules remain inside the Domain layer.
    - This service coordinates Domain components only.
    - Technology independent.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections import Counter
from collections.abc import Iterable
from datetime import date

# ============================================================================
# Local Imports
# ============================================================================
from src.application.builders.session_builder import SessionBuilder
from src.domain.analytics.attendance import (
    calculate_attendance_rate,
    calculate_member_attendance_rate,
    count_attendance_types,
    get_attendees,
)
from src.domain.analytics.done import (
    count_done_events,
    first_done_event,
)
from src.domain.enums.attendance_type import AttendanceType
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.done_event import DoneEvent
from src.domain.models.member import Member
from src.domain.models.message import Message
from src.domain.models.session import Session


class AttendanceService:
    """
    Application service for attendance workflows.

    The service coordinates Session construction and
    delegates business calculations to the Domain layer.
    """

    def __init__(
        self,
        session_builder: SessionBuilder | None = None,
    ) -> None:
        """
        Initialize the service.
        """

        self._session_builder = (
            session_builder if session_builder is not None else SessionBuilder()
        )

    # ------------------------------------------------------------------
    # Session
    # ------------------------------------------------------------------

    def build_session(
        self,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build an immutable Session aggregate.
        """

        return self._session_builder.build(
            session_date=session_date,
            messages=messages,
        )

    # ------------------------------------------------------------------
    # Attendance
    # ------------------------------------------------------------------

    def attendance_events(
        self,
        session: Session,
    ) -> tuple[AttendanceEvent, ...]:
        """
        Return attendance events.
        """

        return session.attendance_events

    def attendees(
        self,
        session: Session,
    ) -> tuple[str, ...]:
        """
        Return unique attendees.
        """

        return get_attendees(
            session.attendance_events,
        )

    def attendance_count(
        self,
        session: Session,
    ) -> int:
        """
        Return unique attendee count.
        """

        return len(self.attendees(session))

    def attendance_rate(
        self,
        session: Session,
        expected_attendees: int,
    ) -> float:
        """
        Calculate attendance percentage.
        """

        return calculate_attendance_rate(
            session.attendance_events,
            expected_attendees,
        )

    def member_attendance_rate(
        self,
        member: Member,
        session: Session,
    ) -> float:
        """
        Calculate attendance rate for a member.
        """

        return calculate_member_attendance_rate(
            member,
            session.attendance_events,
        )

    def attendance_counts(
        self,
        session: Session,
    ) -> Counter[AttendanceType]:
        """
        Count attendance classifications.
        """

        return count_attendance_types(
            session.attendance_events,
        )

    # ------------------------------------------------------------------
    # Done Events
    # ------------------------------------------------------------------

    def done_events(
        self,
        session: Session,
    ) -> tuple[DoneEvent, ...]:
        """
        Return all Done events for the session.
        """

        return session.done_events

    def done_count(
        self,
        session: Session,
    ) -> int:
        """
        Return the number of Done events.

        Every valid Done acknowledgement is counted.
        Duplicate handling is delegated to the Domain
        analytics layer.
        """

        return count_done_events(
            session.done_events,
        )

    def first_done(
        self,
        session: Session,
    ) -> DoneEvent | None:
        """
        Return the first Done event recorded for the
        session.
        """

        return first_done_event(
            session.done_events,
        )

    # ------------------------------------------------------------------
    # Convenience Methods
    # ------------------------------------------------------------------

    def has_attendance(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if attendance exists.
        """

        return session.has_attendance

    def has_done_events(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if Done events exist.
        """

        return bool(session.done_events)

    def is_empty(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if the session contains no attendance
        activity.
        """

        return session.is_empty

    # ------------------------------------------------------------------
    # Builder
    # ------------------------------------------------------------------

    @property
    def builder(self) -> SessionBuilder:
        """
        Return the SessionBuilder used by the service.
        """

        return self._session_builder

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return f"{self.__class__.__name__}" f"(builder={self.builder.name})"

    def __str__(self) -> str:
        """
        Return a human-readable representation.
        """

        return self.__repr__()
