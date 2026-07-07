# Office Catalog — Colorado / Denver

Office-by-office reference for every race in this project's primary scope
(see [`../OVERVIEW.md`](../OVERVIEW.md#elections-of-primary-interest)): term
length, how the office is elected, and current officeholder.

**Snapshot date: 2026-07-07.** Officeholders and legislative composition
change with every election — treat the "current officeholder" fields as a
point-in-time snapshot to be refreshed periodically (see the note at the
bottom), not a live source of truth. For anything time-sensitive, re-verify
before relying on it.

## Federal

| Office | Term | How elected | Current (as of 2026-07-07) |
|---|---|---|---|
| US President | 4 years, max 2 terms | Electoral College — each state awards electors (Colorado has **10**: 8 for its US House seats + 2 for its Senate seats); 48 states + DC use winner-take-all, Colorado included | Donald Trump (took office 2025-01-20); VP JD Vance |
| US Senate (CO seat 1) | 6 years, staggered | Statewide popular vote | Michael Bennet (D) — term through Jan 2029; running for CO Governor in 2026 (see below) |
| US Senate (CO seat 2) | 6 years, staggered | Statewide popular vote | John Hickenlooper (D) — first elected 2020; won the 2026-06-30 primary, on the Nov 2026 ballot for a 2nd term |
| US House (CO-01) | 2 years | District popular vote (Denver-area) | Diana DeGette (D) |
| US House (CO-02) | 2 years | District popular vote | Joe Neguse (D) |
| US House (CO-03) | 2 years | District popular vote (Western Slope) | Jeff Hurd (R) |
| US House (CO-04) | 2 years | District popular vote (Eastern Plains) | Lauren Boebert (R) |
| US House (CO-05) | 2 years | District popular vote (Colorado Springs area) | Jeff Crank (R) |
| US House (CO-06) | 2 years | District popular vote (Aurora area) | Jason Crow (D) |
| US House (CO-07) | 2 years | District popular vote (Jefferson County area) | Brittany Pettersen (D) |
| US House (CO-08) | 2 years | District popular vote (north Denver metro) | Gabe Evans (R) — flipped from D in 2024 |

CO's federal delegation is currently split 4D/4R in the House, both Senate
seats Democratic. See [`redistricting.md`](redistricting.md) for how the 8
House district boundaries are drawn.

## State (Colorado)

| Office | Term | How elected | Current (as of 2026-07-07) |
|---|---|---|---|
| Governor | 4 years, max 2 consecutive | Statewide popular vote | Jared Polis (D) — term-limited, cannot run again in Nov 2026; the 2026 Democratic primary was won by AG Phil Weiser (upsetting Bennet, who had also run) |
| State Senate | 4 years, staggered (~half up each cycle) | District popular vote, 35 districts | Democratic majority, 23–12 (as of the 2025–26 session) |
| State House | 2 years, all seats each cycle | District popular vote, 65 districts | Democratic majority, 43–22 (as of the 2025–26 session) |

Colorado has been a **Democratic trifecta** (governor + both legislative
chambers) continuously since 2019. All 65 House seats and roughly half of
the 35 Senate seats are on the Nov 2026 ballot. See
[`redistricting.md`](redistricting.md) for how Senate/House district
boundaries are drawn (Amendment Z commission).

## Local (Denver)

| Office | Term | How elected | Current (as of 2026-07-07) |
|---|---|---|---|
| Mayor | 4 years | Citywide popular vote (runoff if no majority in first round) | Mike Johnston — elected 2023 |
| Clerk & Recorder | 4 years | Citywide popular vote | Paul López — runs Denver's elections division among other duties |
| City Council | 4 years | 11 members from single-member districts + 2 at-large members, citywide | 13 members total; Council President for the 2025–26 term is Amanda Sandoval (unverified against a primary source — confirm before citing) |

Denver's Clerk & Recorder's office is the one that directly administers
Denver's elections (ballots, precincts, canvassing) — relevant to
`geography.md`'s precinct discussion. Council district boundaries are
redrawn via Denver's own charter process every 10 years (separate from the
state Amendment Y/Z commissions — still an open research item, see
[`redistricting.md`](redistricting.md#open-questions--things-to-verify-later)).

A full current council roster (all 11 district members + 2 at-large) should
be pulled directly from
[denvergov.org's council directory](https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Denver-City-Council/Council-Members-Websites-Info)
rather than hand-maintained here, since individual district seats turn over
independently and this doc will go stale fastest at that level of detail.

## Keeping this doc current

Given how much of this table is election-cycle-dependent (2026 is a midterm
year for CO with Senate, Governor, all US House, all state House, and half
of state Senate on the ballot), this file should be re-verified:
- After the Nov 2026 general election, to update every row affected by that
  cycle.
- Whenever this project starts ingesting real results data (Phase 1/2 of
  the [overview plan](../OVERVIEW.md#phased-plan)) — at that point,
  officeholder history becomes *data* (in a results table) rather than
  something to track by hand in a markdown doc.

## Related docs

- [`geography.md`](geography.md) — the districts these offices are elected from
- [`redistricting.md`](redistricting.md) — how district boundaries are drawn
- [`../OVERVIEW.md`](../OVERVIEW.md) — project goals and phased plan

## Sources

- [2026 US Senate election in Colorado — Wikipedia](https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_Colorado)
- [2026 Colorado gubernatorial election — Wikipedia](https://en.wikipedia.org/wiki/2026_Colorado_gubernatorial_election)
- [Colorado Sun: Bennet's campaign for governor](https://coloradosun.com/2025/04/11/michael-bennet-colorado-governor-bid-2026/)
- [GovTrack: Colorado's congressional delegation](https://www.govtrack.us/congress/members/CO)
- [Ballotpedia: Party control of Colorado state government](https://ballotpedia.org/Party_control_of_Colorado_state_government)
- [Denverite: Denver clerk/mayor 2026 budget dispute](https://denverite.com/2025/09/16/denver-elections-budget-cuts/)
- [Denver City Council — Wikipedia](https://en.wikipedia.org/wiki/Denver_City_Council)
