# src/presentation/components/common/__init__.py

"""
Common Presentation Components Package

Purpose
-------
Provides reusable Streamlit presentation components.

Responsibilities
----------------
- Expose reusable UI components.
- Provide a clean import surface for presentation pages.

Components
-----------
- charts
- metric_cards
- tables

Rules
-----
- Presentation layer only.
- No business logic.
- No analytics calculations.
- No domain dependencies.
"""

from __future__ import annotations

from . import charts, metric_cards, tables

__all__ = [
    "charts",
    "metric_cards",
    "tables",
]
