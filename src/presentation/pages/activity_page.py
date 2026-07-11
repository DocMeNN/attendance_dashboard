# src/presentation/pages/activity_page.py

"""
Activity Page

Purpose
-------
Displays activity information for the active session.

Responsibilities
----------------
- Render activity page UI.
- Prepare future activity visualizations.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics calculations.
"""

from __future__ import annotations

import streamlit as st


def render() -> None:
    """
    Render the Activity page.
    """

    st.title("📈 Activity")

    st.info(
        "Activity analytics page.\n\n"
        "Activity metrics and engagement insights will be displayed here."
    )
