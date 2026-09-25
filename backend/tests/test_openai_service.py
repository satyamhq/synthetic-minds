from types import SimpleNamespace
import pytest
from unittest.mock import MagicMock, patch

from openai import (
    AuthenticationError,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
    APIError,
)

from app.services.openai_service import (
    OpenAIService,
    OpenAIServiceError,
    OpenAIAuthenticationError,
    OpenAIRateLimitError,
    OpenAIQuotaError,
    OpenAITimeoutError,
    OpenAIConnectionError,
    OpenAIResponseError,
    wrap_openai_error,
    clean_chat_text,
    get_openai_service,
)


def test_missing_api_key_raises_auth_error():
    with patch("app.services.openai_service.Config.OPENAI_API_KEY", None):
        with pytest.raises(OpenAIAuthenticationError, match="OPENAI_API_KEY is not configured"):
            OpenAIService(api_key=None)


def test_wrap_authentication_error():
    mock_err = AuthenticationError(
        message="Incorrect API key provided: sk-secret-12345",
        response=MagicMock(status_code=401, headers={}),
        body={"error": {"message": "Incorrect API key"}},
    )
    wrapped = wrap_openai_error(mock_err)
    assert isinstance(wrapped, OpenAIAuthenticationError)
    assert "sk-secret-12345" not in wrapped.message
    assert "verify that your OPENAI_API_KEY is configured" in wrapped.message


def test_wrap_rate_limit_and_quota_errors():
    rate_err = RateLimitError(
        message="Rate limit reached for requests per minute",
        response=MagicMock(status_code=429, headers={}),
        body={},
    )
    wrapped_rate = wrap_openai_error(rate_err)
    assert isinstance(wrapped_rate, OpenAIRateLimitError)
    assert wrapped_rate.code == "rate_limit_exceeded"

    quota_err = RateLimitError(
        message="You exceeded your current quota, please check your plan and billing details.",
        response=MagicMock(status_code=429, headers={}),
        body={},
    )
    wrapped_quota = wrap_openai_error(quota_err)
    assert isinstance(wrapped_quota, OpenAIQuotaError)
    assert wrapped_quota.code == "insufficient_quota"


def test_wrap_timeout_and_connection_errors():
    timeout_err = APITimeoutError(request=MagicMock())
    wrapped_timeout = wrap_openai_error(timeout_err)
    assert isinstance(wrapped_timeout, OpenAITimeoutError)

    conn_err = APIConnectionError(request=MagicMock())
    wrapped_conn = wrap_openai_error(conn_err)
    assert isinstance(wrapped_conn, OpenAIConnectionError)


def test_clean_chat_text():
    raw = "<think>internal reasoning steps</think>```json\n{\"status\": \"active\"}\n```"
    cleaned = clean_chat_text(raw)
    assert cleaned == '{"status": "active"}'


def test_chat_json_success():
    service = object.__new__(OpenAIService)
    service.model = "gpt-4o-mini"
    mock_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                finish_reason="stop",
                message=SimpleNamespace(content='{"status": "ok", "value": 42}'),
            )
        ]
    )
    service._create_completion = MagicMock(return_value=mock_response)

    result = service.chat_json(messages=[{"role": "user", "content": "hi"}])
    assert result == {"status": "ok", "value": 42}
