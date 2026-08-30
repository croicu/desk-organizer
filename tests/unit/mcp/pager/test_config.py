from __future__ import annotations

import json
from pathlib import Path

import pytest

from desk_organizer.mcp.pager.config import DEFAULT_SERVER, DEFAULT_TITLE, PagerConfig, PagerConfigError


def _write_settings(path: Path, payload: dict) -> None:
    path.write_text(json.dumps({"settings": payload}), encoding="utf-8")


def test_load_requires_topic(tmp_path):
    settings_path = tmp_path / "settings.json"
    local_path = tmp_path / "settings.local.json"
    _write_settings(settings_path, {})

    with pytest.raises(PagerConfigError):
        PagerConfig.load(settings_path=settings_path, local_settings_path=local_path, environ={})


def test_load_reads_topic_from_settings_json(tmp_path):
    settings_path = tmp_path / "settings.json"
    local_path = tmp_path / "settings.local.json"
    _write_settings(settings_path, {"ntfy": {"topic": "abc-123"}})

    config = PagerConfig.load(settings_path=settings_path, local_settings_path=local_path, environ={})

    assert config.topic == "abc-123"
    assert config.server == DEFAULT_SERVER
    assert config.default_title == DEFAULT_TITLE


def test_load_reads_server_and_default_title_from_settings_json(tmp_path):
    settings_path = tmp_path / "settings.json"
    local_path = tmp_path / "settings.local.json"
    _write_settings(
        settings_path,
        {"ntfy": {"topic": "abc-123", "server": "https://ntfy.example.com", "defaultTitle": "Custom Title"}},
    )

    config = PagerConfig.load(settings_path=settings_path, local_settings_path=local_path, environ={})

    assert config.server == "https://ntfy.example.com"
    assert config.default_title == "Custom Title"


def test_local_settings_override_settings_json(tmp_path):
    settings_path = tmp_path / "settings.json"
    local_path = tmp_path / "settings.local.json"
    _write_settings(settings_path, {"ntfy": {"topic": "shared-topic"}})
    _write_settings(local_path, {"ntfy": {"topic": "personal-topic"}})

    config = PagerConfig.load(settings_path=settings_path, local_settings_path=local_path, environ={})

    assert config.topic == "personal-topic"


def test_env_vars_override_settings_json(tmp_path):
    settings_path = tmp_path / "settings.json"
    local_path = tmp_path / "settings.local.json"
    _write_settings(settings_path, {"ntfy": {"topic": "from-settings", "server": "https://from-settings.example.com"}})

    config = PagerConfig.load(
        settings_path=settings_path,
        local_settings_path=local_path,
        environ={"NTFY_TOPIC": "from-env", "NTFY_SERVER": "https://from-env.example.com"},
    )

    assert config.topic == "from-env"
    assert config.server == "https://from-env.example.com"


def test_env_var_alone_satisfies_required_topic(tmp_path):
    settings_path = tmp_path / "settings.json"
    local_path = tmp_path / "settings.local.json"

    config = PagerConfig.load(settings_path=settings_path, local_settings_path=local_path, environ={"NTFY_TOPIC": "from-env"})

    assert config.topic == "from-env"
