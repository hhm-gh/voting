# Boundary File Sources — Colorado / Denver

Phase 1 deliverable: where to get authoritative boundary files (shapefile /
GeoJSON) for each geography in [`geography.md`](geography.md). This doc
covers *boundaries only* — election results sourcing is a separate pass.

## Quick reference

Ordered by when we actually need each one — see
[Sequencing: what's needed when](#sequencing-whats-needed-when) below for the
reasoning behind the Priority column.

| Geography | Primary source | Format | Historical cycles? | Priority |
|---|---|---|---|---|
| Congressional District (CD) | [Colorado Redistricting Commission](https://redistricting.colorado.gov/content/congressional-final-approved) | Shapefile, block assignment file, KML | Current cycle only (2021 maps); pre-2021 via Census TIGER by vintage year | Phase 1 |
| State Senate District (SD) | [Colorado Redistricting Commission](https://redistricting.colorado.gov/content/senate-final-approved) | Shapefile, block assignment file, KML | Same as above | Phase 1 |
| State House District (HD) | [Colorado Redistricting Commission](https://redistricting.colorado.gov/content/house-final-approved) | Shapefile, block assignment file, KML | Same as above | Phase 1 |
| County | [Census TIGER/Line — Counties](https://www.census.gov/cgi-bin/geo/shapefiles/index.php) | Shapefile | Static (64 counties, essentially unchanged) | Phase 1 |
| Denver City Council District | [Denver Open Data Catalog](https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-council-districts) | Shapefile, GeoJSON, KML, CSV | Current cycle; check catalog for prior versions | Phase 1 |
| Census Tract / Block Group / Block | [Census TIGER/Line](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html) | Shapefile | By vintage year, back to 2000s | Deferred — Phase 3 |
| Precinct | [Colorado Geospatial Portal](https://geodata.colorado.gov/datasets/fedmaps::voting-districts-2/about) (statewide) or individual counties | Shapefile / feature layer | Inconsistent — see caveat below | Deferred — Phase 3/4 |

## Congressional / State Senate / State House Districts

**Source:** Colorado Independent Redistricting Commissions site, `redistricting.colorado.gov`. This is the authoritative source for the maps actually in effect — approved by the Colorado Supreme Court on March 18, 2022, after the commissions' 2021 process (see [`redistricting.md`](redistricting.md)).

- Congressional: https://redistricting.colorado.gov/content/congressional-final-approved
- State Senate: https://redistricting.colorado.gov/content/senate-final-approved (an errata/corrected version also exists: `senate-final-approved-errata`)
- State House: https://redistricting.colorado.gov/content/house-final-approved

Each page provides:
- A shapefile (`2021_Approved_*_Plan_w_Final_Adjustments.zip`)
- A block assignment file (`.txt` — maps Census blocks to district IDs, useful for the demographic crosswalk in Phase 3)
- KML/KMZ for quick viewing in Google Earth

**Caveat:** these are *only* the current (2021–2030) cycle. For pre-2021 district boundaries (needed to line up historical election results with the map that was in effect at the time), use Census TIGER/Line CD/SLDU/SLDL shapefiles filtered to the relevant vintage year — TIGER re-publishes these annually and older vintages remain archived at `www2.census.gov/geo/tiger/TIGER<year>/`.

## Denver City Council Districts

**Source:** Denver Open Data Catalog.

- Dataset page: https://www.denvergov.org/opendata/dataset/city-and-county-of-denver-council-districts
- Catalog home (for browsing related layers — precincts, neighborhoods, etc.): https://www.denvergov.org/opendata or https://opendata-geospatialdenver.hub.arcgis.com/
- Formats offered: Shapefile, GeoJSON, KML, CSV, plus live API access (GeoServices/WMS/WFS) if we want to query rather than download.

## Counties

Static and low-priority to source carefully — Census TIGER/Line county boundaries are authoritative and simplest:

- https://www.census.gov/cgi-bin/geo/shapefiles/index.php — select year, layer group "Counties", then Colorado.
- Cartographic Boundary (CB) files are a generalized, simplified alternative to full TIGER/Line — smaller file size, better for visualization/mapping where full topological precision isn't needed: https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html. Use CB for maps/visualization (Phase 4), TIGER/Line proper for anything requiring precise boundaries (crosswalks, spatial joins).

## Census Geography (Tract / Block Group / Block)

**Source:** Census TIGER/Line, same portal as above, layer groups "Census Tracts," "Block Groups," "Blocks" — select vintage year and Colorado.

- https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
- Needed for Phase 3 (demographics crosswalk); not urgent for Phase 1.

## Precincts (deferred — Phase 3/4, not Phase 1)

**This is the messiest geography to source** — precincts are drawn and
maintained per-county, not by the state, so there's no single clean
statewide feed guaranteed current. Rather than pay that sourcing cost now,
we're deferring precinct acquisition until it's actually load-bearing for
the work. See [Sequencing](#sequencing-whats-needed-when) below for why
this doesn't block Phase 1/2.

### Why precinct granularity matters (when it does)

Precinct-level data is the atomic unit of *actual cast votes* — smaller
than a district, but (unlike Census blocks) still tied to real election
results rather than population counts. It becomes necessary for two things
this project's plan already anticipates, and isn't generally useful before
that:

1. **Gerrymandering detection (Phase 4).** District-level results are the
   *thing being tested*, so district totals alone can't evaluate them
   against alternatives — there's nothing smaller to reshuffle. Techniques
   like efficiency gap / packing-cracking analysis need to see where votes
   actually clustered *before* district lines were drawn through them.
   Redistricting ensemble simulation (the MGGG Redistricting Lab's
   `GerryChain` toolkit — used as expert-witness evidence in *Gill v.
   Whitford*, *League of Women Voters v. Pennsylvania*, and North Carolina's
   gerrymandering suits) generates thousands of alternative valid maps and
   compares the enacted map's partisan lean to that distribution, which
   requires an atomic sub-district unit to re-aggregate. See the
   [gerrymandering vocabulary in `redistricting.md`](redistricting.md#gerrymandering-vocabulary--metrics)
   for the specific metrics this feeds.
2. **Demographics crosswalk (Phase 3).** Precincts don't nest inside Census
   tracts/blocks, but precinct-level *results* are the finest resolution
   real votes exist at. Answering "how did majority-Latino precincts vote"
   needs precinct (or block-interpolated) results — this is also the basis
   for VRA Section 2 racially-polarized-voting analysis (ecological
   inference), directly relevant given the *Callais* ruling narrowing
   Section 2 (see [`redistricting.md`](redistricting.md#national-context-20252026-the-mid-decade-redistricting-wave)).

Historically, this granularity is also what newsroom "how did your
neighborhood vote" interactive maps use (NYT/WaPo, standard since ~2016)
and what campaigns use for micro-targeting/GOTV — neither relevant to this
project's goals.

**What doesn't need precinct data:** Phase 1–2's vertical slice (results
joined to CD/SD/HD/council boundaries) and Phase 4's basic turnout/
vote-share-trend descriptive work are fine with district- or county-level
results — that's the level Colorado SoS already reports cleanly, and the
level these offices are actually decided at.

### Sourcing options, once needed

Options, roughly best-to-worst for a first pass:

1. **Colorado Geospatial Portal — Voting Districts layer**: https://geodata.colorado.gov/datasets/fedmaps::voting-districts-2/about — mirrors Census TIGER voting district (VTD) data, refreshed weekly. Good default for a statewide first cut.
2. **Colorado State Demographer's Office**, via the [mggg-states/CO-shapefiles](https://github.com/mggg-states/CO-shapefiles) GitHub repo — precinct shapefile with 2018 election results already joined, compiled by Colorado College researchers from Demographer's Office + Secretary of State data. Good for a known-good historical snapshot (2018), not current-cycle precincts.
3. **Redistricting Data Hub** (https://redistrictingdatahub.org/state/colorado/) — precinct boundaries pre-joined with election results for 2016, 2018, 2020, 2022, and (in progress) 2024, sourced from VEST and the CO Secretary of State. Requires free registration. Likely the best source when we get here, since it saves us the geography↔results join ourselves.
4. **Individual county GIS portals** — for the counties the RDH/state notes as having been digitized separately from county-supplied maps rather than the Demographer's aggregate (Boulder, Denver, Douglas, El Paso called out explicitly). Denver's own precincts should come from the Denver Open Data Catalog above rather than the statewide layer, for accuracy.

**Open question to resolve when we get here:** whether the statewide Voting
Districts layer is precinct-accurate for Denver specifically, or whether we
need to swap in Denver's own precinct file.

## Sequencing: what's needed when

- **Phase 1 (now):** CD, SD, HD, county, and Denver council boundaries —
  current cycle (2021 maps) only, joined to district/county-level results.
  This is everything needed for the Phase 1–2 vertical slice.
- **Phase 3:** Census tract/block group/block boundaries, plus precinct
  boundaries + results, for the demographics crosswalk.
- **Phase 4:** Precinct-level results specifically feed the gerrymandering
  metrics (efficiency gap, ensemble simulation) — see
  [why precinct granularity matters](#why-precinct-granularity-matters-when-it-does)
  above.

## General notes

- All the redistricting-commission and Census files are **by vintage/cycle year** — always record which year's boundaries a given dataset uses, since CD/SD/HD boundaries changed in 2021 and precinct boundaries can change more often. This is the "provenance" convention called for in `OVERVIEW.md` Phase 1.
- Redistricting Data Hub is worth prioritizing once we reach precinct acquisition (Phase 3/4), since it bundles boundaries + results and avoids a manual join.

## Next steps

- [ ] Pick a single current-cycle vintage (likely 2021 maps, most recent election) and download CD/SD/HD/county boundaries for a first vertical slice.
- [ ] Move on to sourcing historical election results at district/county level (separate doc/pass).
- [ ] *(Deferred to Phase 3/4)* Resolve the Denver precinct-source open question and register for a Redistricting Data Hub account when precinct acquisition actually starts.
