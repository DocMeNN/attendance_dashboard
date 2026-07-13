# src/infrastructure/ai/clients/openai_client.py

"""
OpenAI SDK Client

Purpose:
    Encapsulates all communication with the OpenAI SDK.

Architecture:
    Infrastructure Layer

Author: Me
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from typing import Any

# ============================================================================
# Third-Party Imports
# ============================================================================
from openai import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)
from openai.types.chat import ChatCompletionMessageParam

# ============================================================================
# Local Imports
# ============================================================================
from src.config.ai_config import AIConfig
from src.domain.ai.exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIProviderError,
    AIRateLimitError,
)

# ============================================================================
# OpenAI Client
# ============================================================================


class OpenAIClient:
    """
    Thin wrapper around the OpenAI SDK.
    """

    def __init__(
        self,
        config: AIConfig,
    ) -> None:
        """
        Initialize the OpenAI SDK client.
        """

        self._client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )

    def generate(
        self,
        *,
        model: str,
        messages: list[ChatCompletionMessageParam],
        temperature: float,
        max_tokens: int,
    ) -> Any:
        """
        Execute a chat completion request.

        Parameters
        ----------
        model:
            OpenAI model name.

        messages:
            Conversation messages.

        temperature:
            Sampling temperature.

        max_tokens:
            Maximum number of output tokens.

        Returns
        -------
        Any
            Raw OpenAI SDK response.
        """

        try:
            return self._client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        except AuthenticationError as exc:
            raise AIAuthenticationError("OpenAI authentication failed.") from exc

        except RateLimitError as exc:
            raise AIRateLimitError("OpenAI rate limit exceeded.") from exc

        except APIConnectionError as exc:
            raise AIConnectionError("Unable to connect to OpenAI.") from exc

        except APIStatusError as exc:
            raise AIProviderError(f"OpenAI returned HTTP {exc.status_code}.") from exc
