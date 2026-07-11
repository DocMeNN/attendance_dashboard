# src/presentation/pages/reports_page.py

"""
Reports Page

Purpose
-------
Displays reporting functionality.

Responsibilities
----------------
- Render reports page UI.
- Prepare future report generation workflow.

Architectural Rules
-------------------
- Presentation only.
- No file generation.
- No business logic.
"""

from __future__ import annotations

import streamlit as st


def render() -> None:
    """
    Render the Reports page.
    """

    st.title("📄 Reports")

    st.info(
        "Reports page.\n\n"
        "PDF, Excel and export functionality will be implemented here."
    )
