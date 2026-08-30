from __future__ import annotations

import requests

from .config import PagerConfig

TIMEOUT_SECONDS = 5


class NtfyClient:
    def __init__(self, config: PagerConfig, session: requests.Session | None = None) -> None:
        self._config = config
        self._session = requests.Session() if session is None else session

    def send(self, message: str, title: str | None, priority: int) -> str:
        url = f"{self._config.server}/{self._config.topic}"
        headers = {
            "Title": self._config.default_title if title is None else title,
            "Priority": str(priority),
        }

        try:
            response = self._session.post(url, data=message.encode("utf-8"), headers=headers, timeout=TIMEOUT_SECONDS)
        except Exception as error:
            # A failed page must never abort the caller's session, so every failure mode —
            # network error, timeout, header encoding — collapses to an error string here
            # rather than propagating.
            return f"notify failed: {error.__class__.__name__}"

        if response.status_code < 200 or response.status_code >= 300:
            return f"notify failed: server returned status {response.status_code}"

        return "notify sent"
