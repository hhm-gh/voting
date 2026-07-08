# Voting & Geography Analysis — Colorado / Denver

Building the ability to analyze US voting behavior, election outcomes, and
demographics — using Colorado (state-level) and Denver (local-level) as the
concrete working examples, with an eventual goal of connecting demographics
to election trends past and future.

See [`OVERVIEW.md`](OVERVIEW.md) for the full goals, scope, and phased plan.

## What's in here

**Docs:**

| Doc | Covers |
|---|---|
| [`OVERVIEW.md`](OVERVIEW.md) | Project goals, elections in scope, phased plan, architecture |
| [`docs/geography.md`](docs/geography.md) | Precincts, congressional/state legislative/council districts, counties, Census geography, and how they relate |
| [`docs/geography.excalidraw.md`](docs/geography.excalidraw.md) | Diagram of the geography hierarchy above (Obsidian Excalidraw format) |
| [`docs/redistricting.md`](docs/redistricting.md) | Colorado's independent redistricting commissions (Amendments Y & Z), gerrymandering metrics, and the 2025–2026 national mid-decade redistricting wave |
| [`docs/offices.md`](docs/offices.md) | Office-by-office catalog: US President through Denver City Council — term lengths, election method, current officeholders |
| [`docs/data-sources.md`](docs/data-sources.md) | Where district boundary files come from, per geography, with an acquisition log |
| [`docs/election-results-sources.md`](docs/election-results-sources.md) | Where historical election results come from, per office, with an acquisition log |

**Code:**

| Path | Covers |
|---|---|
| `scripts/fetch_phase1_boundaries.py` | Downloads CD/SD/HD/county/Denver council boundaries to `data/raw/` |
| `scripts/process_phase1_boundaries.py` | Converts raw boundaries to `data/processed/` (GeoParquet + GeoPackage, reprojected, Colorado-filtered) |
| `scripts/fetch_election_results.py` | Downloads historical election results to `data/raw/election_results/` |
| `r/` | RStudio project (`renv`-managed) — `load.R`, `smoketest.R` (visual sanity checks), `explore.R` (interactive `mapview` exploration) |

**Elections in scope:** US President (Electoral College) → US Congress
(Senate + Colorado's 8 House districts) → Colorado Governor → Colorado State
Senate/House → Denver City Council.

## Status

Phase 0 (documentation) is complete. Phase 1 (data acquisition) is well
underway: boundary files for the current (2021) cycle are downloaded and
verified, the Python-processing + R-viz pipeline is built and smoke-tested,
and election-results sourcing has started (US President 2000–2016
downloaded; several other sources identified but not yet acquired — see
`docs/election-results-sources.md`).

See the [[OVERVIEW#Phased Plan|Phased Plan]] in `OVERVIEW.md` for the full
roadmap (Documentation → Data Acquisition → Core Data Model → Demographics
Integration → Analysis/Visualization → Forecasting).

---

**Note on internal links:** this repo lives inside an Obsidian vault
(`~/code`), so links to headings use Obsidian wikilink syntax
(`[[File#Heading]]`) rather than plain Markdown anchors (`[text](#anchor)`)
— the latter don't reliably resolve in Obsidian. See `~/code/CLAUDE.md` for
the full writeup. Wikilinks won't render as clickable links on GitHub.
