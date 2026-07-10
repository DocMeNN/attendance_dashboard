# src/application/services/report_service.py

"""
Report Application Service

Purpose:
    Provides report-ready application use cases by orchestrating
    attendance, activity and dashboard services.

Responsibilities:
    - Build Session aggregates.
    - Coordinate report data.
    - Aggregate attendance metrics.
    - Aggregate activity metrics.
    - Prepare report-ready structures.
    - Remain free of business logic.

Rules:
    - No pandas.
    - No Streamlit.
    - No plotting.
    - No PDF generation.
    - No Excel generation.
    - No file I/O.
    - No business rules.

Notes:
    - Business calculations remain inside the Domain.
    - Report rendering belongs to the Presentation layer.
    - This service prepares data only.

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
from src.application.services.dashboard_service import DashboardService
from src.domain.models.message import Message
from src.domain.models.session import Session


class ReportService:
    """
    Application service responsible for preparing
    report-ready data.
    """

    def __init__(
        self,
        attendance_service: AttendanceService | None = None,
        activity_service: ActivityService | None = None,
        dashboard_service: DashboardService | None = None,
    ) -> None:
        """
        Initialize the ReportService.
        """

        self._attendance_service = (
            attendance_service
            if attendance_service is not None
            else AttendanceService()
        )

        self._activity_service = (
            activity_service if activity_service is not None else ActivityService()
        )

        self._dashboard_service = (
            dashboard_service
            if dashboard_service is not None
            else DashboardService(
                attendance_service=self._attendance_service,
                activity_service=self._activity_service,
            )
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

        return self._attendance_service.build_session(
            session_date=session_date,
            messages=messages,
        )

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def report_data(
        self,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, object]:
        """
        Return complete report-ready data.
        """

        return {
            "session": self._dashboard_service.session_summary(
                session,
            ),
            "dashboard": self._dashboard_service.dashboard_summary(
                session,
                expected_attendees,
            ),
            "attendance": self._dashboard_service.attendance_summary(
                session,
                expected_attendees,
            ),
            "activity": self._dashboard_service.activity_summary(
                session,
            ),
        }

    # ------------------------------------------------------------------
    # Individual Sections
    # ------------------------------------------------------------------

    def attendance_section(
        self,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, object]:
        """
        Return attendance section.
        """

        return self._dashboard_service.attendance_summary(
            session,
            expected_attendees,
        )

    def activity_section(
        self,
        session: Session,
    ) -> dict[str, object]:
        """
        Return activity section.
        """

        return self._dashboard_service.activity_summary(
            session,
        )

    def dashboard_section(
        self,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, object]:
        """
        Return dashboard section.
        """

        return self._dashboard_service.dashboard_summary(
            session,
            expected_attendees,
        )

    # ------------------------------------------------------------------
    # Session Section
    # ------------------------------------------------------------------

    def session_section(
        self,
        session: Session,
    ) -> dict[str, object]:
        """
        Return general session information.
        """

        return self._dashboard_service.session_summary(
            session,
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

    @property
    def dashboard_service(self) -> DashboardService:
        """
        Return the DashboardService instance.
        """

        return self._dashboard_service

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
            f"{self.activity_service.__class__.__name__}, "
            f"dashboard_service="
            f"{self.dashboard_service.__class__.__name__})"
        )

    def __str__(self) -> str:
        """
        Return a human-readable representation.
        """

        return self.__repr__()
