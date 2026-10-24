from types import SimpleNamespace
from unittest.mock import Mock

import httpx
import pytest
from google.genai import errors

import utils.ai_resume_analyzer as ai_module


@pytest.fixture
def analyzer_with_client(monkeypatch):
    client = Mock()
    monkeypatch.setattr(ai_module, "_configured_secret", lambda name: "test-key")
    monkeypatch.setattr(ai_module.genai, "Client", lambda api_key: client)
    return ai_module.AIResumeAnalyzer(), client


def test_missing_key_returns_configuration_error(monkeypatch):
    client_factory = Mock()
    monkeypatch.setattr(ai_module, "_configured_secret", lambda name: None)
    monkeypatch.setattr(ai_module.genai, "Client", client_factory)

    result = ai_module.AIResumeAnalyzer().analyze_resume_with_gemini("Fictional resume")

    assert "not configured" in result["error"]
    client_factory.assert_not_called()


def test_generate_content_uses_supported_model_and_returns_analysis(analyzer_with_client):
    analyzer, client = analyzer_with_client
    client.models.generate_content.return_value = SimpleNamespace(
        text="Resume Score: 80/100\nATS Score: 70/100"
    )

    result = analyzer.analyze_resume_with_gemini("Fictional resume")

    assert result["analysis"] == "Resume Score: 80/100\nATS Score: 70/100"
    client.models.generate_content.assert_called_once()
    assert (
        client.models.generate_content.call_args.kwargs["model"]
        == ai_module.GEMINI_MODEL
        == "gemini-3.8-flash"
    )


def test_empty_response_returns_actionable_error(analyzer_with_client):
    analyzer, client = analyzer_with_client
    client.models.generate_content.return_value = SimpleNamespace(text=None)

    result = analyzer.analyze_resume_with_gemini("Fictional resume")

    assert "no readable text" in result["error"]


def test_blocked_response_text_returns_actionable_error(analyzer_with_client):
    analyzer, client = analyzer_with_client

    class BlockedResponse:
        @property
        def text(self):
            raise ValueError("private response details")

    client.models.generate_content.return_value = BlockedResponse()

    result = analyzer.analyze_resume_with_gemini("Fictional resume")

    assert "no readable text" in result["error"]
    assert "private response details" not in result["error"]


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (400, "API credentials"),
        (401, "API credentials"),
        (403, "API credentials"),
        (404, "model or API endpoint"),
        (429, "quota or rate limit"),
        (503, "temporarily unavailable"),
    ],
)
def test_api_errors_are_reported_without_provider_details(
    analyzer_with_client, status, expected
):
    analyzer, client = analyzer_with_client
    client.models.generate_content.side_effect = errors.APIError(
        code=status,
        response_json={"error": {"code": status, "message": "private provider detail"}},
    )

    result = analyzer.analyze_resume_with_gemini("Fictional resume")

    assert expected in result["error"]
    assert "private provider detail" not in result["error"]


def test_timeout_returns_safe_connection_error(analyzer_with_client):
    analyzer, client = analyzer_with_client
    client.models.generate_content.side_effect = httpx.TimeoutException(
        "private request details"
    )

    result = analyzer.analyze_resume_with_gemini("Fictional resume")

    assert "timed out" in result["error"]
    assert "private request details" not in result["error"]


def test_connection_error_returns_safe_connection_error(analyzer_with_client):
    analyzer, client = analyzer_with_client
    client.models.generate_content.side_effect = httpx.ConnectError(
        "private request details"
    )

    result = analyzer.analyze_resume_with_gemini("Fictional resume")

    assert "Could not connect" in result["error"]
    assert "private request details" not in result["error"]
