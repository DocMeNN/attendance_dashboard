# src/presentation/components/tables.py

"""
Table Components

Purpose
-------
Reusable Streamlit table components.

Responsibilities
----------------
- Render DataFrames.
- Render tabular records.
- Display consistent empty states.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics.
- No Application Services.
- No Domain dependencies.

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
from collections.abc import Mapping, Sequence
from typing import Any

# ============================================================================
# Third-Party Imports
# ============================================================================
import pandas as pd
import streamlit as st

# ============================================================================
# DataFrame
# ============================================================================


def render_dataframe(
    dataframe: pd.DataFrame,
    *,
    use_container_width: bool = True,
    hide_index: bool = True,
) -> None:
    """
    Render a pandas DataFrame.
    """

    if dataframe.empty:
        render_empty_table()
        return

    st.dataframe(
        dataframe,
        use_container_width=use_container_width,
        hide_index=hide_index,
    )


# ============================================================================
# Records
# ============================================================================


def render_table(
    records: Sequence[Mapping[str, Any]],
) -> None:
    """
    Render tabular records.

    Parameters
    ----------
    records:
        Sequence of dictionaries.
    """

    if not records:
        render_empty_table()
        return

    dataframe = pd.DataFrame(records)

    render_dataframe(dataframe)


# ============================================================================
# Empty State
# ============================================================================


def render_empty_table(
    message: str = "No data available.",
) -> None:
    """
    Display an empty table message.
    """

    st.info(message)
