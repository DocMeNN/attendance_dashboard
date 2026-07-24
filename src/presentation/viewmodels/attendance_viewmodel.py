# src/presentation/viewmodels/attendance_viewmodel.py

"""
Attendance ViewModel

Purpose
-------
Coordinates attendance presentation workflows by consuming the
Application Layer AttendanceService and adapting AttendanceResult
for Presentation Layer consumption.

Responsibilities
----------------
- Delegate attendance workflows to AttendanceService.
- Consume the typed AttendanceResult application contract.
- Expose presentation-friendly attendance data.
- Adapt application results for existing presentation components.

Architectural Rules
-------------------
- Presentation layer only.
- No business logic.
- No analytics calculations.
- No Streamlit.
- No direct Domain analytics.
- No infrastructure dependencies.
- No direct data parsing.

Architecture
------------
Attendance Page
        |
        v
AttendanceViewModel
        |
        v
AttendanceService
        |
        v
AttendanceResult
        |
        v
Presentation Components

The ViewModel is an adapter between the Application Layer
contract and Presentation Layer consumption.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterable
from datetime import date
from typing import Any

# ============================================================================
# Local Imports
# ============================================================================
from src.application.dto.attendance_result import AttendanceResult
from src.application.services.attendance_service import AttendanceService
from src.domain.models.message import Message
from src.domain.models.session import Session

# ============================================================================
# Attendance ViewModel
# ============================================================================


class AttendanceViewModel:
    """
    Presentation ViewModel for attendance workflows.

    Coordinates the AttendanceService and adapts the resulting
    AttendanceResult for Presentation Layer consumption.

    The ViewModel does not calculate attendance. All attendance
    calculations remain in the Application and Domain layers.
    """

    def __init__(
        self,
        attendance_service: AttendanceService | None = None,
    ) -> None:
        """
        Initialize the AttendanceViewModel.

        Parameters
        ----------
        attendance_service:
            Optional AttendanceService dependency.

            When omitted, a default AttendanceService is created.
        """

        self._attendance_service = (
            attendance_service
            if attendance_service is not None
            else AttendanceService()
        )

    # =========================================================================
    # Session Construction
    # =========================================================================

    def build_session(
        self,
        *,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build a Session through the Application Layer.

        Session construction remains delegated to the
        AttendanceService.
        """

        return self._attendance_service.build_session(
            session_date=session_date,
            messages=messages,
        )

    # =========================================================================
    # Attendance Result
    # =========================================================================

    def get_attendance(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> AttendanceResult:
        """
        Return the typed application attendance result.

        The ViewModel delegates attendance result construction
        to the AttendanceService.
        """

        return self._attendance_service.attendance_result(
            session=session,
            expected_attendees=expected_attendees,
        )

    # =========================================================================
    # Presentation Adapter
    # =========================================================================

    def to_presentation_data(
        self,
        result: AttendanceResult,
    ) -> dict[str, Any]:
        """
        Adapt AttendanceResult for Presentation components.

        This method performs structural presentation adaptation only.

        It does not:
            - calculate attendance;
            - calculate analytics;
            - apply business rules;
            - modify the application result.

        The returned dictionary exists to support Presentation
        components that currently consume mapping-based data.
        """

        return {
            "attendees": result.attendees,
            "participants": result.participants,
            "attendance_count": result.attendance_count,
            "attendance_rate": result.attendance_rate,
            "attendance_types": result.attendance_types,
            "attendance_events": result.attendance_events,
            "done_events": result.done_events,
            "done_count": result.done_count,
            "first_done": result.first_done,
        }

    # =========================================================================
    # Presentation Workflow
    # =========================================================================

    def attendance_data(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
        """
        Return presentation-ready attendance data.

        This is the primary convenience method for pages that
        currently consume mapping-based attendance data.

        The workflow is:

            Session
                |
                v
            AttendanceService
                |
                v
            AttendanceResult
                |
                v
            Presentation Mapping
        """

        result = self.get_attendance(
            session=session,
            expected_attendees=expected_attendees,
        )

        return self.to_presentation_data(
            result,
        )

    # =========================================================================
    # Service Access
    # =========================================================================

    @property
    def attendance_service(self) -> AttendanceService:
        """
        Return the underlying AttendanceService.
        """

        return self._attendance_service

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"attendance_service="
            f"{self.attendance_service.__class__.__name__})"
        )

    def __str__(self) -> str:
        """
        Return a readable representation.
        """

        return self.__repr__()


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "AttendanceViewModel",
]
