# src/presentation/components/charts.py

"""
Chart Components

Purpose
-------
Reusable Plotly chart components for the Presentation layer.

Responsibilities
----------------
- Render bar charts.
- Render line charts.
- Render pie charts.
- Display consistent empty chart states.

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
# Third-Party Imports
# ============================================================================
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================================
# Bar Chart
# ============================================================================


def render_bar_chart(
    dataframe: pd.DataFrame,
    *,
    x: str,
    y: str,
    title: str,
) -> None:
    """
    Render a responsive bar chart.
    """

    if dataframe.empty:
        render_empty_chart()
        return

    figure = px.bar(
        dataframe,
        x=x,
        y=y,
        title=title,
    )

    figure.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20,
        ),
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
    )


# ============================================================================
# Line Chart
# ============================================================================


def render_line_chart(
    dataframe: pd.DataFrame,
    *,
    x: str,
    y: str,
    title: str,
) -> None:
    """
    Render a responsive line chart.
    """

    if dataframe.empty:
        render_empty_chart()
        return

    figure = px.line(
        dataframe,
        x=x,
        y=y,
        title=title,
    )

    figure.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20,
        ),
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
    )


# ============================================================================
# Pie Chart
# ============================================================================


def render_pie_chart(
    dataframe: pd.DataFrame,
    *,
    names: str,
    values: str,
    title: str,
) -> None:
    """
    Render a responsive pie chart.
    """

    if dataframe.empty:
        render_empty_chart()
        return

    figure = px.pie(
        dataframe,
        names=names,
        values=values,
        title=title,
    )

    figure.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20,
        ),
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
    )


# ============================================================================
# Empty State
# ============================================================================


def render_empty_chart(
    message: str = "No chart data available.",
) -> None:
    """
    Display an empty chart placeholder.
    """

    st.info(message)
