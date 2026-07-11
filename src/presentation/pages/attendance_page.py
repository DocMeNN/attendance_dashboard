# src/presentation/pages/attendance_page.py

"""
Attendance Page

Purpose
-------
Displays attendance information for the active session.

Responsibilities
----------------
- Render attendance page UI.
- Prepare future attendance visualizations.

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
    Render the Attendance page.
    """

    st.title("👥 Attendance")

    st.info(
        "Attendance analytics page.\n\n"
        "Attendance metrics and attendee details will be displayed here."
    )
