# src/infrastructure/ai/providers/gemini_provider.py

"""
Gemini Provider

Purpose:
    Implements the AIProvider interface using Google Gemini.

Architecture:
    Infrastructure Layer

Dependencies:
    GeminiClient

Notes:
    This provider translates between domain models and the
    Gemini client.

Author: Me
"""

from __future__ import annotations

# Local application imports
from src.config.ai_config import AIConfig
from src.domain.ai.models import AIRequest, AIResponse
from src.infrastructure.ai.clients.gemini_client import GeminiClient

from .base_provider import BaseAIProvider


class GeminiProvider(BaseAIProvider):
    """
    AI provider backed by Google Gemini.
    """

    def __init__(
        self,
        config: AIConfig,
    ) -> None:
        super().__init__(config)
        self._client = GeminiClient(config)

    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Generate text using Gemini.
        """

        response = self._client.generate(
            model=self.model,
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        text = self.require_text(response.text)

        usage = getattr(
            response,
            "usage_metadata",
            None,
        )

        return AIResponse(
            content=text,
            provider="gemini",
            model=self.model,
            prompt_tokens=self.safe_int(
                getattr(
                    usage,
                    "prompt_token_count",
                    0,
                )
            ),
            completion_tokens=self.safe_int(
                getattr(
                    usage,
                    "candidates_token_count",
                    0,
                )
            ),
            total_tokens=self.safe_int(
                getattr(
                    usage,
                    "total_token_count",
                    0,
                )
            ),
            metadata={
                "finish_reason": getattr(
                    response,
                    "finish_reason",
                    None,
                ),
            },
        )
