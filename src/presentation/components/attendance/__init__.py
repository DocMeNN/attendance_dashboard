"""
Attendance Presentation Components

Purpose
-------
Provides reusable presentation components for the Attendance Analytics
workspace.

Responsibilities
----------------
- Organize attendance-specific presentation components.
- Expose a clean package API.
- Keep attendance rendering logic out of page modules.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics calculations.
"""

from __future__ import annotations

from . import distribution, overview

__all__ = [
    "distribution",
    "overview",
]
