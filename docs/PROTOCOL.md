# PROTOCOL.md

CLI signature and file format schemas for `desk-organizer`.

## CLI

<!-- Command name, arguments, flags, exit codes. -->

## MCP servers

### `pager` (`desk-pager`)

An ntfy.sh-backed paging server. Reads its config from `settings.json`/`settings.local.json`'s
`ntfy` section (see `PagerConfig.load` in `src/desk_organizer/mcp/pager/config.py`) — `topic`
required, `server`/`defaultTitle` optional, each overridable by an `NTFY_*` environment variable.

- **`notify(message, title=None, priority=3) -> str`** — sends a push notification. Returns
  `"notify sent"` on success or `"notify failed: <reason>"` on any failure (missing config, a bad
  `settings.json`, or the HTTP request itself failing) — never raises, so a failed page can't crash
  the caller's session.
- **`notify_debug(message, title=None, priority=3) -> str`** — identical to `notify`, except it
  first opens a `debugpy` listener on port 5678 (once per process — a module-level flag guards
  against rebinding an already-open port on a second call) and blocks until a debugger attaches
  before delegating to `notify`. Exists so a breakpoint in `notify`'s own body can catch a real,
  live call's arguments — see `README.md`'s "Debugging an MCP server" section for the actual
  workflow. Deliberately non-blocking at server *startup* (unlike an earlier iteration of this
  tool): blocking there raced the MCP host's own connection-handshake timeout, which killed the
  process before a human had time to attach.

## File formats

<!-- Schemas for any files this project reads or writes. -->

### `src/desk_organizer/skills/skills.json`

Declares which consumer repo(s) each authored skill applies to, so a future distribution
mechanism (e.g. [issue #2](https://github.com/croicu/desk-organizer/issues/2)'s planned
`desk-organizer pull-skills <target-repo>` CLI command) can select the right skills for a given
target without parsing every `SKILL.md`.

```json
{
  "skills": {
    "<skill-directory-name>": {
      "applies_to": ["<repo-name>", "..."]
    }
  }
}
```

- `<skill-directory-name>` matches the skill's directory name under `src/desk_organizer/skills/`
  exactly (e.g. `expose-gateway-method`).
- `applies_to` is a non-empty list of consumer repo names the skill is meant for (e.g.
  `["geo-builder"]`, or multiple repos if a skill genuinely applies to more than one). The reserved
  value `"general"` means the skill applies to any consumer repo, not one in particular — a skill
  entry uses either `"general"` alone or one-or-more specific repo names, never both.
- Every skill directory under `src/desk_organizer/skills/` must have a corresponding entry here —
  an undeclared skill has no defined applicability and should be treated as a bug, not silently
  skipped.
