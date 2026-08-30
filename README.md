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
breakpoint needs an attach rather than a launch. `notify_debug()` handles this without any
`.mcp.json` editing or a second server: it's the same server as `notify()`, just gated to open a
`debugpy` listener (port 5678, on first use) and block until a debugger attaches, before delegating
to `notify()`.

1. Set a breakpoint in `notify()`.
2. Ask for a page via `notify_debug()` specifically, not the normal `notify()` — this call hangs
   until a debugger attaches.
3. Run the **Python: Attach to desk-pager** launch config in VS Code. Attaching unblocks the call,
   which proceeds straight into `notify()` and hits your breakpoint.
