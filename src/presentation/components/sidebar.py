# src/presentation/components/sidebar.py

"""
Sidebar Components

Purpose
-------
Reusable sidebar components for the Presentation layer.

Responsibilities
----------------
- Render application information.
- Render session information.
- Display quick actions.
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
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Sidebar Title
# ============================================================================


def render_title(
    title: str,
) -> None:
    """
    Render the sidebar title.
    """

    st.sidebar.title(title)


# ============================================================================
# Sidebar Section
# ============================================================================


def render_section(
    heading: str,
) -> None:
    """
    Render a sidebar section heading.
    """

    st.sidebar.subheader(heading)


# ============================================================================
# Sidebar Text
# ============================================================================


def render_text(
    text: str,
) -> None:
    """
    Render sidebar text.
    """

    st.sidebar.write(text)


# ============================================================================
# Sidebar Success
# ============================================================================


def render_success(
    message: str,
) -> None:
    """
    Render a success message.
    """

    st.sidebar.success(message)


# ============================================================================
# Sidebar Warning
# ============================================================================


def render_warning(
    message: str,
) -> None:
    """
    Render a warning message.
    """

    st.sidebar.warning(message)


# ============================================================================
# Sidebar Info
# ============================================================================


def render_info(
    message: str,
) -> None:
    """
    Render an informational message.
    """

    st.sidebar.info(message)


# ============================================================================
# Sidebar Divider
# ============================================================================


def render_divider() -> None:
    """
    Render a sidebar divider.
    """

    st.sidebar.divider()
