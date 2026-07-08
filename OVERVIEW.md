	# US / Colorado / Denver Voting & Demographics Project — Overview

## Table of Contents

- [[#Purpose]]
- [[#Elections of Primary Interest]]
- [[#Geographic Units — Glossary (to be expanded)|Geographic Units — Glossary]]
- [[#Architecture: Python retrieval/storage, R analysis/viz]]
  - [[#Storage format]]
- [[#Data Sources (to be vetted/expanded)|Data Sources]]
- [[#Phased Plan]]
  - [[#Phase 0 — Documentation (current phase)|Phase 0 — Documentation]]
  - [[#Phase 1 — Foundation / Data Acquisition]]
  - [[#Phase 2 — Core Data Model]]
  - [[#Phase 3 — Demographics Integration]]
  - [[#Phase 4 — Analysis & Visualization]]
  - [[#Phase 5 — Forecasting / Trend Analysis (long-term)|Phase 5 — Forecasting / Trend Analysis]]
- [[#Status]]

## Purpose

Build the ability to analyze voting behavior, election outcomes, and demographics
across US geography, using **Colorado** (state-level) and **Denver** (local-level)
as the concrete test cases for developing tools, data pipelines, and analysis
methods that could eventually generalize to other states/localities.

Long-term goal: connect detailed demographic data to past and future elections
to understand and predict political trends.

Near-term goal: document how the election system itself is structured — the
geographic units, the offices, the redistricting process — and lay out a
concrete, staged plan for building the data/tooling foundation.

## Elections of Primary Interest

In roughly descending scope:

1. **US President** — via the Electoral College (Colorado's electors, allocation rules)
2. **US Congress** — US Senate (statewide) and US House (Colorado's 8 congressional districts)
3. **State Governor** — statewide executive
4. **State Legislature** — Colorado State Senate (35 districts) and State House (65 districts)
5. **Denver City Council** — 11 districts (13 members: 11 district + 2 at-large), plus Denver Mayor/Clerk & Recorder as relevant local context

Gerrymandering and redistricting mechanics are a cross-cutting topic of interest
across levels 2–5 (Congress, State House/Senate, and to a lesser extent Council
districts).

## Geographic Units — Glossary (to be expanded)

The election system layers several distinct kinds of geography, each drawn for
a different purpose and by a different authority. This is the core confusion
to resolve first. Rough hierarchy from smallest/most granular to largest:

- **Precinct** — smallest voting unit; where individual votes are tallied.
  Drawn/maintained by county election officials. Precincts nest inside every
  other district type below but are redrawn independently of them (for
  logistics like polling place capacity, not politics). Messy to source
  (no single clean statewide feed) and not needed for the early phases of
  this project — district/county-level results suffice until we reach
  gerrymandering metrics and the demographics crosswalk (Phase 3/4). See
  [`docs/data-sources.md`](docs/data-sources.md#precincts-deferred--phase-34-not-phase-1).
- **Congressional District (CD)** — US House seats; Colorado has 8. Redrawn
  every 10 years post-Census. Since 2021, Colorado uses an independent
  redistricting commission (Amendment Y, 2018) rather than the legislature.
- **State Senate District (SD)** — 35 districts, 4-year terms, staggered.
- **State House District (HD)** — 65 districts, 2-year terms.
  State legislative districts also redrawn each decade (Amendment Z, 2018,
  created the parallel independent commission for these).
- **County** — Colorado has 64 counties; Denver is unique as a consolidated
  city-county. Counties administer elections (ballots, precincts, canvassing).
- **Denver City Council District** — 11 districts for city council members,
  redrawn by the city (not the state commissions) after each Census.
- **School District / Special Districts** — (e.g., Denver Public Schools)
  relevant for down-ballot elections but lower near-term priority.
- **Census Geography** (tracts, block groups, blocks) — not a voting
  geography per se, but the backbone for demographic data (ACS, decennial
  Census) that later needs to be crosswalked onto the voting geographies
  above. This crosswalk is one of the harder technical problems in this
  project (boundaries don't nest cleanly).

Open questions to resolve during the documentation phase:
- Exact redistricting timeline/process for each commission (Y vs Z) and how
  public map submissions/criteria work.
- How precinct boundaries relate to (are they subsets of?) CD/SD/HD boundaries.
- Where to source authoritative, versioned boundary files (shapefiles/GeoJSON)
  for each geography, per election cycle (boundaries change over time!).

## Architecture: Python retrieval/storage, R analysis/viz

**Design constraint:** data retrieval and storage are strictly separated
from analysis and visualization, along a language boundary:

- **Python** owns everything that touches the network or writes data:
  downloading boundary files and election results, parsing/normalizing them,
  building the geography crosswalk, and writing the result to `data/`.
- **R** owns analysis and visualization: it only *reads* from `data/` and
  never fetches anything itself.
- Data flow is **one-way**: Python writes → `data/` → R reads. Nothing in R
  should require network access or write back into `data/`.

This mirrors the existing pattern in `~/code/energy` (Python `eia/` package
downloads to Parquet in `data/`; the R/Shiny app in `r/` reads it via
`arrow::read_parquet()` and never calls the network) — reusing a convention
already proven to work rather than inventing a new one.

### Storage format

- **Tabular data** (election results, demographics, crosswalk tables):
  **Parquet** — consistent with every other data project in `~/code`
  (`energy`, `housing`, `co-data` all use it). Both `pandas`/`pyarrow` and R's
  `arrow` package read it natively, no server process required.
- **Geometry/boundary data** (CD/SD/HD/council/precinct/Census shapes):
  `scripts/process_phase1_boundaries.py` writes **both** GeoParquet and
  GeoPackage for every dataset, and `r/load.R`'s `load_boundary()` tries
  GeoParquet first, falling back to GeoPackage on error — this was written
  to get an empirical answer rather than guess. **Result (tested
  2026-07-08): GeoParquet reads fail in R and it falls back to GeoPackage
  every time.** Root cause confirmed via `sf::sf_extSoftVersion()`: R's `sf`
  package links its own statically-bundled GDAL 3.8.5 (independent of
  whatever GDAL is on the system `PATH` — this machine's Homebrew GDAL is
  3.13.1 and does have a Parquet driver, but that's irrelevant, `sf` never
  sees it), and `sf::st_drivers()` confirms that bundled 3.8.5 build has
  zero Parquet drivers registered. **So: GeoPackage (`.gpkg`) is the
  format that actually works for R today, not GeoParquet** — keep writing
  both (GeoParquet costs nothing extra and may pay off once `sf`'s bundled
  GDAL catches up), but treat GeoPackage as primary for anything the R side
  needs to read now.
- **Raw downloads stay untouched** in `data/raw/` in whatever format the
  source actually provides — mostly **Shapefile** and some **KML** for
  boundaries (see [`docs/data-sources.md`](docs/data-sources.md)); these are
  legitimate native GIS formats, fine to keep as the unmodified source-of-
  truth copy, just not what we build the working pipeline on top of. Python
  converts raw → `data/processed/` in the formats above. This is the
  raw-vs-processed provenance convention referenced in Phase 1 below.
- **No server-based database** (Postgres/PostGIS) for now — this is a
  solo, local, non-concurrent project, so file-based Parquet/GeoParquet is
  enough. `DuckDB` (with its `spatial` extension) is worth reaching for
  later if cross-file SQL querying gets useful — it can query Parquet/
  GeoParquet files in place without a separate load step, as already used
  in `~/code/co-data` — but it's an optional convenience layer, not a
  replacement for the file-based storage above.

## Data Sources (to be vetted/expanded)

- **Colorado Secretary of State** — election results, redistricting commission data
- **Denver Elections Division** — city election results, council district maps
- **US Census Bureau** — TIGER/Line shapefiles, ACS demographic data, decennial Census
- **Redistricting Data Hub / Census Redistricting Data Program (P.L. 94-171)**
- **MIT Election Data and Science Lab (MEDSL)** — historical federal/state election results
- **OpenElections project** — precinct-level historical results

## Phased Plan

### Phase 0 — Documentation (current phase)
- [x] Capture this overview
- [x] Write a dedicated `docs/geography.md` detailing each geographic unit,
      its authority, redraw cadence, and current Colorado/Denver specifics
      (includes `docs/geography.excalidraw.md` diagram of how the pieces relate)
- [x] Write `docs/redistricting.md` detailing Colorado's independent
      commission process (Amendments Y & Z) and general gerrymandering concepts
      (e.g., efficiency gap, compactness measures)
- [x] Write `docs/offices.md` cataloging each office of interest (term length,
      how elected, current officeholder as of a snapshot date)

### Phase 1 — Foundation / Data Acquisition
- [x] Identify authoritative boundary file *sources* (shapefile/GeoJSON) for
      CDs, SDs, HDs, precincts, counties, and Denver council districts — see
      [`docs/data-sources.md`](docs/data-sources.md). Precinct *acquisition*
      is deferred to Phase 3/4 (see that doc's Sequencing section) — it's
      the messiest geography to source and isn't needed until the
      gerrymandering metrics and demographics crosswalk work.
- [x] Download boundary files for a first working cycle (CD, SD, HD, county,
      Denver council — current 2021 maps) via `scripts/fetch_phase1_boundaries.py`
      into `data/raw/` (gitignored — not committed). Prior cycles for
      comparison still TODO.
- [ ] Identify and download historical election results at district/county
      level for target races (precinct-level results deferred to Phase 3/4
      alongside precinct boundaries)
- [x] Set up project scaffolding per the
      [[#Architecture: Python retrieval/storage, R analysis/viz]] above, and
      smoke-test it end-to-end before adding election results:
      `scripts/process_phase1_boundaries.py` converts every `data/raw/`
      boundary file to `data/processed/<name>/<cycle>/boundaries.{geoparquet,gpkg}`
      (reprojected to `EPSG:4326`; counties filtered to `STATEFP == '08'`).
      `r/` is a full RStudio project (`renv`-managed) with `load.R` and
      `smoketest.R`, which loads all 5 processed datasets, checks feature
      counts (8/35/65/64/13 — all correct) and that each bbox falls inside
      Colorado's real extent, and plots each to `r/output/*.png`. Visually
      confirmed the congressional and Denver plots are recognizably correct
      (Colorado's outline with 8 CDs; Denver's shape including the DIA
      panhandle). This also empirically resolved the GeoParquet-vs-
      GeoPackage question — see
      [[#Storage format]] above.
- [x] Establish a raw-data vs. processed-data convention, with provenance
      notes (source, retrieval date, license) — each `data/raw/<dataset>/<cycle>/`
      directory now has a `provenance.json` sidecar (source page URL, license,
      retrieval timestamp, per-file size) written automatically by the fetch
      script

### Phase 2 — Core Data Model
- [ ] Define a normalized schema linking: election → office → geography →
      result (votes by candidate/party)
- [ ] Build the geography crosswalk layer (precinct ↔ CD/SD/HD ↔ county ↔
      Census tract/block), handling boundary changes across redistricting cycles
- [ ] Load a first end-to-end vertical slice: e.g., Denver + Colorado results
      for a single recent election cycle, joined to boundaries

### Phase 3 — Demographics Integration
- [ ] Acquire precinct boundaries + results (deferred from Phase 1 — see
      [`docs/data-sources.md`](docs/data-sources.md#precincts-deferred--phase-34-not-phase-1))
      and Census tract/block group/block boundaries
- [ ] Pull ACS demographic data (population, race/ethnicity, age, income,
      education) at Census tract/block group level
- [ ] Build the demographic-to-voting-geography crosswalk (areal
      interpolation or block-level apportionment) — this is the primary
      reason precinct-level results are needed: they're the finest
      resolution real votes exist at, and don't nest cleanly into Census
      geography
- [ ] Produce first joined dataset: demographics + results by precinct/district

### Phase 4 — Analysis & Visualization
- [ ] Basic descriptive analysis: turnout, vote share trends over time by
      geography (district/county level is sufficient here)
- [ ] Redistricting/gerrymandering metrics: compactness, partisan symmetry,
      efficiency gap, comparison across map proposals if available — these
      require precinct-level results as the sub-district unit to
      re-aggregate (district totals alone can't be tested against
      alternative maps); see
      [`docs/redistricting.md`](docs/redistricting.md#gerrymandering-vocabulary--metrics)
- [ ] Mapping/visualization layer (e.g., choropleth maps of results/demographics)

### Phase 5 — Forecasting / Trend Analysis (long-term)
- [ ] Explore models connecting demographic shifts to electoral outcome shifts
- [ ] Scenario analysis under alternative district maps

## Status

Phase 0 documentation is complete (`docs/geography.md`, `docs/redistricting.md`,
`docs/offices.md`). Phase 1 is well underway: boundary file sources are
documented (`docs/data-sources.md`), the current-cycle (2021)
CD/SD/HD/county/Denver council boundary files are downloaded to `data/raw/`
(gitignored) via `scripts/fetch_phase1_boundaries.py`, and the full
Python-processing + R-viz pipeline is built and smoke-tested end-to-end
(`scripts/process_phase1_boundaries.py` → `data/processed/` →
`r/smoketest.R` → `r/output/*.png`, all verified correct) — this is the
project's first R code and its first real Python→R vertical-slice test,
ahead of Phase 2's planned one. Remaining Phase 1 work: historical election
results and prior-cycle boundaries.
