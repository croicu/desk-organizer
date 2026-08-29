# ARCHITECTURE.md

Modules, data flow, and contracts for `geo-organizer`. See `CLAUDE.md`'s `## Mission` for the
one-paragraph summary this document expands on.

## Ownership

### geo-organizer owns

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
geo-organizer
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

MCP server code lives under `src/geo_organizer/` per this template's single-package convention
(Architecture conventions 1/7 in `CLAUDE.md`). Skill and agent content is markdown, not code, so
it lives at the repo root rather than under `src/`.

```text
geo-organizer/
  pyproject.toml
  src/
    geo_organizer/
      cli.py
      diagnostics.py
      settings.py
      errors.py
      protocols.py
      contracts.py
      mcp/
        <server-name>/
  skills/
    <skill-name>/
      SKILL.md
  agents/
    <agent-name>.md
  tests/
```

## Modules

<!-- One entry per module under src/geo_organizer/: what it owns, what it depends on. -->

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
