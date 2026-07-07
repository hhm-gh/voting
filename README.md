# Voting & Geography Analysis — Colorado / Denver

Building the ability to analyze US voting behavior, election outcomes, and
demographics — using Colorado (state-level) and Denver (local-level) as the
concrete working examples, with an eventual goal of connecting demographics
to election trends past and future.

See [`OVERVIEW.md`](OVERVIEW.md) for the full goals, scope, and phased plan.

## What's in here

**Docs (Phase 0 — complete):**

| Doc | Covers |
|---|---|
| [`OVERVIEW.md`](OVERVIEW.md) | Project goals, elections in scope, phased plan |
| [`docs/geography.md`](docs/geography.md) | Precincts, congressional/state legislative/council districts, counties, Census geography, and how they relate |
| [`docs/geography.excalidraw.md`](docs/geography.excalidraw.md) | Diagram of the geography hierarchy above (Obsidian Excalidraw format) |
| [`docs/redistricting.md`](docs/redistricting.md) | Colorado's independent redistricting commissions (Amendments Y & Z), and gerrymandering metrics (efficiency gap, compactness, etc.) |
| [`docs/offices.md`](docs/offices.md) | Office-by-office catalog: US President through Denver City Council — term lengths, election method, current officeholders |

**Elections in scope:** US President (Electoral College) → US Congress
(Senate + Colorado's 8 House districts) → Colorado Governor → Colorado State
Senate/House → Denver City Council.

## Status

Phase 0 (documentation) is complete. No data pipeline or analysis code
exists yet. Next up is Phase 1: identifying and acquiring authoritative
district boundary files and historical election results data.

See the [Phased Plan](OVERVIEW.md#phased-plan) in `OVERVIEW.md` for the full
roadmap (Documentation → Data Acquisition → Core Data Model → Demographics
Integration → Analysis/Visualization → Forecasting).
