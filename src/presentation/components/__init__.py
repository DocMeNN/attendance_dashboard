# src/presentation/components/__init__.py

"""
Presentation Components Package

Purpose
-------
Provides reusable Streamlit UI components.

Responsibilities
----------------
- Expose common presentation components.
- Provide a clean import surface for pages.

Rules
-----
- Presentation layer only.
- No business logic.
- No domain calculations.
"""

from __future__ import annotations

from .common import charts, metric_cards, tables

__all__ = [
    "charts",
    "metric_cards",
    "tables",
]
