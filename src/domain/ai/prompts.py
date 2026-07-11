# src/domain/ai/prompts.py

"""
AI Prompt Templates

Purpose:
    Centralizes reusable prompt templates for the AI subsystem.

Architecture:
    Domain Layer

Dependencies:
    Standard Library Only

Notes:
    Prompt templates are provider-agnostic and should contain only
    formatting logic. Rendering a prompt does not invoke any AI service.

Author: Me
"""

from __future__ import annotations

# Standard library imports
from enum import StrEnum


class PromptTemplate(StrEnum):
    """
    Identifiers for supported AI prompt templates.
    """

    SESSION_SUMMARY = "session_summary"
    SCRIPTURE_SUMMARY = "scripture_summary"
    MESSAGE_INSIGHTS = "message_insights"
    PERSON_OF_THE_WEEK = "person_of_the_week"
    TREND_ANALYSIS = "trend_analysis"
    EXECUTIVE_SUMMARY = "executive_summary"


PROMPTS: dict[PromptTemplate, str] = {
    PromptTemplate.SESSION_SUMMARY: """
You are an assistant helping ministry leaders summarize a church session.

Session Information
-------------------
{session_information}

Attendance Summary
------------------
{attendance_summary}

Activity Summary
----------------
{activity_summary}

Produce:

1. Session overview
2. Major discussion points
3. Key observations
4. Recommendations

Keep the response concise and factual.
""",
    PromptTemplate.SCRIPTURE_SUMMARY: """
Summarize the following scripture passage.

Scripture:
{scripture}

Include:

- Main theme
- Key lessons
- Practical application
""",
    PromptTemplate.MESSAGE_INSIGHTS: """
Analyze the following discussion messages.

Messages:
{messages}

Identify:

- Major topics
- Frequently discussed themes
- Questions raised
- Action items
""",
    PromptTemplate.PERSON_OF_THE_WEEK: """
Based on the following participation metrics:

{metrics}

Identify outstanding contributors.

Explain the reasoning without inventing information.
""",
    PromptTemplate.TREND_ANALYSIS: """
Analyze these session metrics.

{metrics}

Describe:

- Attendance trends
- Engagement trends
- Significant changes
- Recommendations
""",
    PromptTemplate.EXECUTIVE_SUMMARY: """
Generate an executive summary.

Data:
{report}

Provide:

- High-level overview
- Important findings
- Strategic recommendations

Keep the summary suitable for ministry leadership.
""",
}


def render_prompt(
    template: PromptTemplate,
    **kwargs: object,
) -> str:
    """
    Render a prompt template using keyword arguments.

    Parameters
    ----------
    template:
        Prompt template identifier.

    **kwargs:
        Values substituted into the template.

    Returns
    -------
    str
        Fully rendered prompt.

    Raises
    ------
    KeyError
        If a required placeholder is missing.
    """
    return PROMPTS[template].format(**kwargs)
