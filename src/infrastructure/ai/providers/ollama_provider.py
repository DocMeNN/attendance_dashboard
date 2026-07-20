# src/infrastructure/ai/providers/ollama_provider.py

"""
Ollama Provider

Purpose:
    Implements the AIProvider interface using the Ollama REST API.

Architecture:
    Infrastructure Layer

Dependencies:
    OllamaClient

Notes:
    This provider translates between domain AI models and
    the Ollama client response format.

Author:
    Me
"""

from __future__ import annotations

# ============================================================================
# Local Imports
# ============================================================================
from src.config.ai_config import AIConfig
from src.domain.ai.models import AIRequest, AIResponse
from src.infrastructure.ai.clients.ollama_client import OllamaClient

from .base_provider import BaseAIProvider

# ============================================================================
# Provider
# ============================================================================


class OllamaProvider(BaseAIProvider):
    """
    AI provider backed by an Ollama server.
    """

    def __init__(
        self,
        config: AIConfig,
    ) -> None:
        """
        Initialize Ollama provider.
        """

        super().__init__(
            config,
        )

        self._client = OllamaClient(
            config,
        )

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Generate AI response using Ollama.
        """

        data = self._client.generate(
            model=self.model,
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
        )

        content = self.require_text(
            data.get("response"),
        )

        prompt_tokens = self.safe_int(
            data.get("prompt_eval_count"),
        )

        completion_tokens = self.safe_int(
            data.get("eval_count"),
        )

        return AIResponse(
            content=content,
            provider="ollama",
            model=self.model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=(prompt_tokens + completion_tokens),
            metadata=data,
        )
