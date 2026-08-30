from __future__ import annotations

import json

from geo_organizer.mcp.pager import server


class FakeClient:
    last_call: dict | None = None

    def __init__(self, config) -> None:
        self.config = config

    def send(self, message, title, priority) -> str:
        FakeClient.last_call = {"message": message, "title": title, "priority": priority}
        return "notify sent"


def _write_settings(tmp_path, ntfy: dict) -> None:
    (tmp_path / "settings.json").write_text(json.dumps({"settings": {"ntfy": ntfy}}), encoding="utf-8")


def test_notify_requires_topic(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("NTFY_TOPIC", raising=False)

    result = server.notify("hello")

    assert result.startswith("notify failed")


def test_notify_sends_through_ntfy_client(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_settings(tmp_path, {"topic": "test-topic"})
    monkeypatch.setattr(server, "NtfyClient", FakeClient)

    result = server.notify("hello", title="Custom", priority=5)

    assert result == "notify sent"
    assert FakeClient.last_call == {"message": "hello", "title": "Custom", "priority": 5}
