from __future__ import annotations

import json

import pytest

from geo_organizer.errors import TaskError
from geo_organizer.settings import Settings


def _write(path, payload: dict) -> None:
    path.write_text(json.dumps({"settings": payload}), encoding="utf-8")


def test_section_returns_empty_dict_when_missing(tmp_path):
    settings_path = tmp_path / "settings.json"
    local_path = tmp_path / "settings.local.json"
    _write(settings_path, {})

    assert Settings.section("ntfy", path=settings_path, local_path=local_path) == {}


def test_section_returns_named_section(tmp_path):
    settings_path = tmp_path / "settings.json"
    local_path = tmp_path / "settings.local.json"
    _write(settings_path, {"ntfy": {"topic": "abc-123"}})

    assert Settings.section("ntfy", path=settings_path, local_path=local_path) == {"topic": "abc-123"}


def test_section_merges_local_override(tmp_path):
    settings_path = tmp_path / "settings.json"
    local_path = tmp_path / "settings.local.json"
    _write(settings_path, {"ntfy": {"topic": "shared-topic"}})
    _write(local_path, {"ntfy": {"topic": "personal-topic"}})

    assert Settings.section("ntfy", path=settings_path, local_path=local_path) == {"topic": "personal-topic"}


def test_section_rejects_non_object_section(tmp_path):
    settings_path = tmp_path / "settings.json"
    local_path = tmp_path / "settings.local.json"
    _write(settings_path, {"ntfy": "not-an-object"})

    with pytest.raises(TaskError):
        Settings.section("ntfy", path=settings_path, local_path=local_path)
