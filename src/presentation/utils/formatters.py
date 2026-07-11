# src/presentation/utils/formatters.py

"""
Presentation Formatters

Purpose
-------
Provides reusable formatting helpers for the Presentation layer.

Responsibilities
----------------
- Convert application results into presentation-friendly structures.
- Convert collections into pandas DataFrames.
- Format metrics for reusable UI components.
- Keep presentation transformation logic out of Streamlit pages.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics.
- No Infrastructure access.
- No Streamlit dependencies.

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
from collections import Counter
from collections.abc import Mapping
from datetime import date, datetime, timedelta
from typing import Any

# ============================================================================
# Third-Party Imports
# ============================================================================
import pandas as pd

# ============================================================================
# Type Aliases
# ============================================================================

MetricValue = int | float | str

Metric = tuple[
    str,
    MetricValue,
    str | None,
    str | None,
]

# ============================================================================
# Metric Formatters
# ============================================================================


def metric(
    *,
    label: str,
    value: MetricValue,
    delta: str | None = None,
    help_text: str | None = None,
) -> Metric:
    """
    Create a metric definition compatible with
    presentation.metric_cards.render_metric_row().
    """

    return (
        label,
        value,
        delta,
        help_text,
    )


def metrics(
    *items: Metric,
) -> list[Metric]:
    """
    Build a metric collection.
    """

    return list(items)


# ============================================================================
# DataFrame Builders
# ============================================================================


def counter_to_dataframe(
    counter: Counter[Any],
    *,
    category_column: str = "Category",
    value_column: str = "Count",
) -> pd.DataFrame:
    """
    Convert a Counter into a DataFrame.
    """

    if not counter:
        return pd.DataFrame(
            columns=[
                category_column,
                value_column,
            ]
        )

    return pd.DataFrame(
        {
            category_column: [str(key) for key in counter.keys()],
            value_column: list(counter.values()),
        }
    )


def mapping_to_dataframe(
    mapping: Mapping[str, Any],
    *,
    key_column: str = "Property",
    value_column: str = "Value",
) -> pd.DataFrame:
    """
    Convert a mapping into a two-column DataFrame.
    """

    if not mapping:
        return pd.DataFrame(
            columns=[
                key_column,
                value_column,
            ]
        )

    return pd.DataFrame(
        {
            key_column: list(mapping.keys()),
            value_column: list(mapping.values()),
        }
    )


def records_to_dataframe(
    records: list[Mapping[str, Any]],
) -> pd.DataFrame:
    """
    Convert record dictionaries into a DataFrame.
    """

    if not records:
        return pd.DataFrame()

    return pd.DataFrame(records)


# ============================================================================
# Value Formatters
# ============================================================================


def percentage(
    value: float,
    *,
    decimals: int = 1,
) -> str:
    """
    Format a percentage value.
    """

    return f"{value:.{decimals}f}%"


def duration(
    value: timedelta,
) -> str:
    """
    Format a timedelta for display.
    """

    return str(value)


def date_value(
    value: date | None,
) -> str:
    """
    Format a date.
    """

    if value is None:
        return "-"

    return value.isoformat()


def datetime_value(
    value: datetime | None,
) -> str:
    """
    Format a datetime.
    """

    if value is None:
        return "-"

    return value.strftime(
        "%Y-%m-%d %H:%M:%S",
    )


# ============================================================================
# Session Formatters
# ============================================================================


def session_summary(
    session: Any,
) -> pd.DataFrame:
    """
    Convert a Session aggregate into a summary DataFrame.
    """

    return mapping_to_dataframe(
        {
            "Session Date": date_value(session.session_date),
            "Start Time": datetime_value(session.start_time),
            "End Time": datetime_value(session.end_time),
            "Duration": duration(session.duration),
            "Unique Attendees": session.attendee_count,
            "Attendance Events": session.attendance_count,
            "Done Events": session.done_count,
            "Activity Events": session.activity_count,
            "Total Events": session.total_events,
        }
    )


# ============================================================================
# Dashboard Metric Formatters
# ============================================================================


def dashboard_metrics(
    summary: Mapping[str, Any],
) -> list[Metric]:
    """
    Build dashboard metric cards.
    """

    return metrics(
        metric(
            label="Attendance",
            value=summary["attendance_count"],
            help_text="Unique attendees",
        ),
        metric(
            label="Attendance %",
            value=percentage(summary["attendance_rate"]),
            help_text="Attendance rate",
        ),
        metric(
            label="Done",
            value=summary["done_count"],
            help_text="Done acknowledgements",
        ),
        metric(
            label="Activities",
            value=summary["activity_count"],
            help_text="Activity events",
        ),
    )


# ============================================================================
# Event Record Builders
# ============================================================================


def highlight_records(
    *,
    session: Any,
    summary: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """
    Build session highlight records.
    """

    first_done = summary.get("first_done")
    first_activity = summary.get("first_activity")
    last_activity = summary.get("last_activity")

    return [
        {
            "Item": "First Attendee",
            "Value": session.first_attendee or "-",
        },
        {
            "Item": "First Done",
            "Value": (
                getattr(first_done, "attendee", "-") if first_done is not None else "-"
            ),
        },
        {
            "Item": "First Activity",
            "Value": (
                getattr(first_activity, "attendee", "-")
                if first_activity is not None
                else "-"
            ),
        },
        {
            "Item": "Last Activity",
            "Value": (
                getattr(last_activity, "attendee", "-")
                if last_activity is not None
                else "-"
            ),
        },
    ]


# ============================================================================
# Generic Helpers
# ============================================================================


def empty_dataframe(
    columns: list[str] | tuple[str, ...] | None = None,
) -> pd.DataFrame:
    """
    Return an empty DataFrame.

    Parameters
    ----------
    columns:
        Optional column names.
    """

    return pd.DataFrame(
        columns=list(columns) if columns else None,
    )


def safe_text(
    value: Any,
    *,
    placeholder: str = "-",
) -> str:
    """
    Convert a value into displayable text.

    None values are replaced with a placeholder.
    """

    if value is None:
        return placeholder

    return str(value)


def safe_records(
    records: list[Mapping[str, Any]] | None,
) -> list[Mapping[str, Any]]:
    """
    Return a safe list of records.
    """

    return records if records is not None else []


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "Metric",
    "MetricValue",
    "metric",
    "metrics",
    "counter_to_dataframe",
    "mapping_to_dataframe",
    "records_to_dataframe",
    "percentage",
    "duration",
    "date_value",
    "datetime_value",
    "session_summary",
    "dashboard_metrics",
    "highlight_records",
    "empty_dataframe",
    "safe_text",
    "safe_records",
]
