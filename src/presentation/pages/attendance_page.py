# src/presentation/pages/attendance_page.py

"""
Attendance Page

Purpose
-------
Displays attendance analytics for the active ministry session.

Responsibilities
----------------
- Coordinate attendance presentation components.
- Display attendance session summary.
- Display attendance page footer.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics calculations.
"""

from __future__ import annotations

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation import context
from src.presentation.components.attendance import (
    distribution,
    overview,
)
from src.presentation.components.common import (
    metric_cards,
    tables,
)
from src.presentation.utils import formatters

# ============================================================================
# Attendance Page
# ============================================================================


def render() -> None:
    """
    Render the Attendance page.
    """

    context.initialize()

    st.title("👥 Attendance")

    if not context.has_session():
        st.info(
            "No session loaded.\n\n"
            "Please load a WhatsApp session from the Home page."
        )
        return

    session = context.current_session()

    if session is None:
        st.error(
            "Unable to retrieve the active session.",
        )
        return

    dashboard = context.dashboard_service()

    attendance = dashboard.attendance_summary(
        session,
        context.expected_attendees(),
    )

    # =====================================================================
    # Attendance Overview
    # =====================================================================

    overview.render(
        attendance,
    )

    st.divider()

    # =====================================================================
    # Attendance Distribution
    # =====================================================================

    distribution.render(
        attendance,
    )

    st.divider()

    # =====================================================================
    # Session Summary
    # =====================================================================

    metric_cards.render_section_header(
        "Session Attendance",
        "Attendance information for this meeting.",
    )

    tables.render_dataframe(
        formatters.session_summary(
            session,
        )
    )

    st.divider()

    # =====================================================================
    # Footer
    # =====================================================================

    left_column, right_column = st.columns([3, 1])

    with left_column:
        st.caption(
            (
                f"Session Date: {session.session_date} | "
                f"Expected: {context.expected_attendees()} | "
                f"Present: {session.attendee_count}"
            )
        )

    with right_column:
        if st.button(
            "🔄 Refresh",
            use_container_width=True,
        ):
            st.rerun()
