# src/domain/ai/models.py

"""
AI Domain Models

Purpose:
    Defines the request and response models exchanged between the
    Application layer and AI providers.

Architecture:
    Domain Layer

Dependencies:
    Standard Library Only

Notes:
    These models are provider-agnostic and must not contain any
    provider-specific objects or SDK types.

Author: Me
"""

from __future__ import annotations

# Standard library imports
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class AIRequest:
    """
    Represents a structured request to an AI provider.
    """

    prompt: str
    system_prompt: str | None = None
    temperature: float = 0.3
    max_tokens: int = 1024
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class AIResponse:
    """
    Represents a structured response returned by an AI provider.
    """

    content: str
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
