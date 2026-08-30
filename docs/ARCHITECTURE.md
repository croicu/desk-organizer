# ARCHITECTURE.md

Modules, data flow, and contracts for `desk-organizer`. See `CLAUDE.md`'s `## Mission` for the
one-paragraph summary this document expands on.

## Ownership

### desk-organizer owns

- skill authoring (`SKILL.md` content and structure)
- agent definitions
- MCP server implementation
- conventions for deriving invariants from a producer/consumer boundary
- packaging and distribution of anything executable

### Consumers own

- their `.claude/` directory contents once delivered
- when to update
- whether to accept a generated artifact at all

## Distribution model

```text
desk-organizer
→ generate artifact
→ deliver into <consumer>/.claude/
→ commit in the consumer repo
```

Delivered artifacts version with the repo they govern, not with this one. MCP servers are
distributed as installable Python packages, not as source to be cloned or path-referenced. Once
delivered, a consumer runs standalone — nothing here is imported, invoked, or resolved at
consumer runtime.

## Why the separation

A skill is documentation a model reads and acts on. A stale skill is worse than no skill: it
encodes invariants that no longer hold, with the model's confidence behind them.

Keeping generated artifacts inside the repo they describe means they move when the code moves and
get reviewed in the same pull request. Keeping the *authoring* in a separate repo means the
conventions have one home rather than being duplicated and drifting across consumers.

## Artifact types

| Type | Format | Delivered to | Executable |
|---|---|---|---|
| Skill | `SKILL.md` + optional bundled scripts | `<consumer>/.claude/skills/` | no |
| Agent | agent definition markdown | `<consumer>/.claude/agents/` | no |
| MCP server | Python package | installed in consumer environment | yes |

Skills and agents are markdown. Only MCP servers involve code, which is why this repo is Python.

## Repository structure

MCP server code and skill content both live under `src/desk_organizer/`, per this template's
single-package convention (Architecture conventions 1/7 in `CLAUDE.md`). Skills are markdown, not
code, but they're packaged data all the same: [issue #2](https://github.com/croicu/desk-organizer/issues/2)'s
planned `desk-organizer pull-skills <target-repo>` CLI command needs to read a skill's content from
the *installed* package, not from a loose repo-root directory a consumer has no access to — so
skill content ships as `package-data` (see `pyproject.toml`'s `[tool.setuptools.package-data]`)
alongside the code that will eventually read it. Agent definitions have no content yet, but the
same reasoning will apply once they do.

```text
desk-organizer/
  pyproject.toml
  src/
    desk_organizer/
      cli.py
      diagnostics.py
      settings.py
      errors.py
      protocols.py
      contracts.py
      mcp/
        <server-name>/
      skills/
        skills.json
        <skill-name>/
          SKILL.md
      agents/
        <agent-name>.md
  tests/
```

`skills.json` declares which consumer repo(s) each skill applies to (see `docs/PROTOCOL.md`) — a
flat directory of skills plus this one manifest, rather than grouping skills into per-repo
subdirectories, so a skill can name more than one applicable repo without having to live in more
than one place.

## Modules

<!-- One entry per module under src/desk_organizer/: what it owns, what it depends on. -->

## Data flow

<!-- How data enters, gets transformed, and leaves the system. -->

## Contracts

<!-- protocols.py: public contracts -- persisted/shared data (pure data) plus behavioral Protocols
     meant for a consumer to implement/inject (e.g. LoggingSink, already scaffolded there).
     contracts.py: behavioral Protocols (Protocol classes) that wire this project's own internals
     together -- never imported by external consumers, unlike protocols.py's. -->

## Design principles

- authored artifacts, immutable once delivered
- consumers run independently of the author
- explicit/simple over clever
- markdown where markdown suffices
- installable over path-referenced
- no hidden coupling between author and consumer

## Status

Early. First deliverable is a single hand-written skill for the `geo-builder` / `geo-browser`
contract boundary, used to learn what a good skill contains before anything here generates one.
