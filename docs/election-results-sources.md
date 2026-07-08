# Historical Election Results Sources — Colorado / Denver

Phase 1 deliverable: where to get historical election results at
district/county level for the offices in scope (see `OVERVIEW.md`).
Precinct-level results are deferred to Phase 3/4 alongside precinct
boundaries (see [`data-sources.md`](data-sources.md#precincts-deferred--phase-34-not-phase-1)).

Unlike boundaries, results come from three genuinely different systems —
one per office tier — and each has a different acquisition story. This doc
also records the practical friction each one has, since (unlike the
boundary files) not everything here can be scripted end-to-end yet.

## Quick reference

| Office | Source | Format | Years | Status |
|---|---|---|---|---|
| US President | MEDSL (Harvard Dataverse + GitHub mirror) | CSV/TSV, county-level | 2000–2016 (GitHub, no gate); 2000–2024 (Dataverse, gated) | **Downloaded** (2000–2016) |
| US House | MEDSL (Harvard Dataverse) | TSV, district-level | 1976–2024 | Blocked on guestbook — see below |
| US Senate | MEDSL (Harvard Dataverse) | TSV, state-level | 1976–2024 | Blocked on guestbook — see below |
| CO Governor | Colorado historical elections database | Web UI (searchable) | 1902–2025 | Needs further investigation (JS app, no obvious API found yet) |
| CO State Senate / House | Colorado historical elections database | Web UI (searchable) | 1902–2025 | Same as Governor |
| Denver City Council | Denver Elections Division results portal | Tableau dashboard | 2008–2025 | Needs further investigation (Tableau embed, no obvious export API found yet) |

## US President / House / Senate — MEDSL

**Source:** [MIT Election Data and Science Lab](https://electionlab.mit.edu/data), published on [Harvard Dataverse](https://dataverse.harvard.edu/dataverse/medsl_election_returns). This is the standard, citable, widely-used academic source for federal election returns — clean, versioned, documented via a codebook per dataset, county/district-level rather than precinct (matches Phase 1 scope exactly).

**The catch:** every file on Harvard Dataverse is gated behind a "guestbook"
— a one-time form (name/email/institution/purpose) MEDSL uses to track who's
using their data. Confirmed via direct API testing: `curl`-ing any file
download URL returns `"You may not download this file without the required
Guestbook response for guestbookID 458."` (HTTP 400) regardless of which
dataset. This can't be scripted around honestly — it's a consent form
collecting real identity info for MEDSL's own reporting, not a technical
obstacle to route around. **Manual one-time step required:** visit the
dataset page in a browser, fill in the guestbook, download the file, then
drop it in the corresponding `data/raw/` folder below.

Relevant datasets (persistent IDs stable, confirmed via the Dataverse API):

| Dataset | DOI | File(s) | Years | Level |
|---|---|---|---|---|
| County Presidential Election Returns 2000-2024 | `10.7910/DVN/VOQCHQ` | `countypres_2000-2024.tab` | 2000–2024 | County |
| U.S. House 1976–2024 | `10.7910/DVN/IG0UN2` | `1976-2024-house.tab` | 1976–2024 | District (constituency-level) |
| U.S. Senate statewide 1976–2024 | `10.7910/DVN/PEJ5QU` | `1976-2024-senate-state.tab` | 1976–2024 | State |

**Workaround already used for part of this — no gate, no manual step:**
MEDSL also mirrors their pre-2018 presidential county returns on GitHub,
unrestricted: [`MEDSL/county-returns`](https://github.com/MEDSL/county-returns)
(`countypres_2000-2016.csv`). This is a legitimate MEDSL-maintained mirror,
not a workaround of their consent gate — it simply predates when they moved
to gating everything through Dataverse. **This is what's actually downloaded
into `data/raw/` right now** — see the Acquisition Log below. It only covers
president through 2016; House, Senate, and 2018–2024 president still need
the manual Dataverse step above.

## CO Governor / State Senate / State House

**Source:** [Colorado historical elections database](https://historicalelectiondata.coloradosos.gov/) — "a searchable database of historical election information, all from official source documents," covering 1902–2025, including candidate results, ballot questions, party enrollment, voter registration, and turnout.

This is a Next.js (JS-rendered) application — no static download links or
obvious REST API surfaced from the raw HTML (checked via `curl`, no `/api/`
references in the served markup). It very likely has an internal API the
frontend calls, but finding it needs actual browser devtools (watching
network requests while using the search UI), which isn't something to guess
at from static HTML. **Open item, not yet resolved.**

Fallback options if the API can't be found cleanly:
- The Secretary of State's [Election Results Archives](https://www.sos.state.co.us/pubs/elections/Results/Archives.html) publish PDF "abstracts of votes cast" per election — authoritative but would need PDF parsing, not a clean structured download.
- [Ballotpedia](https://ballotpedia.org/Colorado_State_Senate_elections) has synthesized seat-control history (which party held which seats each cycle) but not raw vote totals — useful for cross-checking, not as a primary data source.

## Denver City Council

**Source:** [Denver Elections Division results portal](https://denvergov.org/electionresults) and its [data/maps archive](https://denvergov.org/content/denvergov/en/denver-elections-divison/data-maps/results-maps-archive.html), covering 2008–2025 (presidential, general, primary, and municipal/coordinated elections).

Results are served through an interactive Tableau dashboard, not static
files. Tableau workbooks often expose a way to export the underlying
crosstab data, but that typically requires interacting with the embedded
viz (not scriptable from a plain HTTP request the way the council-districts
boundary layer was via its ArcGIS FeatureServer). **Open item, not yet
resolved** — worth checking whether Denver's Open Data Catalog
(`denvergov.org/opendata`, same ArcGIS Hub instance used for council
districts) separately hosts election results as a feature layer/table,
the way it did for boundaries.

## Acquisition log

- **2026-07-08** — Downloaded `countypres_2000-2016.csv` (4.5 MB) from
  `github.com/MEDSL/county-returns` (raw, unrestricted) into
  `data/raw/election_results/president_county/2000-2016/`, via
  `scripts/fetch_election_results.py`. Provenance sidecar written
  alongside it. **Verified**: 5 cycles present (2000/2004/2008/2012/2016),
  50,524 total rows, 1,020 Colorado rows; spot-checked Adams County 2016
  (Clinton 96,558 / Trump 80,082) against known results — correct. Not yet
  filtered to Colorado — that happens in the processing step, same pattern
  as counties in `scripts/process_phase1_boundaries.py`.

## Next steps

- [ ] Manually complete the MEDSL Dataverse guestbook (one-time) and
      download `countypres_2000-2024.tab`, `1976-2024-house.tab`, and
      `1976-2024-senate-state.tab` into `data/raw/election_results/`
- [ ] Investigate `historicalelectiondata.coloradosos.gov`'s actual data
      API via browser devtools (Governor + State Senate/House results)
- [ ] Investigate whether Denver's ArcGIS Hub has an election-results
      feature layer/table separate from the Tableau dashboard
- [ ] Once results land, build the Phase 2 join to boundaries (needs the
      geography crosswalk — county FIPS in MEDSL's files vs. `GEOID` in
      the processed county boundaries; CD/SD/HD results join on district
      number directly, no crosswalk needed there)
