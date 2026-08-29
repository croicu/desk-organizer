# geo-organizer

geo-organizer is the organizer tool for the geo ecosystem's AI tooling. It generates Claude Code skills, agent definitions, and MCP servers that are consumed by geo-builder and geo-browser.

Consumers run independently. Generated artifacts are copied into each target repo's .claude/ directory and version with that repo. The organizer repo does not need to be present — or even exist on the same machine — for a consumer to use what it produced.

This repo owns: skill and agent organizer, MCP server implementation, the conventions for deriving invariants from a producer/consumer boundary.

This repo does not: execute skills, read consumer source at runtime, or participate in any consumer's build.

Python. Markdown artifacts, packaged distribution for anything executable.

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
