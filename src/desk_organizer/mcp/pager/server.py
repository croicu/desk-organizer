from __future__ import annotations

import logging
import os

from mcp.server.mcpserver import MCPServer

from .config import PagerConfig
from .ntfy import NtfyClient

# The stdio transport this server runs over reserves stdout for the MCP JSON-RPC stream —
# anything else written there corrupts the protocol. desk_organizer.diagnostics.ConsoleLogSink
# prints to stdout by design, so it's the wrong sink for this process; stdlib logging propagates
# to the root logger that mcp.run() configures with a stderr handler instead (see
# mcp.server.mcpserver.utilities.logging.configure_logging).
_logger = logging.getLogger(__name__)

mcp = MCPServer("pager")


@mcp.tool()
def notify(message: str, title: str | None = None, priority: int = 3) -> str:
    """Send a push notification to the user's phone. Use ONLY when the user has explicitly
    asked to be notified or paged about something — for example "let me know when the
    build finishes" or "page me if this fails". Do not use it to report ordinary
    progress, to confirm you finished a short task, or because a result seems
    interesting. If the user has not asked to be paged, do not call this tool.
    """
    try:
        config = PagerConfig.load()
    except Exception as error:
        # Covers PagerConfigError (missing/malformed ntfy config) and TaskError (malformed
        # settings.json) alike — a bad config must fail the same as a bad send: an error
        # string back to the caller, never a raised exception.
        _logger.error("pager: configuration error: %s", error)
        return f"notify failed: {error}"

    result = NtfyClient(config).send(message, title, priority)

    # Never log message bodies — they may contain repo content.
    if result.startswith("notify failed"):
        _logger.warning("pager: %s", result)
    else:
        _logger.info("pager: notification sent")

    return result


def main() -> None:
    if os.environ.get("DESK_PAGER_DEBUGPY") == "1":
        # Opt-in only: this process is normally launched by the MCP host (Claude Code), not by a
        # debugger, so there's nothing to attach to unless explicitly requested. Blocks startup
        # until VS Code's "Python: Attach to desk-pager" config attaches, so the very first tool
        # call — not just a later one — can hit a breakpoint.
        import debugpy

        debugpy.listen(5678)
        debugpy.wait_for_client()

    mcp.run()


if __name__ == "__main__":
    main()
