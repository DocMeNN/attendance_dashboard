# src/domain/analytics/insight.py

"""
Domain Insight Analytics

Purpose
-------
Provides business logic for analytical insights.

Responsibilities
----------------
- Retrieve insights.
- Filter insights by severity.
- Count insights by severity.
- Retrieve session-specific insights.
- Retrieve general insights.
- Rank insights by importance.

Notes
-----
- Pure domain analytics.
- No pandas.
- No Streamlit.
- No database access.
- No file I/O.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections import Counter
from collections.abc import Iterable
from datetime import date

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.models.insight_event import (
    InsightEvent,
    InsightSeverity,
)

# ============================================================================
# Retrieval
# ============================================================================


def get_insights(
    insights: Iterable[InsightEvent],
) -> tuple[InsightEvent, ...]:
    """
    Return insights in their supplied order.
    """

    return tuple(insights)


def get_insights_by_severity(
    insights: Iterable[InsightEvent],
    severity: InsightSeverity,
) -> tuple[InsightEvent, ...]:
    """
    Return insights matching the specified severity.
    """

    return tuple(insight for insight in insights if insight.severity is severity)


def get_session_insights(
    insights: Iterable[InsightEvent],
    session_date: date,
) -> tuple[InsightEvent, ...]:
    """
    Return insights associated with a specific session date.
    """

    return tuple(
        insight for insight in insights if insight.session_date == session_date
    )


def get_general_insights(
    insights: Iterable[InsightEvent],
) -> tuple[InsightEvent, ...]:
    """
    Return insights not associated with a specific session.
    """

    return tuple(insight for insight in insights if insight.session_date is None)


# ============================================================================
# Classification
# ============================================================================


def get_positive_insights(
    insights: Iterable[InsightEvent],
) -> tuple[InsightEvent, ...]:
    """
    Return positive insights.
    """

    return get_insights_by_severity(
        insights,
        InsightSeverity.POSITIVE,
    )


def get_warning_insights(
    insights: Iterable[InsightEvent],
) -> tuple[InsightEvent, ...]:
    """
    Return warning insights.
    """

    return get_insights_by_severity(
        insights,
        InsightSeverity.WARNING,
    )


def get_critical_insights(
    insights: Iterable[InsightEvent],
) -> tuple[InsightEvent, ...]:
    """
    Return critical insights.
    """

    return get_insights_by_severity(
        insights,
        InsightSeverity.CRITICAL,
    )


def get_informational_insights(
    insights: Iterable[InsightEvent],
) -> tuple[InsightEvent, ...]:
    """
    Return informational insights.
    """

    return get_insights_by_severity(
        insights,
        InsightSeverity.INFO,
    )


# ============================================================================
# Counts
# ============================================================================


def count_insights(
    insights: Iterable[InsightEvent],
) -> int:
    """
    Return total insight count.
    """

    return len(get_insights(insights))


def count_insights_by_severity(
    insights: Iterable[InsightEvent],
) -> Counter[InsightSeverity]:
    """
    Count insights grouped by severity.
    """

    return Counter(insight.severity for insight in insights)


# ============================================================================
# Importance
# ============================================================================


def _severity_priority(
    severity: InsightSeverity,
) -> int:
    """
    Return the analytical priority of a severity.
    """

    priorities = {
        InsightSeverity.CRITICAL: 4,
        InsightSeverity.WARNING: 3,
        InsightSeverity.POSITIVE: 2,
        InsightSeverity.INFO: 1,
    }

    return priorities[severity]


def sort_by_importance(
    insights: Iterable[InsightEvent],
) -> tuple[InsightEvent, ...]:
    """
    Return insights ordered from highest to lowest importance.

    Within the same severity, the original order is preserved.
    """

    return tuple(
        sorted(
            insights,
            key=lambda insight: _severity_priority(insight.severity),
            reverse=True,
        )
    )


def highest_priority_insight(
    insights: Iterable[InsightEvent],
) -> InsightEvent | None:
    """
    Return the highest-priority insight.
    """

    ordered = sort_by_importance(insights)

    if not ordered:
        return None

    return ordered[0]


def top_insights(
    insights: Iterable[InsightEvent],
    limit: int = 10,
) -> tuple[InsightEvent, ...]:
    """
    Return the highest-priority insights.
    """

    if limit < 1:
        raise ValueError("limit must be greater than zero.")

    return sort_by_importance(insights)[:limit]


# ============================================================================
# Summary
# ============================================================================


def insight_summary(
    insights: Iterable[InsightEvent],
) -> dict[str, object]:
    """
    Return a summary of insight analytics.
    """

    collected = get_insights(insights)

    return {
        "insight_count": len(collected),
        "severity_counts": count_insights_by_severity(collected),
        "positive_count": len(get_positive_insights(collected)),
        "warning_count": len(get_warning_insights(collected)),
        "critical_count": len(get_critical_insights(collected)),
        "informational_count": len(get_informational_insights(collected)),
        "session_specific_count": sum(
            insight.is_session_specific for insight in collected
        ),
        "general_count": len(get_general_insights(collected)),
        "highest_priority": highest_priority_insight(collected),
    }
