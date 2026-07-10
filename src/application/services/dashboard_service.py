# src/application/services/dashboard_service.py

"""
Dashboard Application Service

Purpose:
    Provides dashboard-ready application use cases by orchestrating
    attendance and activity services.

Responsibilities:
    - Build Session aggregates.
    - Coordinate attendance metrics.
    - Coordinate activity metrics.
    - Provide dashboard-ready data.
    - Remain free of business logic.

Rules:
    - No pandas.
    - No Streamlit.
    - No plotting.
    - No reporting.
    - No business rules.

Notes:
    - Delegates all business calculations to the Domain layer.
    - Delegates Session construction to the SessionBuilder.
    - Acts as the primary service consumed by the Presentation layer.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterable
from datetime import date

# ============================================================================
# Local Imports
# ============================================================================
from src.application.services.activity_service import ActivityService
from src.application.services.attendance_service import AttendanceService
from src.domain.models.message import Message
from src.domain.models.session import Session


class DashboardService:
    """
    Application service for dashboard workflows.
    """

    def __init__(
        self,
        attendance_service: AttendanceService | None = None,
        activity_service: ActivityService | None = None,
    ) -> None:
        """
        Initialize the DashboardService.
        """

        self._attendance_service = (
            attendance_service
            if attendance_service is not None
            else AttendanceService()
        )

        self._activity_service = (
            activity_service if activity_service is not None else ActivityService()
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
        Build a Session aggregate.

        The AttendanceService owns Session construction,
        ensuring there is a single orchestration path.
        """

        return self._attendance_service.build_session(
            session_date=session_date,
            messages=messages,
        )

    # ------------------------------------------------------------------
    # Dashboard Summary
    # ------------------------------------------------------------------

    def dashboard_summary(
        self,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, object]:
        """
        Return a dashboard-ready summary.
        """

        return {
            "session_date": session.session_date,
            "attendance_count": self._attendance_service.attendance_count(
                session,
            ),
            "attendance_rate": self._attendance_service.attendance_rate(
                session,
                expected_attendees,
            ),
            "done_count": self._attendance_service.done_count(
                session,
            ),
            "activity_count": self._activity_service.activity_count(
                session,
            ),
            "first_done": self._attendance_service.first_done(
                session,
            ),
            "first_activity": self._activity_service.first_activity(
                session,
            ),
            "last_activity": self._activity_service.last_activity(
                session,
            ),
        }

    # ------------------------------------------------------------------
    # Attendance
    # ------------------------------------------------------------------

    def attendance_summary(
        self,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, object]:
        """
        Return attendance metrics.
        """

        return {
            "attendees": self._attendance_service.attendees(
                session,
            ),
            "attendance_count": self._attendance_service.attendance_count(
                session,
            ),
            "attendance_rate": self._attendance_service.attendance_rate(
                session,
                expected_attendees,
            ),
            "attendance_types": self._attendance_service.attendance_counts(
                session,
            ),
        }

    # ------------------------------------------------------------------
    # Activity
    # ------------------------------------------------------------------

    def activity_summary(
        self,
        session: Session,
    ) -> dict[str, object]:
        """
        Return activity metrics.
        """

        return {
            "activity_count": self._activity_service.activity_count(
                session,
            ),
            "activity_types": self._activity_service.activity_counts(
                session,
            ),
            "first_activity": self._activity_service.first_activity(
                session,
            ),
            "last_activity": self._activity_service.last_activity(
                session,
            ),
        }

    # ------------------------------------------------------------------
    # Session Status
    # ------------------------------------------------------------------

    def session_summary(
        self,
        session: Session,
    ) -> dict[str, object]:
        """
        Return general session information.
        """

        return {
            "session_date": session.session_date,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "duration": session.duration,
            "attendance_events": session.attendance_count,
            "done_events": session.done_count,
            "activity_events": session.activity_count,
            "total_events": session.total_events,
        }

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

        return self._attendance_service.has_attendance(
            session,
        )

    def has_activities(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if activities exist.
        """

        return self._activity_service.has_activities(
            session,
        )

    def is_empty(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if the session contains no events.
        """

        return session.is_empty

    # ------------------------------------------------------------------
    # Service Accessors
    # ------------------------------------------------------------------

    @property
    def attendance_service(self) -> AttendanceService:
        """
        Return the AttendanceService instance.
        """

        return self._attendance_service

    @property
    def activity_service(self) -> ActivityService:
        """
        Return the ActivityService instance.
        """

        return self._activity_service

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"attendance_service="
            f"{self.attendance_service.__class__.__name__}, "
            f"activity_service="
            f"{self.activity_service.__class__.__name__})"
        )

    def __str__(self) -> str:
        """
        Return a human-readable representation.
        """

        return self.__repr__()
