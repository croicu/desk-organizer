from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from desk_organizer.settings import Settings

DEFAULT_SERVER = "https://ntfy.sh"
DEFAULT_TITLE = "desk-organizer"

_SETTINGS_PATH = Path("./settings.json")
_LOCAL_SETTINGS_PATH = Path("./settings.local.json")


class PagerConfigError(Exception):
    pass


@dataclass
class PagerConfig:
    topic: str
    server: str = DEFAULT_SERVER
    default_title: str = DEFAULT_TITLE

    @staticmethod
    def load(
        settings_path: Path = _SETTINGS_PATH,
        local_settings_path: Path = _LOCAL_SETTINGS_PATH,
        environ: dict[str, str] | None = None,
    ) -> PagerConfig:
        env = os.environ if environ is None else environ

        ntfy_payload = Settings.section("ntfy", path=settings_path, local_path=local_settings_path)

        # Env vars are a per-process override on top of settings.json, not the primary source —
        # settings.json is what's uniform across consumer repos, an env var is a one-off local
        # tweak (e.g. testing against a throwaway topic without editing a tracked file).
        topic = env.get("NTFY_TOPIC") or ntfy_payload.get("topic")
        if not topic:
            raise PagerConfigError(
                "ntfy topic is required: set 'settings.ntfy.topic' in settings.json (or settings.local.json), or the NTFY_TOPIC environment variable."
            )

        server = env.get("NTFY_SERVER") or ntfy_payload.get("server") or DEFAULT_SERVER
        default_title = env.get("NTFY_DEFAULT_TITLE") or ntfy_payload.get("defaultTitle") or DEFAULT_TITLE

        return PagerConfig(topic=str(topic), server=str(server), default_title=str(default_title))
