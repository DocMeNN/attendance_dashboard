# src/infrastructure/ai/providers/openai_provider.py

"""
OpenAI Provider

Purpose:
    Implements the AIProvider interface using the OpenAI API.

Architecture:
    Infrastructure Layer

Dependencies:
    OpenAIClient

Notes:
    This provider translates between the application's domain
    models and the OpenAI client.

Author: Me
"""

from __future__ import annotations

# Third-party imports
from openai import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    RateLimitError,
)

# Local application imports
from src.config.ai_config import AIConfig
from src.domain.ai.exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIProviderError,
    AIRateLimitError,
)
from src.domain.ai.models import AIRequest, AIResponse
from src.infrastructure.ai.clients.openai_client import OpenAIClient

from .base_provider import BaseAIProvider


class OpenAIProvider(BaseAIProvider):
    """
    AI provider backed by the OpenAI API.
    """

    def __init__(self, config: AIConfig) -> None:
        """
        Initialize the provider.
        """
        super().__init__(config)
        self._client = OpenAIClient(config)

    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Generate text using OpenAI.
        """

        messages: list[dict[str, str]] = []

        if request.system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": request.system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": request.prompt,
            }
        )

        try:
            response = self._client.generate(
                model=self.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

        except AuthenticationError as exc:
            raise AIAuthenticationError("OpenAI authentication failed.") from exc

        except RateLimitError as exc:
            raise AIRateLimitError("OpenAI rate limit exceeded.") from exc

        except APIConnectionError as exc:
            raise AIConnectionError("Unable to connect to OpenAI.") from exc

        except APIStatusError as exc:
            raise AIProviderError(f"OpenAI returned HTTP {exc.status_code}.") from exc

        message = self.require_text(response.choices[0].message.content)

        usage = response.usage

        return AIResponse(
            content=message,
            provider="openai",
            model=response.model,
            prompt_tokens=self.safe_int(usage.prompt_tokens if usage else 0),
            completion_tokens=self.safe_int(usage.completion_tokens if usage else 0),
            total_tokens=self.safe_int(usage.total_tokens if usage else 0),
            metadata={
                "finish_reason": response.choices[0].finish_reason,
            },
        )
