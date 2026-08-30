# desk-organizer

desk-organizer is a personal authoring hub for AI tooling: Claude Code skills, agent definitions,
and MCP servers for whichever of the user's own projects need them. It is an authoring tool, not a
runtime dependency — artifacts are generated here, delivered into a consumer's `.claude/`
directory, and committed into that repo.

Authoring for the geo-family repos (`geo-builder`, `geo-browser`) is what this repo started as, and
it's still a live capability — but it's one capability among several now, not the whole mission.
Non-geo work authored here for its own sake (e.g. `desk-pager`, a general-purpose paging MCP
server) is equally in scope.

| Type | Format | Delivered to | Executable |
|---|---|---|---|
| Skill | `SKILL.md` + optional bundled scripts | `<consumer>/.claude/skills/` | no |
| Agent | agent definition markdown | `<consumer>/.claude/agents/` | no |
| MCP server | Python package | installed in consumer environment | yes |

Once delivered, a consumer runs standalone — desk-organizer does not need to exist on the same
machine, and nothing here is imported, invoked, or resolved at consumer runtime.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for ownership boundaries, the distribution
model, and repository layout.

---

## Install

```bash
pip install -e ".[dev]"
```

## Lint

```bash
ruff check src/ tests/
ruff format src/ tests/
```

## Test

```bash
pytest
pytest tests/unit/test_foo.py::test_bar   # single test
```

## Debugging an MCP server

The pager MCP server is normally launched by the MCP host (Claude Code), not by a debugger, so a
breakpoint needs an attach rather than a launch:

1. In `.mcp.json`, temporarily add `"DESK_PAGER_DEBUGPY": "1"` to the `pager` entry's `env`, then
   reconnect the `pager` MCP server so it relaunches with that variable set. The process will block
   at startup, waiting for a debugger.
2. Run the **Python: Attach to desk-pager** launch config in VS Code. Once attached, the server
   continues; a breakpoint in `notify()` now hits on the next tool call.
3. Revert the `.mcp.json` change when done — leaving `DESK_PAGER_DEBUGPY` set makes every future
   `pager` connection hang until a debugger attaches.
