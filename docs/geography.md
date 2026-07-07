# Election & Census Geography — Colorado / Denver

This doc explains the different geographic units that show up when working
with US elections, why there are so many of them, and how they relate to
each other in Colorado specifically. It expands on the glossary in
[`../OVERVIEW.md`](../OVERVIEW.md).

## Diagram

See [`geography.excalidraw.md`](geography.excalidraw.md) — this is authored
directly in the [Obsidian Excalidraw plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin)'s
native format, so it opens cleanly in Obsidian (switch to Excalidraw view via
the file's "more options" menu). To view it outside Obsidian (e.g.
excalidraw.com or the
[Excalidraw VS Code extension](https://marketplace.visualstudio.com/items?itemName=pomdtr.excalidraw-editor)),
use the plugin's command palette action "Export Excalidraw" (or "Decompress
current Excalidraw file") to get a plain `.excalidraw` JSON copy first — a
bare `.excalidraw` file placed in an Obsidian vault gets auto-converted to
this `.md` wrapper format on open, so that's not a viable long-term storage
format here.

It shows two largely independent hierarchies that meet only through an
imperfect crosswalk:

- **Voting/administrative geography**: State → Counties (Denver is a
  consolidated city-county) → **Precincts** → four *different* district maps
  that each aggregate precincts on their own terms (Congressional, State
  Senate, State House, Denver Council).
- **Census/demographic geography**: Tract → Block Group → Block.

The key visual point: precincts are the atomic voting unit, and every
higher-level *voting* district (CD/SD/HD/Council) is just a different way of
grouping the same precincts. Census geography is drawn independently for
statistical purposes and has to be cross-walked onto precincts/districts —
it does not nest cleanly.

## Why so many overlapping geographies?

Each geography is drawn by a different authority, for a different purpose,
on a different schedule:

| Geography | Purpose | Drawn by | Redraw cadence |
|---|---|---|---|
| Precinct | Administer voting (ballots, polling places, tabulation) | County election officials (Denver Elections Division for Denver) | As needed (population shifts, polling logistics); can change most years |
| Congressional District (CD) | Elect US House members | Independent redistricting commission (est. by Amendment Y, 2018) | Every 10 years, post-Census |
| State Senate District (SD) / State House District (HD) | Elect state legislators | Independent redistricting commission (est. by Amendment Z, 2018) | Every 10 years, post-Census |
| County | General government + election administration | Fixed by state constitution/statute | Essentially static (64 counties) |
| Denver City Council District | Elect city council members | Denver's own charter-mandated process (city council / commission per city charter) | Every 10 years, post-Census |
| Census Tract / Block Group / Block | Statistical reporting of demographics | US Census Bureau | Every 10 years (decennial), tracts/blocks redefined; block groups derived from blocks |

Because each geography answers to a different clock and a different
authority, **a precinct's boundary, a CD's boundary, and a Census tract's
boundary are all independently drawn and don't line up** — which is exactly
why a "crosswalk" step is needed to combine data across them (see Phase 2/3
of the [overview plan](../OVERVIEW.md#phased-plan)).

## Geography reference

### Precinct
The smallest unit of election administration. All votes are tallied at the
precinct level before being aggregated upward. In Colorado, precincts are
established and maintained by county clerks (for Denver: the Denver
Elections Division, since Denver is both a city and a county). Precincts are
sized for polling logistics (historically ~ a few thousand voters), not for
political balance — although in the mail-ballot era (Colorado is an
all-mail-ballot state), precincts matter more for results-reporting
geography than for physical polling places.

Every other voting district (CD, SD, HD, county commissioner district,
Denver council district) is built by assigning whole precincts to that
district — precincts are not usually split between two districts of the
same type, which is what makes them the natural "atomic unit" for
redistricting and for joining election results to district boundaries.

### Congressional District (CD)
Colorado currently has **8 US House seats** (gained the 8th after the 2020
Census). Boundaries are redrawn once per decade by Colorado's independent
Congressional Redistricting Commission, created by **Amendment Y (2018)**,
which took the process away from the state legislature. The commission must
satisfy criteria in a specified priority order: constitutional/Voting Rights
Act compliance, equal population, contiguity, then preserving communities of
interest, compactness, and competitiveness — with an explicit prohibition on
drawing maps to protect incumbents or a party.

### State Senate District (SD) / State House District (HD)
- **State Senate**: 35 districts, 4-year terms, staggered so roughly half
  are up for election each cycle.
- **State House**: 65 districts, 2-year terms, all up every cycle.

Both are redrawn once per decade by Colorado's independent Legislative
Redistricting Commission, created by the companion **Amendment Z (2018)**,
with similar criteria to Amendment Y's congressional commission.

### County
Colorado has **64 counties**. Counties are the operational backbone of
election administration (issuing ballots, maintaining precincts, canvassing
results) regardless of what districts overlay them. **Denver is a
consolidated city-county** — the only fully consolidated city-county in
Colorado — meaning the City and County of Denver are the same legal entity
and the same election authority handles both municipal and state/federal
elections for Denver residents.

### Denver City Council District
Denver's City Council has **13 members: 11 elected from single-member
districts + 2 at-large**. Council district boundaries are redrawn every 10
years following the decennial Census, through a process defined in the
Denver City Charter (distinct from — and independent of — the state's
Amendment Y/Z commissions, which only cover congressional and state
legislative maps).

### Census geography (Tract / Block Group / Block)
Not a voting geography at all — it's the US Census Bureau's statistical
geography, used to report demographic data (population, race/ethnicity,
age, income, education via the decennial Census and the American Community
Survey). It nests cleanly *within itself* (Blocks roll up into Block Groups,
which roll up into Tracts) but has no required relationship to precincts or
districts, since the Census Bureau draws it independently.

This matters a lot for this project's long-term goal of connecting
demographics to election results: getting demographic data onto voting
geography requires a **crosswalk** (typically via the Census Bureau's own
block-level correspondence files, or geometric/areal-interpolation methods
when official crosswalks aren't published for a given geography pair).

## Open questions / things to verify before building the data model

- Whether Colorado publishes an official **precinct-to-district
  correspondence file** per election cycle (this would be the ideal
  ground-truth crosswalk, better than geometric interpolation).
- Whether historical precinct boundaries (pre-2021 maps) are archived
  anywhere, since precinct lines shift more frequently than every 10 years.
- The exact statutory/charter process Denver uses for council redistricting
  (commission composition, criteria, public input process) — needs its own
  read of the Denver City Charter.
- Whether county commissioner districts (a `sub-county` geography relevant
  for Colorado's other 63 counties but not Denver) need to be in scope later.

## Related docs

- [`../OVERVIEW.md`](../OVERVIEW.md) — project goals and phased plan
- `redistricting.md` (planned) — deep dive on Amendment Y/Z commission
  process and gerrymandering metrics
- `offices.md` (planned) — office-by-office catalog (term lengths, current
  officeholders as of a snapshot date)
