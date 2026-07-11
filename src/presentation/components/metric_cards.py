# src/presentation/components/metric_cards.py

"""
Metric Card Components

Purpose
-------
Reusable Streamlit metric card components for displaying
key performance indicators (KPIs) throughout the application.

Responsibilities
----------------
- Render a single metric card.
- Render a row of metric cards.
- Provide a consistent metric appearance.
- Remain presentation-only.

Architectural Rules
-------------------
- No business logic.
- No analytics.
- No Session objects.
- No Application Services.
- No Infrastructure access.

Author
------
OYBS Attendance Dashboard

Created
-------
July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Sequence

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Type Aliases
# ============================================================================

MetricValue = int | float | str

Metric = tuple[
    str,  # Label
    MetricValue,  # Value
    str | None,  # Delta
    str | None,  # Help text
]


# ============================================================================
# Single Metric
# ============================================================================


def render_metric(
    *,
    label: str,
    value: MetricValue,
    delta: str | None = None,
    help_text: str | None = None,
) -> None:
    """
    Render a single Streamlit metric card.

    Parameters
    ----------
    label:
        Metric title.

    value:
        Metric value.

    delta:
        Optional delta displayed beneath the value.

    help_text:
        Optional tooltip.
    """

    st.metric(
        label=label,
        value=value,
        delta=delta,
        help=help_text,
    )


# ============================================================================
# Metric Row
# ============================================================================


def render_metric_row(
    metrics: Sequence[Metric],
) -> None:
    """
    Render multiple metrics in a responsive row.

    Parameters
    ----------
    metrics:
        Sequence of metric definitions.
    """

    if not metrics:
        st.info("No metrics available.")
        return

    columns = st.columns(len(metrics))

    for column, metric in zip(columns, metrics, strict=False):
        label, value, delta, help_text = metric

        with column:
            render_metric(
                label=label,
                value=value,
                delta=delta,
                help_text=help_text,
            )


# ============================================================================
# Section Header
# ============================================================================


def render_section_header(
    title: str,
    description: str | None = None,
) -> None:
    """
    Render a section heading above a metric group.

    Parameters
    ----------
    title:
        Section title.

    description:
        Optional descriptive text.
    """

    st.subheader(title)

    if description:
        st.caption(description)


# ============================================================================
# Empty State
# ============================================================================


def render_empty_metrics(
    message: str = "No metrics available.",
) -> None:
    """
    Display an empty metric state.

    Parameters
    ----------
    message:
        Message displayed to the user.
    """

    st.info(message)
