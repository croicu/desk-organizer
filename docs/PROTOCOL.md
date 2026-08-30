# PROTOCOL.md

CLI signature and file format schemas for `desk-organizer`.

## CLI

<!-- Command name, arguments, flags, exit codes. -->

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
