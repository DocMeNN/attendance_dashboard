# src/domain/analytics/__init__.py

"""
Domain Analytics Package

Purpose
-------
Provides pure domain-level analytical functions for the
OYBS Attendance Dashboard.

Responsibilities
----------------
- Attendance analytics.
- Activity analytics.
- Comparison analytics.
- Done acknowledgement analytics.
- Insight analytics.
- Leaderboard analytics.
- Scripture analytics.
- Session analytics.
- Statistical analytics.

Notes
-----
- Technology independent.
- No UI dependencies.
- No pandas dependencies.
- No infrastructure dependencies.
"""

from __future__ import annotations

from . import (
    activity,
    attendance,
    comparisons,
    done,
    insight,
    leaderboards,
    scripture,
    sessions,
    statistics,
)

__all__ = [
    "activity",
    "attendance",
    "comparisons",
    "done",
    "insight",
    "leaderboards",
    "scripture",
    "sessions",
    "statistics",
]
