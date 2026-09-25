"""
Centralized OpenAI API Service for Synthetic Minds.

Provides the single official interface for all AI generations across the platform:
- Agent decision-making and personas
- Graph and ontology extraction
- Simulation planning and orchestration
- Autonomous report generation and reflections
- Summarization and scenario analysis
"""

import json
import logging
import re
from typing import Optional, Dict, Any, List
from openai import (
    OpenAI,
    APIError,
    AuthenticationError,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
)

from ..config import Config
from ..utils.openai_chat_compat import create_chat_completion, extract_chat_completion_text


logger = logging.getLogger(__name__)


class OpenAIServiceError(Exception):
    """Base exception for Synthetic Minds OpenAI service errors with user-safe messages."""

    def __init__(self, message: str, *, status_code: Optional[int] = None, code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code


class OpenAIAuthenticationError(OpenAIServiceError):
    """Raised when the OpenAI API key is missing or invalid."""
    pass


class OpenAIRateLimitError(OpenAIServiceError):
    """Raised when OpenAI API rate limits are exceeded."""
    pass


class OpenAIQuotaError(OpenAIServiceError):
    """Raised when OpenAI account credit/quota is exhausted."""
    pass


class OpenAITimeoutError(OpenAIServiceError):
    """Raised when an OpenAI request times out."""
    pass


class OpenAIConnectionError(OpenAIServiceError):
    """Raised when unable to establish a connection to OpenAI."""
    pass


class OpenAIResponseError(OpenAIServiceError, ValueError):
    """Structured exception for unusable or malformed model responses."""

    def __init__(self, message: str, *, finish_reason: Optional[str] = None):
        super().__init__(message)
        self.finish_reason = finish_reason


def wrap_openai_error(error: Exception) -> OpenAIServiceError:
    """
    Wrap raw OpenAI SDK exceptions into sanitized, user-safe application errors.
    Ensures API keys, authorization tokens, and internal headers are never exposed.
    """
    if isinstance(error, OpenAIServiceError):
        return error

    if isinstance(error, AuthenticationError):
        return OpenAIAuthenticationError(
            "OpenAI API authentication failed. Please verify that your OPENAI_API_KEY is configured correctly.",
            status_code=401,
            code="invalid_api_key",
        )

    if isinstance(error, RateLimitError):
        err_msg = str(error).lower()
        if "quota" in err_msg or "billing" in err_msg or "insufficient_quota" in err_msg:
            return OpenAIQuotaError(
                "OpenAI API quota exceeded. Please check your OpenAI account billing and usage limits.",
                status_code=429,
                code="insufficient_quota",
            )
        return OpenAIRateLimitError(
            "OpenAI API rate limit exceeded. Please retry after a brief pause.",
            status_code=429,
            code="rate_limit_exceeded",
        )

    if isinstance(error, APITimeoutError):
        return OpenAITimeoutError(
            "OpenAI API request timed out. Please try again.",
            status_code=504,
            code="request_timeout",
        )

    if isinstance(error, APIConnectionError):
        return OpenAIConnectionError(
            "Failed to connect to the OpenAI API. Please check network connectivity.",
            status_code=502,
            code="connection_error",
        )

    if isinstance(error, APIError):
        return OpenAIServiceError(
            f"OpenAI API error occurred (code: {error.code or 'unknown'}).",
            status_code=error.status_code or 500,
            code=str(error.code or "api_error"),
        )

    return OpenAIServiceError(
        f"An unexpected AI service error occurred: {type(error).__name__}",
        status_code=500,
        code="internal_error",
    )


def _is_response_format_unsupported(error: Exception) -> bool:
    """Detect an explicit provider rejection of JSON response_format."""
    if getattr(error, "status_code", None) not in {400, 422}:
        return False

    body = getattr(error, "body", None)
    if not isinstance(body, dict):
        return False

    details = body.get("error", body)
    if not isinstance(details, dict):
        return False

    param = str(details.get("param") or "").strip().lower()
    if param == "response_format" or param.startswith("response_format."):
        return True

    message = str(details.get("message") or "").lower()
    if "response_format" not in message:
        return False

    code = str(details.get("code") or "").lower()
    unsupported_codes = {
        "unsupported_parameter",
        "unsupported_value",
        "unknown_parameter",
        "invalid_parameter",
    }
    unsupported_phrases = (
        "not support",
        "unsupported",
        "unknown parameter",
        "unrecognized parameter",
    )
    return code in unsupported_codes or any(
        phrase in message for phrase in unsupported_phrases
    )


def clean_chat_text(content: str) -> str:
    """Remove common reasoning wrappers and an outer Markdown JSON fence."""
    cleaned = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
    cleaned = cleaned.lstrip("\ufeff")
    cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\n?```\s*$', '', cleaned)
    return cleaned.strip()


def _contains_additional_json_container(content: str) -> bool:
    """Return True when trailing text embeds another JSON object or array."""
    decoder = json.JSONDecoder()
    for match in re.finditer(r"[\[{]", content):
        try:
            value, _ = decoder.raw_decode(content[match.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(value, (dict, list)):
            return True
    return False


class OpenAIService:
    """
    Unified OpenAI AI Service for Synthetic Minds.
    Manages official OpenAI SDK interactions, token budgeting, and JSON parsing.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model or Config.OPENAI_MODEL

        if not self.api_key:
            raise OpenAIAuthenticationError(
                "OPENAI_API_KEY is not configured. Please set OPENAI_API_KEY in your .env file."
            )

        self.client = OpenAI(api_key=self.api_key)

    def _create_completion(
        self,
        *,
        messages: List[Dict[str, str]],
        temperature: Optional[float],
        max_tokens: Optional[int],
        response_format: Optional[Dict[str, Any]],
    ) -> Any:
        """Send chat completion request through the compatibility layer."""
        return create_chat_completion(
            self.client,
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
        )

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = 4096,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Send a chat completion request to the OpenAI API.

        Args:
            messages: List of message dictionaries [{'role': 'user', 'content': '...'}]
            temperature: Sampling temperature
            max_tokens: Maximum tokens in completion
            response_format: Response format specifier (e.g. {'type': 'json_object'})

        Returns:
            Cleaned response string
        """
        try:
            response = self._create_completion(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format,
            )
            content = extract_chat_completion_text(response)
            return clean_chat_text(content)
        except Exception as error:
            if isinstance(error, OpenAIResponseError):
                raise
            wrapped = wrap_openai_error(error)
            logger.error("OpenAI chat error: %s", wrapped.message)
            raise wrapped from error

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: Optional[int] = 4096,
        max_attempts: int = 1,
    ) -> Dict[str, Any]:
        """
        Send a chat completion request expecting a valid JSON object return.

        Args:
            messages: List of message dictionaries
            temperature: Sampling temperature
            max_tokens: Maximum tokens in completion
            max_attempts: Number of parsing/regeneration attempts

        Returns:
            Parsed JSON dictionary
        """
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        response_format: Optional[Dict[str, str]] = {"type": "json_object"}
        request_max_tokens = max_tokens
        last_error: Optional[OpenAIResponseError] = None

        for attempt in range(1, max_attempts + 1):
            while True:
                try:
                    response = self._create_completion(
                        messages=messages,
                        temperature=temperature,
                        max_tokens=request_max_tokens,
                        response_format=response_format,
                    )
                except Exception as error:
                    if (
                        response_format is not None
                        and _is_response_format_unsupported(error)
                    ):
                        logger.warning(
                            "OpenAI rejected response_format; retrying once with prompt-only JSON guidance"
                        )
                        response_format = None
                        continue
                    raise
                break

            try:
                return self._parse_json_response(response)
            except OpenAIResponseError as error:
                last_error = error
                if attempt >= max_attempts:
                    raise

                had_token_cap = request_max_tokens is not None
                request_max_tokens = None
                logger.warning(
                    "OpenAI returned unusable JSON (finish_reason=%s); "
                    "retrying content generation%s",
                    error.finish_reason or "unknown",
                    " without an output token cap" if had_token_cap else "",
                )

        if last_error is not None:
            raise last_error
        raise OpenAIResponseError("OpenAI did not produce a JSON response")

    @staticmethod
    def _parse_json_response(response: Any) -> Dict[str, Any]:
        """Validate and parse a JSON completion response."""
        choices = getattr(response, "choices", None) or []
        if not choices:
            raise OpenAIResponseError("OpenAI returned no choices")

        choice = choices[0]
        finish_reason = getattr(choice, "finish_reason", None)
        if finish_reason == "length":
            raise OpenAIResponseError(
                "OpenAI JSON output was truncated at the token limit",
                finish_reason=finish_reason,
            )
        if finish_reason not in {None, "stop"}:
            raise OpenAIResponseError(
                f"OpenAI JSON generation stopped unexpectedly ({finish_reason})",
                finish_reason=finish_reason,
            )

        content = clean_chat_text(extract_chat_completion_text(response))
        if not content:
            raise OpenAIResponseError(
                "OpenAI returned empty JSON content",
                finish_reason=finish_reason,
            )

        try:
            value = json.loads(content)
        except json.JSONDecodeError as strict_error:
            try:
                value, end = json.JSONDecoder().raw_decode(content)
            except json.JSONDecodeError:
                raise OpenAIResponseError(
                    "OpenAI returned invalid JSON "
                    f"(line {strict_error.lineno}, column {strict_error.colno})",
                    finish_reason=finish_reason,
                ) from strict_error

            trailing = content[end:].strip()
            if trailing:
                if _contains_additional_json_container(trailing):
                    raise OpenAIResponseError(
                        "OpenAI returned multiple JSON values",
                        finish_reason=finish_reason,
                    )
                logger.warning("Ignoring text after a complete OpenAI JSON object")

        if not isinstance(value, dict):
            raise OpenAIResponseError(
                "OpenAI JSON response must be a top-level JSON object",
                finish_reason=finish_reason,
            )

        return value


# Global service instance accessor
_service_instance: Optional[OpenAIService] = None


def get_openai_service() -> OpenAIService:
    """Retrieve the singleton OpenAIService instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = OpenAIService()
    return _service_instance
