# src/presentation/pages/reports_page.py

"""
Reports Page

Purpose
-------
Displays reporting and AI executive reporting for the active session.

Responsibilities
----------------
- Display report metrics.
- Display session summary.
- Display AI executive report generation.
- Display export roadmap.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics.
- No report generation.
"""

from __future__ import annotations

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

from src.presentation import context
from src.presentation.components.ai import ministry_ai_panel

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation.components.common import (
    metric_cards,
    tables,
)
from src.presentation.utils import formatters
from src.presentation.viewmodels.ai_viewmodel import AIViewModel

# ============================================================================
# Reports Page
# ============================================================================


def render() -> None:
    """
    Render the Reports page.
    """

    context.initialize()

    st.title("📄 Reports")

    if not context.has_session():
        st.info(
            "Load a session before generating reports.",
        )
        return

    session = context.current_session()

    if session is None:
        st.error(
            "Unable to retrieve the active session.",
        )
        return

    dashboard = context.dashboard_service()

    expected = context.expected_attendees()

    summary = dashboard.dashboard_summary(
        session,
        expected,
    )

    attendance = dashboard.attendance_summary(
        session,
        expected,
    )

    activity = dashboard.activity_summary(
        session,
    )

    # =====================================================================
    # Report Overview
    # =====================================================================

    metric_cards.render_section_header(
        "Report Overview",
        "Summary statistics included in this report.",
    )

    metric_cards.render_metric_row(
        formatters.dashboard_metrics(
            summary,
        ),
    )

    st.divider()

    # =====================================================================
    # Session Summary
    # =====================================================================

    metric_cards.render_section_header(
        "Session Summary",
        "General information for the current meeting.",
    )

    tables.render_dataframe(
        formatters.session_summary(
            session,
        )
    )

    st.divider()

    # =====================================================================
    # Session Highlights
    # =====================================================================

    metric_cards.render_section_header(
        "Session Highlights",
        "Important milestones from this meeting.",
    )

    tables.render_table(
        formatters.highlight_records(
            session=session,
            summary=summary,
        )
    )

    st.divider()

    # =====================================================================
    # AI Executive Summary
    # =====================================================================

    viewmodel = AIViewModel(
        controller=context.ai_controller(),
    )

    report = viewmodel.build_executive_report(
        session=session,
        dashboard_summary=summary,
        attendance=attendance,
        activity=activity,
    )

    metric_cards.render_section_header(
        "AI Executive Report",
        "Generate an executive summary for ministry leadership.",
    )

    ministry_ai_panel.render(
        title="Executive Summary",
        button_label="✨ Generate Executive Summary",
        callback=context.ai_controller().generate_executive_summary,
        callback_kwargs={
            "report": report,
        },
        result_key="executive_summary",
        button_key="generate_executive_summary",
        help_text="Generate an executive report from the current session.",
        empty_message=(
            "Click 'Generate Executive Summary' "
            "to create an AI-powered leadership report."
        ),
    )

    st.divider()

    # =====================================================================
    # Export
    # =====================================================================

    metric_cards.render_section_header(
        "Export",
        "Export functionality planned for the next checkpoint.",
    )

    st.info(
        "Planned export formats:\n\n"
        "• PDF Ministry Report\n"
        "• Excel Workbook\n"
        "• CSV Export\n"
        "• AI Executive Summary\n"
        "• Printable Ministry Report"
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
                f"Attendance: {summary['attendance_count']} | "
                f"Activities: {summary['activity_count']}"
            )
        )

    with right_column:
        if st.button(
            "🔄 Refresh",
            use_container_width=True,
        ):
            st.rerun()
