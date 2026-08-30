# Rename geo-organizer to desk-organizer

<!-- Run this in the fresh clone, after the GitHub repo itself has already been renamed
     (`gh repo rename desk-organizer` or via Settings) and cloned under the new name/URL. -->

## Status: Brainstorm

## Problem statement

The repo has outgrown its original scope — it was named and mission-scoped around one thing
(authoring Claude Code skills/agents/MCP servers for the `geo`-family repos: `geo-builder`,
`geo-browser`) but has since taken on work that isn't geo-specific at all (e.g. `geo-pager`, a
general-purpose paging MCP server). The rename to `desk-organizer` is prompted by that scope
growth, so it isn't cosmetic-only — `CLAUDE.md`'s Mission section is written entirely in terms of
the old, narrower scope and needs to actually be rewritten, not just find-and-replaced.

A GitHub rename by itself only changes the repo's name/URL (GitHub redirects the old URL, and
issues/PRs/history all carry over automatically). It does **not** touch the repo's internal
identity: the Python package name, the CLI entry point, or every prose reference to
"geo-organizer" across `CLAUDE.md`/docs/README. That's this task.

## Open questions

Resolve these before/while rewriting `CLAUDE.md`'s Mission section — they're design decisions,
not mechanical renames:

- What is `desk-organizer`'s actual scope now? Still "authoring hub for the geo family, plus
  some personal tooling," or has the geo-family-authoring piece become one capability among
  several rather than the whole mission?
- Does `geo-pager` itself get renamed (e.g. to `desk-pager`)? Its own settings.json convention
  is currently described as "uniform across the geo-family repos" (see `Settings.section()`'s
  docstring in `settings.py` and the pager's own history in issue
  [#6](https://github.com/croicu/geo-organizer/issues/6)) — if the scope is no longer
  geo-family-specific, that framing needs revisiting too, independent of the rename itself.
- Does the "Cross-Repo Coordination" section's relationship to `geo-builder`/`geo-browser` still
  hold as-is, or does it need reframing now that this repo isn't only about that boundary?
- Package/CLI naming: `desk_organizer` (package) / `desk-organizer` (CLI) is the obvious mechanical
  choice, matching the existing `geo_organizer`/`geo-organizer` pattern — confirm before running
  the mechanical steps below, since it's the one truly mechanical decision here.

## Implementation plan

Mechanical steps, once the questions above are settled:

1. **Package**: rename `src/geo_organizer/` → `src/desk_organizer/`. Update every intra-package
   import that spells the name out explicitly (relative imports like `from .settings import
   Settings` are unaffected; absolute imports aren't — grep for `geo_organizer` across
   `src/` and `tests/` and update each hit):
   - `src/geo_organizer/mcp/pager/config.py`, `server.py`
   - `tests/unit/mcp/pager/test_config.py`, `test_ntfy.py`, `test_server.py`
   - `tests/unit/test_settings.py`, `tests/unit/test_placeholder.py`
2. **`pyproject.toml`**:
   - `[project] name = "geo-organizer"` → `"desk-organizer"`
   - `description` — rewrite once the Mission section's new wording is settled, don't just
     swap the name in the old sentence
   - `[project.scripts]`: `geo-organizer = "geo_organizer.cli:main"` →
     `desk-organizer = "desk_organizer.cli:main"`; update `geo-pager`'s target module path
     regardless of whether the pager itself gets renamed (still moves with the package)
   - `dev` extra's self-reference `"geo-organizer[pager]"` → `"desk-organizer[pager]"`
3. **`.vscode/launch.json`**: `"module": "geo_organizer.cli"` → `"desk_organizer.cli"`
4. **`CLAUDE.md`**:
   - Rewrite the Mission section per the open questions above — not a find-and-replace, an
     actual rewrite
   - Update the `geo-organizer` references at the Commands section and the `Logger` import
     example (`from geo_organizer.diagnostics import Logger`)
   - **Leave the historical "Completed Tasks" entries alone** (e.g. "Repo Setup — instantiated
     from tpl-py as geo-organizer...") — those describe what actually happened at the time, not
     the repo's current name. Add a new entry for this rename instead of editing old ones.
   - Template Sync section needs no change — it doesn't reference this repo's own name.
5. **`docs/ARCHITECTURE.md`**, **`docs/PROTOCOL.md`**, **`README.md`**: same treatment — update
   the repo-name references and the `src/geo_organizer/` path in the repository-structure tree;
   `README.md`'s opening paragraph mirrors `CLAUDE.md`'s Mission wording, so update both together
   for consistency.
6. **`.mcp.json`**: only needs a change if `geo-pager`'s console-script name itself changes
   (see Open questions) — if so, re-run `claude mcp add` with the new command and expect a fresh
   approval prompt.
7. **Verify**: `pip install -e ".[dev]"`, `ruff check src/ tests/`, `ruff format src/ tests/`,
   `pytest`, `desk-organizer` (CLI runs), and re-approve/test the pager MCP server if its command
   name changed.
8. **tpl-py cross-link cleanup (optional, low priority)**: [tpl-py#7](https://github.com/croicu/tpl-py/issues/7)'s
   body says "Source: croicu/geo-organizer" — the link still resolves via GitHub's redirect, but
   a comment noting the new name avoids confusion for anyone reading the issue cold.
9. Add a "Repo Renamed to desk-organizer" entry to `CLAUDE.md`'s Completed Tasks once done,
   matching the existing entries' style.

## Test results

<!-- Fill in once run: ruff/pytest status, CLI smoke test, pager MCP re-registration if applicable. -->
