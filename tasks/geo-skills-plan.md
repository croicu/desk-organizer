# Claude Skills for the geo ecosystem — context, goal, plan

## Context

### The repos

**geo-builder** (Python)
- Originally: pure offline pipeline. Raw photo metadata → filter/cluster/weight → immutable GeoJSON artifacts. No rendering, no API, no service.
- Now also: a design-mode host. Creates a WebView control, runs geo-browser inside it, exposes APIs to it, and receives user input back.
- **The README is stale.** It still describes the pure-pipeline design and explicitly states geo-builder does not render maps or host APIs. That is no longer true.
- Not deployed anywhere. Local only.

**geo-browser** (TypeScript, Vite, Leaflet, no frameworks)
- Static-first renderer. Deployed to Cloudflare Pages at `geo-browser.croicu.com`; data served from a separate origin, `geo-places.croicu.com`.
- Loads staged: `catalog.head.json` (cache-busted) → area manifest → layer GeoJSON on demand.
- Runs in two modes: **browse** (static hosting, state in `localStorage`) and **design** (hosted by geo-builder, state via the gateway).
- Virtual layers owned by the client, absent from the data contract: `__poi__`, `__user__`, `__void__`, `__search__`.

### Invariants that live at the seams

These are the things a model gets wrong confidently, and the reason a skill is worth writing:

1. **Coordinate order.** `AreaSpec.center` is `[latitude, longitude]`. GeoJSON coordinates are `[longitude, latitude]`. Same numbers, opposite order, no type distinction to catch it.
2. **Capability-based validation.** geo-browser treats payloads as open/unknown JSON. Producer emits stable, simple GeoJSON; consumer probes for what it needs. No schema enforcement, deliberately — the cost is deferred error detection, the benefit is no lockstep versioning across clients (geo-ios and geo-desktop don't exist yet).
3. **Dual-mode rendering.** Rendering must never assume browse vs design mode. Easy to violate quietly in an AI-assisted change.
4. **API surface additions.** Now that geo-builder exposes methods to the embedded page, what's the rule for adding one? Does the renderer degrade gracefully when a method is missing? This is capability-based validation again, moved from data to API.
5. **Static-first discipline.** No database, no backend, no framework. Explicit over clever. Deep linking is absent by design — the app is single-user, sharing isn't a scenario.

### Why this matters beyond the repos

The geo-builder/geo-browser boundary is a native host embedding a web renderer and brokering a governed API surface to it. That's structurally the same problem as Office extensibility over WebView2 — which is 15 years of prior work, rebuilt small. Encoding those invariants so an AI-assisted change can't silently break them is governance over an extensibility surface, which is the throughline worth being able to talk about.

---

## Goal

Hands-on understanding of **Claude Skills**: what a skill can hold, what it can't, and where encoded conventions beat inferred ones.

The output isn't a feature. It's a defensible observation about where explicit encoding changes model behavior and where it doesn't — the kind of thing that generalizes from two repos to an engineering org.

Secondary: a skill that's actually useful afterward.

---

## Constraints

- **Two days, a weekend.** Interview Monday 10:00 AM.
- **Skip MCP servers and subagents.** Both are interesting; neither fits the window. MCP is describable conceptually without having shipped one.
- Rested Monday matters more than a third deliverable.

---

## Plan

### Step 0 — Fix the geo-builder README (blocking)

A skill is documentation a model reads and acts on. Writing one from a stale description automates the wrong invariants.

Update it to reflect the WebView host role: what geo-builder now does, what the API surface is, how design mode relates to the static pipeline. Doesn't need to be polished — needs to be true.

### Step 1 — Write one skill

Start with geo-builder, since that's where the architecture moved.

Encode:
- The coordinate-order rule, stated as a rule with an example, not as prose
- Capability-based validation and *why* (so the model doesn't helpfully add schema validation)
- The API surface convention: how methods get added, how the renderer degrades when one is missing
- The "no database, no backend, no framework" constraints, as constraints rather than preferences

### Step 2 — Test it against real changes

Make 3–4 actual changes with the skill loaded. Deliberately include:
- Something that touches coordinates in both conventions
- Something that adds or changes an API method
- Something where the tempting move is to add validation

Watch for: what the skill caught, what it ignored, what had to be made explicit that seemed obvious, whether stating the *reason* behind a rule changed adherence versus stating the rule alone.

### Step 3 — Only if it's flowing

A second skill for geo-browser, or a seam skill covering the boundary itself. Not required. One repo done properly is enough.

---

## What to capture along the way

Notes for the observation, not the code:

- Where did the skill change behavior, and where did the model do the right thing anyway?
- Which invariants needed the rationale attached to stick?
- What's the failure mode when a skill is wrong or stale — worse than no skill, or just neutral?
- How would this scale to 100 repos with different owners? What breaks?

That last question is the interview answer.
