# src/presentation/components/filters.py

"""
Filter Components

Purpose
-------
Reusable filter widgets for the Presentation layer.

Responsibilities
----------------
- Render reusable input controls.
- Collect user selections.
- Return selected values.
- Remain presentation-only.

Architectural Rules
-------------------
- No business logic.
- No analytics.
- No Application Services.
- No Domain dependencies.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Sequence
from datetime import date

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Select Box
# ============================================================================


def render_selectbox(
    *,
    label: str,
    options: Sequence[str],
    index: int = 0,
    help_text: str | None = None,
) -> str:
    """
    Render a reusable select box.
    """

    return st.selectbox(
        label,
        options,
        index=index,
        help=help_text,
    )


# ============================================================================
# Date Input
# ============================================================================


def render_date_input(
    *,
    label: str,
    value: date | None = None,
) -> date | None:
    """
    Render a date picker.

    Returns
    -------
    date | None
        The selected date, or None when no date has been chosen.
    """

    return st.date_input(
        label,
        value=value,
    )


# ============================================================================
# Number Input
# ============================================================================


def render_number_input(
    *,
    label: str,
    value: int = 0,
    minimum: int = 0,
    maximum: int = 1000,
) -> int:
    """
    Render an integer number input.
    """

    return st.number_input(
        label,
        min_value=minimum,
        max_value=maximum,
        value=value,
        step=1,
    )


# ============================================================================
# Checkbox
# ============================================================================


def render_checkbox(
    *,
    label: str,
    value: bool = False,
) -> bool:
    """
    Render a checkbox.
    """

    return st.checkbox(
        label,
        value=value,
    )


# ============================================================================
# Divider
# ============================================================================


def render_divider() -> None:
    """
    Render a visual divider.
    """

    st.divider()


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "render_selectbox",
    "render_date_input",
    "render_number_input",
    "render_checkbox",
    "render_divider",
]
