# src/application/services/attendance_service.py

"""
Attendance Application Service

Purpose:
    Provides application-level attendance use cases by orchestrating
    Session construction and Domain attendance analytics.

Responsibilities:
    - Build Session aggregates.
    - Expose attendance-related application workflows.
    - Coordinate attendance analytics.
    - Coordinate Done acknowledgement analytics.
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
    - Attendance is based on WhatsApp participants only.
    - Missing members cannot be calculated because no member registry exists.

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

    Coordinates Session creation and delegates all
    attendance calculations to Domain analytics.
    """

    def __init__(
        self,
        session_builder: SessionBuilder | None = None,
    ) -> None:
        """
        Initialize attendance service.
        """

        self._session_builder = (
            session_builder if session_builder is not None else SessionBuilder()
        )

    # ------------------------------------------------------------------
    # Session Construction
    # ------------------------------------------------------------------

    def build_session(
        self,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build immutable Session aggregate.
        """

        return self._session_builder.build(
            session_date=session_date,
            messages=messages,
        )

    # ------------------------------------------------------------------
    # Attendance Events
    # ------------------------------------------------------------------

    def attendance_events(
        self,
        session: Session,
    ) -> tuple[AttendanceEvent, ...]:
        """
        Return attendance events from session.
        """

        return session.attendance_events

    def attendees(
        self,
        session: Session,
    ) -> tuple[str, ...]:
        """
        Return unique WhatsApp participants who attended.
        """

        return get_attendees(
            session.attendance_events,
        )

    def attendance_count(
        self,
        session: Session,
    ) -> int:
        """
        Return unique participant attendance count.
        """

        return len(
            self.attendees(session),
        )

    def attendance_rate(
        self,
        session: Session,
        expected_attendees: int,
    ) -> float:
        """
        Calculate attendance percentage.

        Note:
            Expected attendees must come from an external
            known participant count. WhatsApp export alone
            cannot determine silent members.
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
        Calculate attendance rate for a known participant.
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
        Return Done acknowledgement events.
        """

        return session.done_events

    def done_count(
        self,
        session: Session,
    ) -> int:
        """
        Return total Done acknowledgement count.
        """

        return count_done_events(
            session.done_events,
        )

    def first_done(
        self,
        session: Session,
    ) -> DoneEvent | None:
        """
        Return first Done acknowledgement event.
        """

        return first_done_event(
            session.done_events,
        )

    # ------------------------------------------------------------------
    # Participant Information
    # ------------------------------------------------------------------

    def participant_count(
        self,
        session: Session,
    ) -> int:
        """
        Return number of unique WhatsApp participants.

        This represents observed participants only.
        No missing-member calculation is performed.
        """

        return len(
            session.unique_attendees,
        )

    def participants(
        self,
        session: Session,
    ) -> tuple[str, ...]:
        """
        Return observed WhatsApp participants.
        """

        return session.unique_attendees

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

        return session.has_done_events

    def is_empty(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if session contains no events.
        """

        return session.is_empty

    # ------------------------------------------------------------------
    # Builder Access
    # ------------------------------------------------------------------

    @property
    def builder(self) -> SessionBuilder:
        """
        Return the SessionBuilder.
        """

        return self._session_builder

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Return official representation.
        """

        return f"{self.__class__.__name__}" f"(builder={self.builder.name})"

    def __str__(self) -> str:
        """
        Return readable representation.
        """

        return self.__repr__()
