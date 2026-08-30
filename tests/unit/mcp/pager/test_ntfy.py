from __future__ import annotations

from dataclasses import dataclass

from geo_organizer.mcp.pager.config import PagerConfig
from geo_organizer.mcp.pager.ntfy import NtfyClient


@dataclass
class FakeResponse:
    status_code: int


class FakeSession:
    def __init__(self, status_code: int = 200, exception: Exception | None = None) -> None:
        self._status_code = status_code
        self._exception = exception
        self.calls: list[dict] = []

    def post(self, url, data=None, headers=None, timeout=None):
        self.calls.append({"url": url, "data": data, "headers": headers, "timeout": timeout})
        if self._exception is not None:
            raise self._exception
        return FakeResponse(status_code=self._status_code)


def _config() -> PagerConfig:
    return PagerConfig(topic="test-topic", server="https://ntfy.example.com", default_title="Default Title")


def test_send_success_returns_confirmation():
    session = FakeSession(status_code=200)
    client = NtfyClient(_config(), session=session)

    result = client.send("hello", None, 3)

    assert result == "notify sent"


def test_send_posts_to_topic_url():
    session = FakeSession(status_code=200)
    client = NtfyClient(_config(), session=session)

    client.send("hello", None, 3)

    assert session.calls[0]["url"] == "https://ntfy.example.com/test-topic"
    assert session.calls[0]["data"] == b"hello"


def test_send_defaults_title_when_not_given():
    session = FakeSession(status_code=200)
    client = NtfyClient(_config(), session=session)

    client.send("hello", None, 3)

    assert session.calls[0]["headers"]["Title"] == "Default Title"
    assert session.calls[0]["headers"]["Priority"] == "3"


def test_send_uses_explicit_title_and_priority():
    session = FakeSession(status_code=200)
    client = NtfyClient(_config(), session=session)

    client.send("hello", "Custom", 5)

    assert session.calls[0]["headers"]["Title"] == "Custom"
    assert session.calls[0]["headers"]["Priority"] == "5"


def test_send_non_2xx_returns_error_without_raising():
    session = FakeSession(status_code=500)
    client = NtfyClient(_config(), session=session)

    result = client.send("hello", None, 3)

    assert result.startswith("notify failed")


def test_send_exception_returns_error_without_raising():
    session = FakeSession(exception=TimeoutError("boom"))
    client = NtfyClient(_config(), session=session)

    result = client.send("hello", None, 3)

    assert result.startswith("notify failed")
