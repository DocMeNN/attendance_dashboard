# src/domain/models/__init__.py

"""
Domain Models Package

Purpose
-------
Provides the canonical domain model objects used throughout
the OYBS Attendance Dashboard.

Responsibilities
----------------
- Expose domain model classes through a stable package interface.
- Provide a single import location for domain models.
- Keep model organization explicit and discoverable.

Architectural Rules
-------------------
- Domain layer only.
- No UI dependencies.
- No pandas dependencies.
- No infrastructure dependencies.
- Models must remain technology independent.
"""

from __future__ import annotations

# ============================================================================
# Domain Model Imports
# ============================================================================
from .activity_event import ActivityEvent
from .attendance_event import AttendanceEvent
from .attendance_summary import AttendanceSummary
from .dashboard_metrics import DashboardMetrics
from .done_event import DoneEvent
from .insight_event import InsightEvent
from .member import Member
from .message import Message
from .report import Report
from .scripture_event import ScriptureEvent
from .session import Session

# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "ActivityEvent",
    "AttendanceEvent",
    "AttendanceSummary",
    "DashboardMetrics",
    "DoneEvent",
    "InsightEvent",
    "Member",
    "Message",
    "Report",
    "ScriptureEvent",
    "Session",
]
