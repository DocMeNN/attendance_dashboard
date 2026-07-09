# src/domain/analytics/__init__.py

"""
Domain Analytics Package.

Purpose
-------
Contains pure business logic used throughout the Attendance Dashboard.

The analytics layer is responsible for computing business metrics and
statistics from immutable domain models. It is completely independent of
the infrastructure, application, and presentation layers.

Modules
-------
attendance
    Attendance-related business calculations.

sessions
    Session-level business calculations.

leaderboards
    Member ranking and leaderboard calculations.

statistics
    Aggregate statistics across multiple sessions.

comparisons
    Comparative analytics between sessions and reporting periods.
"""

from . import attendance
from . import comparisons
from . import leaderboards
from . import sessions
from . import statistics

__all__ = [
    "attendance",
    "comparisons",
    "leaderboards",
    "sessions",
    "statistics",
]
