# src/presentation/viewmodels/dashboard_viewmodel.py

"""
Dashboard ViewModel

Purpose
-------
Coordinates dashboard presentation workflows by consuming the
Application Layer DashboardService and adapting dashboard data
for Presentation Layer consumption.

Responsibilities
----------------
- Delegate dashboard workflows to DashboardService.
- Build Session aggregates through the Application Layer.
- Expose presentation-ready dashboard data.
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
Dashboard Page
        |
        v
DashboardViewModel
        |
        v
DashboardService
        |
        v
AttendanceService + ActivityService
        |
        v
Presentation Components

The ViewModel is an adapter between the Application Layer
and the Presentation Layer.
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
from src.application.services.dashboard_service import DashboardService
from src.domain.models.message import Message
from src.domain.models.session import Session

# ============================================================================
# Dashboard ViewModel
# ============================================================================


class DashboardViewModel:
    """
    Presentation ViewModel for dashboard workflows.

    Coordinates the DashboardService and adapts dashboard
    application data for Presentation Layer consumption.

    The ViewModel does not calculate dashboard analytics.
    All calculations remain delegated to the Application
    and Domain layers.
    """

    def __init__(
        self,
        dashboard_service: DashboardService | None = None,
    ) -> None:
        """
        Initialize the DashboardViewModel.

        Parameters
        ----------
        dashboard_service:
            Optional DashboardService dependency.

            When omitted, a default DashboardService is created.
        """

        self._dashboard_service = (
            dashboard_service
            if dashboard_service is not None
            else DashboardService()
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

        Session construction remains delegated to
        DashboardService.
        """

        return self._dashboard_service.build_session(
            session_date=session_date,
            messages=messages,
        )

    # =========================================================================
    # Dashboard Data
    # =========================================================================

    def get_dashboard(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
        """
        Return complete dashboard data.

        Dashboard calculations are delegated to
        DashboardService.
        """

        return self.to_presentation_data(
            session=session,
            expected_attendees=expected_attendees,
        )

    def to_presentation_data(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
        """
        Adapt dashboard application results for Presentation components.

        This method performs structural presentation adaptation only.

        It does not:
            - calculate analytics;
            - apply business rules;
            - parse messages;
            - modify the Session aggregate.
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

    # =========================================================================
    # Individual Sections
    # =========================================================================

    def session_summary(
        self,
        *,
        session: Session,
    ) -> dict[str, Any]:
        """
        Return presentation-ready session summary data.
        """

        return self._dashboard_service.session_summary(
            session,
        )

    def dashboard_summary(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
        """
        Return presentation-ready dashboard summary data.
        """

        return self._dashboard_service.dashboard_summary(
            session,
            expected_attendees,
        )

    def attendance_summary(
        self,
        *,
        session: Session,
        expected_attendees: int,
    ) -> dict[str, Any]:
        """
        Return presentation-ready attendance summary data.
        """

        return self._dashboard_service.attendance_summary(
            session,
            expected_attendees,
        )

    def activity_summary(
        self,
        *,
        session: Session,
    ) -> dict[str, Any]:
        """
        Return presentation-ready activity summary data.
        """

        return self._dashboard_service.activity_summary(
            session,
        )

    # =========================================================================
    # State
    # =========================================================================

    def has_attendance(
        self,
        *,
        session: Session,
    ) -> bool:
        """
        Return True when attendance exists.
        """

        return self._dashboard_service.has_attendance(
            session,
        )

    def has_activities(
        self,
        *,
        session: Session,
    ) -> bool:
        """
        Return True when activities exist.
        """

        return self._dashboard_service.has_activities(
            session,
        )

    def is_empty(
        self,
        *,
        session: Session,
    ) -> bool:
        """
        Return True when the Session contains no events.
        """

        return self._dashboard_service.is_empty(
            session,
        )

    # =========================================================================
    # Service Access
    # =========================================================================

    @property
    def dashboard_service(self) -> DashboardService:
        """
        Return the underlying DashboardService.
        """

        return self._dashboard_service

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"dashboard_service="
            f"{self.dashboard_service.__class__.__name__})"
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
    "DashboardViewModel",
]
