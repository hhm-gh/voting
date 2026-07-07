	# US / Colorado / Denver Voting & Demographics Project — Overview

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
  logistics like polling place capacity, not politics).
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
- [ ] Identify and download authoritative boundary files (shapefile/GeoJSON)
      for CDs, SDs, HDs, precincts, and Denver council districts — for at
      least the current cycle, ideally also prior cycles for comparison
- [ ] Identify and download historical election results at the most granular
      level available (precinct-level where possible) for target races
- [ ] Set up a project structure/repo scaffolding (data directory conventions,
      a lightweight tech stack decision — e.g., Python + GeoPandas + a
      Postgres/PostGIS or DuckDB backend)
- [ ] Establish a raw-data vs. processed-data convention, with provenance
      notes (source, retrieval date, license) for everything ingested

### Phase 2 — Core Data Model
- [ ] Define a normalized schema linking: election → office → geography →
      result (votes by candidate/party)
- [ ] Build the geography crosswalk layer (precinct ↔ CD/SD/HD ↔ county ↔
      Census tract/block), handling boundary changes across redistricting cycles
- [ ] Load a first end-to-end vertical slice: e.g., Denver + Colorado results
      for a single recent election cycle, joined to boundaries

### Phase 3 — Demographics Integration
- [ ] Pull ACS demographic data (population, race/ethnicity, age, income,
      education) at Census tract/block group level
- [ ] Build the demographic-to-voting-geography crosswalk (areal
      interpolation or block-level apportionment)
- [ ] Produce first joined dataset: demographics + results by precinct/district

### Phase 4 — Analysis & Visualization
- [ ] Basic descriptive analysis: turnout, vote share trends over time by
      geography
- [ ] Redistricting/gerrymandering metrics: compactness, partisan symmetry,
      efficiency gap, comparison across map proposals if available
- [ ] Mapping/visualization layer (e.g., choropleth maps of results/demographics)

### Phase 5 — Forecasting / Trend Analysis (long-term)
- [ ] Explore models connecting demographic shifts to electoral outcome shifts
- [ ] Scenario analysis under alternative district maps

## Status

Phase 0 documentation is complete (`docs/geography.md`, `docs/redistricting.md`,
`docs/offices.md`). Project still has no code. Next concrete step is Phase 1:
identifying and acquiring authoritative boundary files and historical
election results data.
